# Use Case


Automates guest feedback processing — guests submit a form after their stay, OpenAI analyzes the sentiment, and the system routes responses automatically: a thank-you email to the guest for positive feedback, and internal alerts to hotel management for neutral or negative reviews.

## Workflow
Guest Feedback Form → Sentiment Analysis (OpenAI) → Routing (Switch) → Email Response (Guest or Management)

<img width="655" height="397" alt="image" src="https://github.com/user-attachments/assets/9d43fbf7-0a50-4f64-80a1-80d40cebdaae" />

## How it was built
- n8n Form Trigger with fields: room number (Number), check-in date (Date), check-out date (Date), overall rating (Radio Buttons: 1–5), feedback (Textarea), email address (Text Input)
- OpenAI GPT-4o-mini analyzes the free-text feedback and returns structured JSON with sentiment (positiv/neutral/negativ), topics, and a one-sentence summary
- System prompt explicitly instructs the model to return raw JSON only — no markdown, no code blocks
- Switch Node routes based on JSON.parse($json.output[0].content[0].text).sentiment to one of three paths
- Positive feedback → Dankes-Mail (thank-you email) sent directly to the guest's submitted email address
- Neutral feedback → Internal info email to hotel management with full details and AI summary
- Negative feedback → Urgent alert email to hotel management with action-required subject line and AI summary
  
## Credentials & Authentication

<img width="629" height="155" alt="image" src="https://github.com/user-attachments/assets/928290cf-2c1d-4b86-8180-352ec841d9d9" />

## How it works
1. A guest submits the feedback form after their stay — room number, dates, rating, and free-text feedback
2. OpenAI analyzes the feedback and classifies sentiment as positiv, neutral, or negativ
3. The Switch Node routes the data to the correct email path
4. Positive: guest receives a personalized thank-you email with their feedback details
5. Neutral/Negative: management receives an internal alert with full guest data and AI-generated summary for follow-up

**Known limitation:** The production workflow (09) itself runs without an error 
branch — malformed model output would fail at the JSON.parse in the Switch node. 
In a real deployment this would be the first hardening step (continue-on-error + 
fallback notification, as implemented in the eval suite 09b).
   
## Nodes

<img width="631" height="473" alt="image" src="https://github.com/user-attachments/assets/b1284516-c053-44dd-a596-1683d40bb4dd" />

## Tools
- n8n Form Trigger
- OpenAI GPT-4o-mini
- n8n Switch Node
- Gmail (OAuth2)

## Background
Designed for hotels that want to close the feedback loop automatically. Positive reviews are acknowledged immediately — improving guest experience without manual effort. Negative feedback triggers an instant internal alert so management can respond before the guest writes a public review. The check-in and check-out dates are stored to enable future analysis of seasonal patterns, occupancy correlations, and service quality over time.

# Eval Suite (09b)

<img width="1263" height="555" alt="image" src="https://github.com/user-attachments/assets/7c2830f6-8941-4977-b5e8-adcef91949f5" />

The AI classification step is covered by a separate evaluation workflow
(`09b-sentiment-eval.json`). Instead of assuming the sentiment classification
works, it measures how well it works:

**Setup:** Manual Trigger → Google Sheets (25 labeled test cases) → OpenAI
(same system prompt as the production workflow) → automated comparison
against the expected label → results written back to the sheet
(processing status, model output, correct yes/no).

**Test set design:** 25 German hotel feedback cases across three sentiment
classes, deliberately including hard cases — irony, mixed sentiment, short
answers and emoji-only feedback.

**Results (v1 baseline):**
- 23/25 correct = **92%**, measured with GPT-4.1-mini
- Irony and emoji cases were classified correctly
- Both misclassifications were mixed-sentiment cases (praise + complaint in
  one text), resolved by the model in opposite directions — pointing to a
  definition gap rather than a model weakness

**Labeling policy (derived from the v1 results):**
- A concretely named complaint counts as negative, even if other aspects
  are praised — a complaint is a fact, not an interpretation
- Irony alone, without a named problem, does not make feedback negative
- Where a numeric rating exists, it should drive the routing; text
  classification covers channels without ratings (e.g. email)

**Next iteration (v2, planned):** refined prompt implementing the labeling
policy, extended test set (pure irony without complaint), and model parity
with the production workflow. Paused for now — a deliberate budget decision,
documented rather than hidden.
