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
| 1 | **Idempotency / Dedupe** | Duplicate inbound events (webhook retries!) must not create duplicate records or actions. Dedupe by event ID at the entry point. | 🟡 Flag-based dedupe implemented: workflow 10's `task_erstellt` column prevents the same dunning case from generating a duplicate Google Task on a repeat run — added after a real duplicate-run bug was caught and fixed in testing. No event-ID dedupe on webhook entry yet (relevant for workflow 11's webhook trigger). | Add a dedupe key at workflow 11's webhook entry point. |
| 2 | **Retry & Backoff** | Explicitly configured retries with increasing waits — never default-hammering a recovering API. | 🔴 Not yet implemented. | No current workflow has a rate-limited external API to test this against honestly — needs a real candidate before claiming it. |
| 3 | **Error paths** | Failures route to a defined branch with notification — no silent dying. | ✅ Workflows 10, 11 and 12 all route failures to a central error handler (workflow 13) via the Error Workflow setting — no silent failures, one shared mechanism instead of per-workflow logic. Workflows 05, 07 and eval suite 09b additionally use inline continue-on-error with user-facing notification for that specific case. | Apply the same central-handler pattern to 01–09 retroactively (currently each is standalone). |
| 4 | **Dead-Letter Queue & Replay** | Payloads that exhaust retries land in a DLQ with status + retry count; replay is one click. | 🔴 Not yet implemented. Workflow 13 logs every failure, but there's no retry count and no replay trigger — it's an audit log, not a DLQ. | Extend workflow 13's log with a status + retry-count column and a manual replay trigger. |
| 5 | **Audit trail** | Any run reconstructable after the fact: timestamp, payload, outcome. | ✅ Workflow 13 writes every failure (timestamp, workflow, node, message, execution ID) to a durable `workflow_error_log` table — not just n8n's execution log. Workflow 12 additionally logs every dunning decision (who decided, why) for both approved and deferred cases. | Define a retention/rotation policy for the log table. |
| 6 | **Secrets handling** | Credentials live only in the credential vault; exports and repos contain placeholders only. | ✅ All published JSONs sanitized (placeholder IDs, no addresses, no keys) — held up through workflows 10–14 as the repo grew. | Keep as standing review step before every commit. |
| 7 | **Monitoring / Heartbeat** | Something alerts when the workflow *stops* running — not only when it fails. | ✅ Workflow 15 checks daily whether workflow 10 wrote its heartbeat; if not, it alerts — catching a disabled trigger or deactivated workflow, cases the error handler (13) structurally can't see since no error ever fires. Both the monitor logic and its own error-handler coupling were verified against real production executions, not just manual test runs. | Extend the same heartbeat pattern to other schedule-driven workflows (12) if they go into real production use. |
| 8 | **Tested against bad inputs** | Happy path AND malformed input: empty results, broken payloads, edge cases. | 🟡 Concrete edge cases handled, not just claimed: workflow 11 falls back to "Sonstiges" when the AI response doesn't match an expected category; workflow 10's digest shows "None" instead of breaking when a list is empty. Eval suite 09b covers deliberately hard AI cases (irony, mixed sentiment, emoji-only). No dedicated malformed-payload test set yet. | Add one "known bad" payload per workflow. |
| 9 | **Measured AI quality (evals)** | AI steps are measured against a labeled test set, not assumed to work. | ✅ Eval suite 09b: 25 labeled cases, 92% baseline, documented labeling policy, iteration planned. 🔴 Workflow 11's four-category classifier has no equivalent eval suite yet — its accuracy is currently assumed, not measured. | Build an 11b eval suite mirroring 09b's methodology for workflow 11's classifier. |
| 10 | **Version control** | Workflow JSONs live in git with meaningful history. | ✅ This repository. | — |
| 11 | **Documentation & handoff** | A colleague could understand, run and maintain the workflow from the docs alone. | ✅ Per-workflow READMEs (use case, build notes, node tables, screenshots, known limitations) maintained through workflow 14. 🟡 No operational runbook (who reacts to what, when) yet — relevant now that workflow 12 has a real human-in-the-loop step. | Add a lightweight runbook for workflow 12's approval step (who decides, expected turnaround, escalation if nobody responds). |
| 12 | **Honest scope decisions** | What is deliberately *not* built is documented, not hidden. | ✅ Known limitations stated in READMEs (e.g. workflow 10's duplicate-task bug and fix, workflow 11's test-webhook-only trigger); this checklist itself. | — |

**Legend:** ✅ implemented · 🟡 partially implemented · 🔴 not yet — planned

*This is a living document. The point is not a perfect scorecard — it is
knowing exactly where the gaps are before someone else finds them.*
