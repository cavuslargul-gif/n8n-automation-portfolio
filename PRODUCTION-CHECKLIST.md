# Production-Readiness Checklist

How I assess whether an automation is production-ready — and where my own
portfolio currently stands against that bar.

The criteria are compiled from my own research in the n8n community forum:
I analyzed how operators who run workflows in production vet quality and
what they test for before trusting an automation with real business
processes. This checklist is my working standard, applied honestly to my
own repository — including the gaps.

| # | Criterion | What it means | Status in this portfolio | Next step |
|---|---|---|---|---|
| 1 | **Idempotency / Dedupe** | Duplicate inbound events (webhook retries!) must not create duplicate records or actions. Dedupe by event ID at the entry point. | 🟡 Basic dedupe key implemented (unique case IDs in workflow 08). No event-ID dedupe on webhook entry yet. | Workflow 10 (e-commerce order intake) is designed around a webhook dedupe key. |
| 2 | **Retry & Backoff** | Explicitly configured retries with increasing waits — never default-hammering a recovering API. | 🔴 Not yet implemented. | Part of workflow 10; rate-limit handling tested against real 429s. |
| 3 | **Error paths** | Failures route to a defined branch with notification — no silent dying. | 🟡 Implemented exemplarily (workflows 05, 07 and eval suite 09b via continue-on-error + error notification). Documented as known limitation where absent (09). | Extend pattern to remaining AI workflows. |
| 4 | **Dead-Letter Queue & Replay** | Payloads that exhaust retries land in a DLQ with status + retry count; replay is one click. | 🔴 Not yet implemented. | Planned as the core of workflow 10 (sheet-based DLQ with replay trigger). |
| 5 | **Audit trail** | Any run reconstructable after the fact: timestamp, payload, outcome. | 🟡 n8n execution log (limited retention) + results written back to sheets in the eval suite. No dedicated long-term sink yet. | Add a structured log sink to workflow 10. |
| 6 | **Secrets handling** | Credentials live only in the credential vault; exports and repos contain placeholders only. | ✅ All published JSONs sanitized (placeholder IDs, no addresses, no keys). | Keep as standing review step before every commit. |
| 7 | **Monitoring / Heartbeat** | Something alerts when the workflow *stops* running — not only when it fails. | 🔴 Not yet implemented. | Planned for workflow 11 (threshold alerts + heartbeat). |
| 8 | **Tested against bad inputs** | Happy path AND malformed input: empty results, broken payloads, edge cases. | 🟡 All workflows tested end-to-end with live runs; eval suite includes deliberately hard cases (irony, mixed sentiment, emoji-only). No malformed-payload test set yet. | Add one "known bad" payload per workflow. |
| 9 | **Measured AI quality (evals)** | AI steps are measured against a labeled test set, not assumed to work. | ✅ Eval suite 09b: 25 labeled cases, 92% baseline, documented labeling policy, iteration planned. | v2 iteration (refined prompt, model parity). |
| 10 | **Version control** | Workflow JSONs live in git with meaningful history. | ✅ This repository. | — |
| 11 | **Documentation & handoff** | A colleague could understand, run and maintain the workflow from the docs alone. | ✅ Per-workflow READMEs (use case, build notes, node tables, screenshots, known limitations). 🟡 No operational runbook (who reacts to what, when) yet. | Add a lightweight runbook template with workflow 10. |
| 12 | **Honest scope decisions** | What is deliberately *not* built is documented, not hidden. | ✅ Known limitations stated in READMEs; this checklist itself. | — |

**Legend:** ✅ implemented · 🟡 partially implemented · 🔴 not yet — planned

*This is a living document. The point is not a perfect scorecard — it is
knowing exactly where the gaps are before someone else finds them.*
