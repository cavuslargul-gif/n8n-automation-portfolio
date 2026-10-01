# 13 – Cross-Domain: Central Error Handler with Audit Log

## Use Case
A single, reusable error handler shared across the entire portfolio of admin workflows (10, 11, 12, and others). Instead of each workflow building its own error notification logic, every workflow points to this one in its settings (Settings → Error Workflow) — any unhandled error anywhere gets caught here and written to a central audit log, with no workflow-specific code required.

## Workflow
Error Trigger → Write to Error Log (Data Table)

<!-- Canvas screenshot goes here -->

## How it was built
- **Error Trigger** is n8n's built-in trigger that fires automatically whenever a workflow configured to use this one as its "Error Workflow" fails — no manual wiring inside the failing workflow itself beyond that one settings field
- **Data Table** node writes one row per failure to a shared `workflow_error_log` table: timestamp, the name of the workflow that failed, the node that failed (or the last node executed, as a fallback), the error message, and the execution ID for direct lookup in n8n's execution history

## How it works
1. Any workflow with this one set as its Error Workflow fails during execution
2. n8n automatically triggers this workflow and passes the full error context (which workflow, which node, what message, which execution)
3. A log entry is written immediately — no delay, no dependency on the failing workflow still being able to run code
4. The failed workflow's own downstream logic (digest emails, task creation, etc.) is unaffected — it simply stops at the point of failure while this workflow independently records what happened

## Nodes & Tools

<!-- Node list screenshot goes here -->

- n8n Error Trigger
- n8n Data Table

## Background
Centralizing error handling this way means every admin workflow gets consistent, structured failure logging for free, just by pointing to one shared workflow — instead of each one needing its own try/catch-equivalent logic. This is also what makes the "Error-Handling" notes in workflows 10, 11, and 12 true in practice: each of them mentions being coupled to a central error handler, and this is that workflow. The audit log itself (`workflow_error_log`) is the same data table read by workflow 10's daily/weekly digest, so unresolved errors surface in the regular admin overview rather than only existing in n8n's internal execution history.
