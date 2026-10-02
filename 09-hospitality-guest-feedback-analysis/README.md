# Use Case


Automates guest feedback processing — guests submit a form after their stay, an AI model analyzes the sentiment, and the system routes responses automatically: a thank-you email to the guest for positive feedback, and internal alerts to hotel management for neutral or negative reviews.

## Workflow
Guest Feedback Form → Sentiment Analysis (Basic LLM Chain, Groq) → Routing (Switch) → Email Response (Guest or Management)

<p align="center">
<img width="984" height="511" alt="image" src="https://github.com/user-attachments/assets/328dcba2-e45b-4a84-a278-da7601c72ce0" />
</p>

## How it was built
- n8n Form Trigger with fields: room number (Number), check-in date (Date), check-out date (Date), overall rating (Radio Buttons: 1–5), feedback (Textarea), email address (Text Input)
- Basic LLM Chain (Groq, `openai/gpt-oss-20b`) analyzes the free-text feedback **and the numeric rating together**, returning structured JSON with sentiment (positiv/neutral/negativ), topics, and a one-sentence summary
- The rating was collected from the start but originally unused by the prompt — added as a second signal specifically to catch sarcasm: a glowing text with a 1/5 rating is flagged negative instead of taken at face value
- System prompt explicitly instructs the model to return raw JSON only — no markdown, no code blocks
- Switch Node routes based on `JSON.parse($json.text).sentiment` to one of three paths
- Positive feedback → Dankes-Mail (thank-you email) sent directly to the guest's submitted email address
- Neutral feedback → Internal info email to hotel management with full details and AI summary
- Negative feedback → Urgent alert email to hotel management with action-required subject line and AI summary
- Model temperature set to 0 — found through testing that the default (0.7) produced different results for the identical sarcasm case across repeated runs; see eval suite section below

## How it works
1. A guest submits the feedback form after their stay — room number, dates, rating, and free-text feedback
2. The model analyzes the feedback text together with the numeric rating and classifies sentiment as positiv, neutral, or negativ — a mismatch between the two (e.g. praising words, low rating) is treated as a sarcasm signal
3. The Switch Node routes the data to the correct email path
4. Positive: guest receives a personalized thank-you email with their feedback details
5. Neutral/Negative: management receives an internal alert with full guest data and AI-generated summary for follow-up

**Verified against real form submissions:** tested four live cases through the actual production trigger — clear positive, clear negative, a sarcasm case (glowing text, 1/5 rating), and a control case (mildly critical wording, 5/5 rating, meant to check the model doesn't just blindly follow the number). All four routed correctly, repeated twice with identical results after fixing the model's temperature (see below).

**Known limitation:** The production workflow (09) itself runs without an error 
branch — malformed model output would fail at the JSON.parse in the Switch node. 
In a real deployment this would be the first hardening step (continue-on-error + 
fallback notification, as implemented in the eval suite 09b).
   
## Nodes & Tools

- n8n Form Trigger
- n8n Basic LLM Chain
- Groq Chat Model (`openai/gpt-oss-20b`)
- n8n Switch Node
- Gmail (OAuth2)

## Background
Designed for hotels that want to close the feedback loop automatically. Positive reviews are acknowledged immediately — improving guest experience without manual effort. Negative feedback triggers an instant internal alert so management can respond before the guest writes a public review. The check-in and check-out dates are stored to enable future analysis of seasonal patterns, occupancy correlations, and service quality over time.

# Eval Suite (09b)

The AI classification step is covered by a separate evaluation workflow
(`09b–sentiment-eval-suite.json`). Instead of assuming the sentiment
classification works, it measures how well it works:

**Setup:** Manual Trigger → Google Sheets (29 labeled test cases) → Basic
LLM Chain + Groq Chat Model (same system prompt and model as the production
workflow) → automated comparison against the expected label → results
written back to the sheet (processing status, model output, correct
yes/no). Requests run in batches of 5 with a 40-second pause between
batches — Groq's free tier limits to 8000 tokens/minute, not
requests/minute, and running all 29 items back-to-back hit that cap after
roughly 13-16 calls.

<p align="center">
<img width="1108" height="456" alt="image" src="https://github.com/user-attachments/assets/9cc71351-3a60-4260-90fe-1ae425f0ca1f" />
</p>

**Test set design (v1, 25 cases):** German hotel feedback cases across
three sentiment classes, deliberately including hard cases — irony, mixed
sentiment, short answers and emoji-only feedback.

**v1 baseline:**
- 23/25 correct = **92%**, measured with GPT-4.1-mini (OpenAI), text only
- Both misclassifications were mixed-sentiment cases (praise + complaint in
  one text), resolved by the model in opposite directions — pointing to a
  definition gap rather than a model weakness

**v1 labeling policy (derived from the v1 results):**
- A concretely named complaint counts as negative, even if other aspects
  are praised — a complaint is a fact, not an interpretation
- Irony alone, without a named problem, does not make feedback negative
- Where a numeric rating exists, it should drive the routing; text
  classification covers channels without ratings (e.g. email)

**v2: the rating as a second signal.** The guest form always collected a
1–5 star rating alongside the free text, but the original prompt only
looked at the text. That meant genuine sarcasm — glowing text with a
1-star rating — read as positive. v2 adds the rating to the prompt and
instructs the model to treat a mismatch between text and rating as a
sarcasm signal, with the rating taking precedence. 4 new cases were added
to the test set: two clear sarcasm cases, one control case (mildly
critical wording but a 5-star rating, meant to catch the model
over-correcting and just following the number), and one short ambiguous
case — 29 cases total.

**v2 results:** 29/29 correct = **100%**, measured with `openai/gpt-oss-20b`
via Groq, including the previously-failing mixed-sentiment case (id 25)
and all 4 new sarcasm/control cases. As with eval suite 11b, a 100% result
is treated with more suspicion than celebration — it says the test set
isn't hard enough yet to find where this prompt breaks, not that it's
bulletproof.

**Non-determinism found and fixed.** The first live test of the sarcasm
case — through the real production form trigger, not the eval suite —
came back positive instead of negative, even though the identical text ran
correctly inside the eval suite minutes earlier. Both workflows used the
same default temperature (0.7, unset in the node, confirmed in the
execution logs). Setting `temperature: 0` in both the production workflow
and the eval suite's Groq node fixed it: two repeated full eval runs
(29/29 twice) and two repeated 4-case production runs (4/4 twice) now
return identical results every time. Documented here deliberately — a
single passing test run doesn't prove a prompt works if the model is
sampling with any randomness; two passing runs at temperature 0 is what
actually supports the claim.

**Next iteration (v3, planned):** test cases with genuinely overlapping
signals — a high rating with sharply critical text, or a rating that
itself seems miskeyed — to find where the rating-as-signal logic actually
breaks, rather than confirming it works on cases it was always likely to
get right.
