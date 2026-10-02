# 13 – Cross-Domain: Central Error Handler with Audit Log

## Use Case
A single, reusable error handler shared across the entire portfolio of admin workflows (10, 11, 12, and others). Instead of each workflow building its own error notification logic, every workflow points to this one in its settings (Settings → Error Workflow) — any unhandled error anywhere gets caught here and written to a central audit log, with no workflow-specific code required.

## Workflow
Error Trigger → Write to Error Log (Data Table)

<img width="483" height="678" alt="image" src="https://github.com/user-attachments/assets/0acdd036-c8db-4d5d-a3f2-825ec5f25b82" />

## How it was built
- **Error Trigger** is n8n's built-in trigger that fires automatically whenever a workflow configured to use this one as its "Error Workflow" fails — no manual wiring inside the failing workflow itself beyond that one settings field
- **Data Table** node writes one row per failure to a shared `workflow_error_log` table: timestamp, the name of the workflow that failed, the node that failed (or the last node executed, as a fallback), the error message, and the execution ID for direct lookup in n8n's execution history
- Three more columns — `status` (defaults to "offen"), `retry_count` (defaults to 0), and `workflow_id` — turn the audit log into an actual dead-letter queue: a separate workflow (13b) can find open failures and retry the right workflow programmatically

## How it works
1. Any workflow with this one set as its Error Workflow fails during execution
2. n8n automatically triggers this workflow and passes the full error context (which workflow, which node, what message, which execution)
3. A log entry is written immediately — no delay, no dependency on the failing workflow still being able to run code
4. The failed workflow's own downstream logic (digest emails, task creation, etc.) is unaffected — it simply stops at the point of failure while this workflow independently records what happened

## Nodes & Tools

- n8n Error Trigger
- n8n Data Table

## Background
Centralizing error handling this way means every admin workflow gets consistent, structured failure logging for free, just by pointing to one shared workflow — instead of each one needing its own try/catch-equivalent logic. This is also what makes the "Error-Handling" notes in workflows 10, 11, and 12 true in practice: each of them mentions being coupled to a central error handler, and this is that workflow. The audit log itself (`workflow_error_log`) is the same data table read by workflow 10's daily/weekly digest, so unresolved errors surface in the regular admin overview rather than only existing in n8n's internal execution history.

## Dead-Letter Queue & Replay (13b)

A separate workflow (`13b-error-handler-replay.json`) extends this log into an actual dead-letter queue: it reads every row where `status = offen`, re-runs the originally-failed workflow by `workflow_id`, and marks the row `wiederholt` with an incremented `retry_count` on success. A failed replay attempt is caught (not silently dropped) and leaves the row open for the next run.

**Verified, not just built:**
- A row with an empty/invalid `workflow_id` (e.g. an older log entry from before this column existed, or a since-deleted target workflow) is caught by the Execute Workflow node's error branch instead of crashing the whole replay run — tested directly with a known-bad payload.
- That same test uncovered a real bug: the error branch wasn't wired back into the batch loop, so one failed replay silently stopped the entire run before it reached any later rows. Fixed by connecting the error output back to the loop node — confirmed with a second run that a failing row no longer blocks the rows after it.
- A real happy-path replay (re-running eval suite 11b end-to-end) completed and correctly flipped the row to `wiederholt`. It also surfaced a separate, honestly-documented limitation: 11b's own Groq request-batching/pause logic isn't respected when it's invoked as a sub-workflow via Execute Workflow — all 25 requests fired close together instead of paced. It happened to stay under Groq's free-tier rate limit this time; it isn't guaranteed to.

**Known limitation — replay is not payload replay.** n8n's Error Trigger never receives the original input data of the failed run, only workflow/node/error metadata. Replay here means "re-trigger the workflow," not "reprocess the exact request that failed." For schedule-triggered workflows (10, 12, 15) that's meaningful — the next run picks up the current data again. For webhook-triggered workflow 11, the specific customer inquiry that failed can't be reconstructed this way; the sender would need to submit again.

**Kept deliberately simple (v1):** no retry cap, no backoff between replay attempts, and a failed replay is just skipped rather than escalated. A real production version would add a max-retry counter before giving up on a row permanently.
