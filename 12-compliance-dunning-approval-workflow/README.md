# 12 – Cross-Domain: Dunning Approval with Human-in-the-Loop and Audit Trail

## Use Case
Daily check for overdue invoices that enforces a human approval step before any dunning notice is sent — no automated reminder email ever reaches a customer without a person explicitly signing off. Every decision (approve or defer), who made it, and why is written back to the record. Built as the compliance/audit layer underneath workflow 10's dunning digest: this is the workflow that actually sets the `offene_posten` status that workflow 10 later reads and summarizes.

## Workflow
Schedule Trigger (daily 9:00) → Fetch Overdue Invoices (Data Table) → Approval Request (Gmail Send-and-Wait, custom form, 7-day limit) → Response Received? (IF) → **No (timeout)**: Deputy (Set) → Reminder Email, record stays "offen" **or** **Yes**: Branch on decision → Send Dunning Email + Mark "gemahnt" (approved) **or** Mark "zurückgestellt" (deferred), both with decision-maker and reason logged

<img width="1559" height="693" alt="image" src="https://github.com/user-attachments/assets/70f4719f-d347-43e6-a237-b2822d3fa0fc" />

## How it was built
- **Schedule Trigger** runs daily at 9:00
- **n8n Data Table** (`offene_posten`) fetches all rows where `status = offen` and `faelligkeitsdatum <= today`
- **Gmail Send-and-Wait** with a custom form pauses the workflow and asks a human to decide — three fields: a required "Freigabe" dropdown (Freigeben/Zurückstellen), a required "Entscheidende Instanz" (decision-maker name), and an optional "Begründung" (reason). A 7-day **Limit Wait Time** means the node resumes automatically if nobody responds, instead of waiting forever
- **IF node** ("Antwort erhalten?") checks whether the resume carries real form data or came from the 7-day timeout
- Timeout branch: **Set node** holds a deputy address, then **Gmail** sends a reminder to the original requester, CC'd to the deputy — no data table write, the record deliberately stays `offen` since both outcomes (approve or defer) remain open
- Response branch: a second **IF node** branches on the dropdown response
- Approved: **Gmail** sends the actual dunning email to the customer, then a **Data Table update** sets `status = gemahnt` plus `entschieden_von` and `begruendung`
- Deferred: **no customer email at all** — only a **Data Table update** sets `status = zurueckgestellt` plus the same `entschieden_von` and `begruendung`
- Connected to the same central error-handler workflow as the other admin workflows

## How it works
1. Every morning at 9:00, the workflow pulls all invoices that are both unresolved and past due
2. For each one, a human receives an approval request by email and must explicitly choose "Freigeben" or "Zurückstellen" before anything else happens
3. If nobody responds within 7 days, a reminder goes out to the original requester with the deputy CC'd — the record stays `offen`, untouched, since the decision is still open either way
4. If approved, the customer gets the dunning email and the record is marked `gemahnt`
5. If deferred, no email goes out and the record is marked `zurueckgestellt` instead
6. Either way, who decided and why is written to the record — including deferred cases, since a deferred decision can turn out to be the wrong call just as much as an approved one

**Compliance note:** The four-eyes requirement is structurally enforced, not just procedural — the "Mahnung senden" (send dunning email) node is only wired to the approved branch of the IF node. There is no path in the workflow that can send a dunning email without going through the approval form first.

**Escalation note:** The timeout path intentionally does not force a decision or pick a default — it only makes the open decision more visible. Who exactly counts as "the deputy" depends on the organization; in practice this is typically the accountant/bookkeeper's substitute. The reminder is a nudge, not an auto-approval or auto-deferral.

## Nodes & Tools

- n8n Schedule Trigger
- n8n Data Table
- Gmail Send-and-Wait (custom form, Limit Wait Time, OAuth2)
- n8n IF Node (×2)
- n8n Set
- Gmail (OAuth2)

## Background
Automated dunning carries real business risk — a reminder sent on an invoice that was already settled, disputed, or under a payment plan damages the customer relationship. This workflow keeps the AI/automation layer (workflow 10's digest) purely informational and puts the only action with external, customer-facing consequences behind a mandatory, logged human decision. The `entschieden_von` and `begruendung` columns turn every dunning case — approved or deferred — into an auditable decision rather than a silent automated action. The 7-day escalation closes the remaining gap: human-in-the-loop only works if someone eventually loops back in, so a stalled approval surfaces itself instead of sitting silently until someone happens to check.
