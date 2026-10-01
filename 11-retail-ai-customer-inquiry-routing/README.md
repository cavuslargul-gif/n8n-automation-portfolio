# 11 – Retail: AI Customer Inquiry Routing

## Use Case
Automatically categorizes incoming customer inquiries for a craft/trade business using AI and routes them by email to the right department — replacing manual sorting and forwarding of requests.

## Workflow
Webhook (Form Submission) → Normalize Fields → Request-ID (Hash, Crypto) → Duplicate Check (Data Table, `rowNotExists`) → AI Categorization (Groq / Basic LLM Chain) → Category Fallback (Set Node) → Target Address Mapping → Gmail (Internal Notification) + Audit Log (Data Table) → Dedupe Key Saved

<img width="1151" height="564" alt="image" src="https://github.com/user-attachments/assets/3c3f74ac-39d5-41b4-8adf-282aba720835" />

## How it was built
- **Webhook** receives POST requests simulating the website contact form (name, email, message, source) — designed to later also accept real inbound email as an additional trigger
- **Set node** normalizes incoming fields to a consistent shape: name, email, nachricht (message), quelle (source)
- **Crypto node** hashes name+email+message (SHA256) as a fallback idempotency key, used only when the client doesn't supply its own `request_id`
- **Data Table** (`rowNotExists`) checks a dedicated dedupe table for that key — if it's already there (e.g. a webhook retry from the sender), the item is dropped here and nothing downstream runs: no duplicate task, no duplicate email
- **Basic LLM Chain** (Groq, `openai/gpt-oss-20b`) classifies the message into exactly one of four categories: Angebot (quote request), Terminanfrage (appointment request), Reklamation (complaint), Sonstiges (other)
- **Set node** parses the model's raw answer and falls back to "Sonstiges" if the response doesn't match one of the four expected categories — a safety net against unexpected model output
- **Set node** maps each category to a fixed target mailbox (placeholder addresses for the portfolio, e.g. `angebot@test.de`)
- **Gmail** sends the inquiry, including sender details, to the matched department mailbox
- **Data Table** writes an audit log entry per classification (timestamp, workflow name, message, category, model, status) — documents every AI decision for traceability
- **Data Table insert** saves the dedupe key only *after* the audit log write succeeds — if something fails earlier in the chain, the item is more likely to be safely reprocessed than silently lost
- Connected to a central error-handler workflow via Error Trigger Node — errors are logged automatically, active only on production executions

## How it works
1. A customer inquiry arrives via the webhook (currently simulating the website form)
2. Name, email, message, and source are normalized into a consistent format
3. A request ID is determined (client-supplied, or a hash of the message content) and checked against previously processed requests
4. If it's a duplicate, processing stops right there — no AI call, no email, no new log entry
5. Otherwise, the AI model classifies the message into one of four categories
6. If the model's answer doesn't match an expected category, it defaults to "Sonstiges" instead of failing
7. The category is mapped to a fixed department mailbox and an internal notification email is sent
8. The classification is logged to a data table, then the dedupe key is saved

**Note:** Currently triggered via a test webhook with simulated form data — built to later also accept real inbound email as an additional trigger, without changing the categorization or dedupe logic.

**Idempotency, verified:** Sending the identical request twice through the real webhook trigger produced exactly one processed case — the second attempt stopped cleanly at the duplicate check, with no second email and no second audit log row.

**Planned next:** an evaluation suite (11b) measuring the classifier's accuracy against a labeled test set, mirroring workflow 09b's methodology — currently the four-category routing is tested for malformed-response handling (see Production Checklist) but not yet for classification accuracy itself.

## Nodes & Tools
- n8n Webhook
- n8n Set / Edit Fields
- n8n Crypto (SHA256 hash)
- n8n Data Table (dedupe check + audit log)
- n8n Basic LLM Chain
- Groq Chat Model (`openai/gpt-oss-20b`)
- Gmail (OAuth2)

## Background
Built for craft/trade businesses that receive customer inquiries through multiple channels and currently sort them manually. AI classification removes that first triage step, while the fallback to "Sonstiges" and the audit log keep the system honest about uncertain cases instead of silently misrouting them. Pure routing workflow: no automatic replies to customers, no AI-generated responses sent externally — only internal notification.
