# 05 – Education: AI Learning Request Routing

## Use Case
Automatically classifies incoming learning requests by skill level using AI and sends personalized resource recommendations via email — designed for educational providers, online courses, or internal training programs.

## Workflow
Form Trigger → Basic LLM Chain + Groq (AI classification) → Switch (3-way routing + fallback) → Gmail (personalized recommendations) + Gmail (error notification)

<p align="center">
<img width="494" height="606" alt="image" src="https://github.com/user-attachments/assets/f162ef11-7a9a-420b-b2eb-815d562e3592" />
</p>

## How it was built
- Form Trigger configured with three fields: name, learning topic, and self-assessment (Anfänger / Fortgeschritten / Experte)
- Basic LLM Chain with a Groq chat model (`openai/gpt-oss-20b`, temperature 0) classifies requests — originally an OpenAI node; replaced when the workflow was migrated to a self-hosted instance without an OpenAI credential
- Switch node in Rules mode routing to three separate branches based on AI output, comparing the trimmed answer without regard to case or trailing punctuation, plus a fallback output for any answer that matches none of the three levels
- Three Gmail nodes connected via OAuth2, each with level-specific resource recommendations
- Error handling on the AI node (Continue using error output) and on the Switch fallback, both leading to a dedicated Fehlerbericht Gmail node that reports name, topic and the raw AI answer
- Connected to the central error handler (workflow 13) via the Error Workflow setting
- Tested end-to-end with all three routing paths, then against deliberately bad input (see below)

## How it works
1. A learner submits their request via the form (name, topic, self-assessment)
2. The model analyzes the topic and self-assessment and returns one word: Anfänger, Fortgeschritten, or Experte
3. The Switch node routes the request to the matching branch
4. A personalized email with level-appropriate resources is sent automatically
5. If the AI call fails, or the model answers with something that isn't one of the three levels, a Fehlerbericht email is sent instead of the run ending silently

**Known-bad-payload test (found and fixed):** The original Switch compared the AI's answer for exact equality and had no fallback output. Feeding it a topic that contained a formatting instruction (answer in lowercase with a trailing period) made the model reply `anfänger.` — matching none of the three rules, so the run ended as "success" with no email and no error report. Nobody would have noticed a learner never getting a reply.

The fix has three parts: the answer is trimmed and stripped of trailing punctuation before comparing, the comparison ignores case, and anything still unrecognized goes through a fallback output to the error report. Verified against the published workflow in production mode: the same input now routes to the Anfänger branch, and — to exercise the fallback itself — the system prompt was temporarily changed so the model answered `Quatsch`, which landed in the error report with the right context; the prompt was then restored and re-tested.

Worth knowing what did *not* break it: prompt-injection style topics (an instruction to answer only `Quatsch`, to use number codes, to answer in English, to "forget the classification") were all ignored by the model, which kept to the three-word format.

**Empty topic — and a correction.** The form's own description said "Optional — kannst du leer lassen", although the field is required; that text is gone. I first assumed a whitespace-only topic would slip through the form and checked it in a browser: it doesn't — the n8n form itself rejects it ("This field is required") and no execution even starts. My first whitespace test was a direct API call that bypassed the form UI, which is why it looked like a gap.

**A loop that was built and removed.** For topics that are merely too short (`ab`) I built a validation loop: a second form page asking again, at most 5 rounds, then an abort email. It worked in a real browser test. I removed it again: it added six nodes for a case that does not cause a wrong result, since the model classifies from the self-assessment plus the topic and `ab` is routed to a sensible level. Re-verified against the published workflow in production mode after the rollback: a normal request (Experte), the formatting-instruction topic (`anfänger.`, still routed to Anfänger) and a two-character topic (`ab`, routed by self-assessment, no fallback) all ended in the right email.

## Tools
- n8n Form Trigger
- n8n Basic LLM Chain
- Groq Chat Model (`openai/gpt-oss-20b`)
- Switch Node (Rules mode, 3 outputs + fallback)
- Gmail (×4: Anfänger, Fortgeschrittene, Experten, Fehlerbericht)
- Error Handling (Continue using error output, central error workflow)

## Background
Built to demonstrate AI-powered routing in an educational context. The workflow simulates how training providers or HR departments could automatically match learners to the right resources without manual triage — using AI classification instead of simple keyword matching.
