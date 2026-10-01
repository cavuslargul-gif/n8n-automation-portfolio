# 11 – Retail: AI Customer Inquiry Routing

## Use Case
Automatically categorizes incoming customer inquiries for a craft/trade business using AI and routes them by email to the right department — replacing manual sorting and forwarding of requests.

## Workflow
Webhook (Form Submission) → Normalize Fields → AI Categorization (Groq / Basic LLM Chain) → Category Fallback (Set Node) → Target Address Mapping → Gmail (Internal Notification) + Audit Log (Data Table)

<img width="1151" height="564" alt="image" src="https://github.com/user-attachments/assets/3c3f74ac-39d5-41b4-8adf-282aba720835" />

## How it was built
- **Webhook** receives POST requests simulating the website contact form (name, email, message, source) — designed to later also accept real inbound email as an additional trigger
- **Set node** normalizes incoming fields to a consistent shape: name, email, nachricht (message), quelle (source)
- **Basic LLM Chain** (Groq, `openai/gpt-oss-20b`) classifies the message into exactly one of four categories: Angebot (quote request), Terminanfrage (appointment request), Reklamation (complaint), Sonstiges (other)
- **Set node** parses the model's raw answer and falls back to "Sonstiges" if the response doesn't match one of the four expected categories — a safety net against unexpected model output
- **Set node** maps each category to a fixed target mailbox (placeholder addresses for the portfolio, e.g. `angebot@test.de`)
- **Gmail** sends the inquiry, including sender details, to the matched department mailbox
- **Data Table** writes an audit log entry per classification (timestamp, workflow name, message, category, model, status) — documents every AI decision for traceability
- Connected to a central error-handler workflow via Error Trigger Node — errors are logged automatically, active only on production executions

## How it works
1. A customer inquiry arrives via the webhook (currently simulating the website form)
2. Name, email, message, and source are normalized into a consistent format
3. The AI model classifies the message into one of four categories
4. If the model's answer doesn't match an expected category, it defaults to "Sonstiges" instead of failing
5. The category is mapped to a fixed department mailbox and an internal notification email is sent
6. Every classification is logged to a data table for audit purposes

**Note:** Currently triggered via a test webhook with simulated form data — built to later also accept real inbound email as an additional trigger, without changing the categorization logic.

## Nodes & Tools
- n8n Webhook
- n8n Set / Edit Fields
- n8n Basic LLM Chain
- Groq Chat Model (`openai/gpt-oss-20b`)
- Gmail (OAuth2)
- n8n Data Table (audit log)

## Background
Built for craft/trade businesses that receive customer inquiries through multiple channels and currently sort them manually. AI classification removes that first triage step, while the fallback to "Sonstiges" and the audit log keep the system honest about uncertain cases instead of silently misrouting them. Pure routing workflow: no automatic replies to customers, no AI-generated responses sent externally — only internal notification.
