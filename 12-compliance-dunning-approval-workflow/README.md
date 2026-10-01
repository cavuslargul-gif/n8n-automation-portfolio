# 12 – Cross-Domain: Dunning Approval with Human-in-the-Loop and Audit Trail

## Use Case
Daily check for overdue invoices that enforces a human approval step before any dunning notice is sent — no automated reminder email ever reaches a customer without a person explicitly signing off. Every decision (approve or defer), who made it, and why is written back to the record. Built as the compliance/audit layer underneath workflow 10's dunning digest: this is the workflow that actually sets the `offene_posten` status that workflow 10 later reads and summarizes.

## Workflow
Schedule Trigger (daily 9:00) → Fetch Overdue Invoices (Data Table) → Approval Request (Gmail Send-and-Wait, custom form) → Branch on decision → Send Dunning Email + Mark "gemahnt" (approved) **or** Mark "zurückgestellt" (deferred), both with decision-maker and reason logged

<!-- Canvas screenshot goes here -->

## How it was built
- **Schedule Trigger** runs daily at 9:00
- **n8n Data Table** (`offene_posten`) fetches all rows where `status = offen` and `faelligkeitsdatum <= today`
- **Gmail Send-and-Wait** with a custom form pauses the workflow and asks a human to decide — three fields: a required "Freigabe" dropdown (Freigeben/Zurückstellen), a required "Entscheidende Instanz" (decision-maker name), and an optional "Begründung" (reason)
- **IF node** branches on the dropdown response
- Approved branch: **Gmail** sends the actual dunning email to the customer, then a **Data Table update** sets `status = gemahnt` plus `entschieden_von` and `begruendung`
- Deferred branch: **no customer email at all** — only a **Data Table update** sets `status = zurueckgestellt` plus the same `entschieden_von` and `begruendung`
- Connected to the same central error-handler workflow as the other admin workflows

## How it works
1. Every morning at 9:00, the workflow pulls all invoices that are both unresolved and past due
2. For each one, a human receives an approval request by email and must explicitly choose "Freigeben" or "Zurückstellen" before anything else happens
3. If approved, the customer gets the dunning email and the record is marked `gemahnt`
4. If deferred, no email goes out and the record is marked `zurueckgestellt` instead
5. Either way, who decided and why is written to the record — including deferred cases, since a deferred decision can turn out to be the wrong call just as much as an approved one

**Compliance note:** The four-eyes requirement is structurally enforced, not just procedural — the "Mahnung senden" (send dunning email) node is only wired to the approved branch of the IF node. There is no path in the workflow that can send a dunning email without going through the approval form first.

## Nodes & Tools

<!-- Node list screenshot goes here -->

- n8n Schedule Trigger
- n8n Data Table
- Gmail Send-and-Wait (custom form, OAuth2)
- n8n IF Node
- Gmail (OAuth2)

## Background
Automated dunning carries real business risk — a reminder sent on an invoice that was already settled, disputed, or under a payment plan damages the customer relationship. This workflow keeps the AI/automation layer (workflow 10's digest) purely informational and puts the only action with external, customer-facing consequences behind a mandatory, logged human decision. The `entschieden_von` and `begruendung` columns turn every dunning case — approved or deferred — into an auditable decision rather than a silent automated action.
