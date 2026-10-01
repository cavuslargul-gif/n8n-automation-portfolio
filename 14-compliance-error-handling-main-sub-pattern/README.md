# 14 – Cross-Domain: Error Handling Main/Sub Pattern

## Use Case
A reusable Main/Sub error-handling pattern: a dedicated "sub" workflow that only extracts structured error information (message, failed workflow, last node) whenever triggered by n8n's Error Trigger, kept separate from the business logic. The "main" workflow included here is a minimal test harness that intentionally fails on a schedule, so the pattern can be demonstrated and verified without needing a real production failure. Shown as an alternative to the single-workflow error handler in #13 — same underlying n8n mechanism (Error Workflow setting → Error Trigger), different structure.

## Workflow
**14a (Main, test harness):** Schedule Trigger → Mock Order (Set) → Simulate Failure (Stop and Error)

<img width="819" height="453" alt="image" src="https://github.com/user-attachments/assets/8de127ee-cb23-4b44-bd8d-51605eba35ee" />

**14b (Sub, the actual pattern):** Error Trigger → Extract Error Info (Set)

<img width="816" height="456" alt="image" src="https://github.com/user-attachments/assets/08afabf4-35de-417a-b8be-b71e10a510a8" />

## How it was built
- **14a** runs every 5 minutes, builds a fake order record (`customer_id`, `action`, `amount`) with a Set node, and then deliberately stops with a hardcoded error ("Payment processing failed: gateway timeout") via the Stop and Error node — purely to produce a reliable, repeatable failure for testing
- **14b** is configured as 14a's Error Workflow. Its Error Trigger fires automatically on any failure in 14a and receives n8n's full error payload
- A Set node in 14b extracts the three fields that matter for downstream use — `error_message`, `failed_workflow`, `last_node` — into a flat, easy-to-consume structure

## How it works
1. 14a fails on a fixed schedule (simulated failure, not a real one)
2. n8n automatically invokes 14b as the configured Error Workflow
3. 14b extracts the relevant error fields into a clean, flat object
4. From here, the extracted fields could feed any downstream action — a notification, a log entry, a ticket — without that logic needing to know anything about n8n's raw error payload shape

**Why this is here as a separate entry from #13:** #13 is the error handler actually wired into this portfolio's production workflows (10, 11, 12) — it writes straight to an audit log table. This pattern is a more general-purpose building block: separating "extract the error" from "do something with the error" so the extraction step can be reused regardless of what happens next (log it, alert on it, retry it). Both are valid approaches; which one fits depends on how many different things need to happen with a failure.

## Nodes & Tools
- n8n Schedule Trigger
- n8n Set / Edit Fields
- n8n Stop and Error
- n8n Error Trigger

## Background
Demonstrates the Main/Sub split as an n8n error-handling architecture choice, tested with simulated data rather than a specific client process — the pattern itself, not a business case, is the point of this entry.
