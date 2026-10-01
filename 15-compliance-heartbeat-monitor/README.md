# 15 – Cross-Domain: Heartbeat Monitor for Daily Admin Run

## Use Case
Catches the one failure mode the central error handler (#13) structurally cannot: a workflow that doesn't fail, it just doesn't run — a disabled trigger, a deactivated workflow version, a schedule that silently stopped. The Error Trigger in #13 only fires on an actual execution failure, so a missing run produces no error at all, just silence. This workflow checks for that silence directly.

## Workflow
Schedule Trigger (daily 8:00) → Query Today's Heartbeat (Data Table) + constant Marker item, merged (append) → Evaluate (Code) → Heartbeat Missing? (IF) → Alert Email (only if missing)

<img width="1208" height="773" alt="image" src="https://github.com/user-attachments/assets/1598dc98-7409-4cca-ba4d-abf50e6ac878" />

## How it was built
- **Schedule Trigger** runs daily at 8:00 — deliberately one hour after workflow 10's 7:00 trigger, giving its daily chain time to complete
- Workflow 10 was extended with one additional node at the end of its daily chain: a **Data Table insert** into a new `heartbeat_log` table (timestamp + workflow name), written right after the daily digest email sends successfully
- **Data Table** (`get`) queries `heartbeat_log` for any row with today's timestamp
- A parallel **Set** node ("Marker") always emits exactly one item, regardless of the query result
- **Merge** (`append` mode) concatenates both branches — guaranteeing at least one item downstream even when the query found nothing
- **Code** node checks whether any item in the merged list carries a real `zeitstempel` field
- **IF** routes to the alert only when none does
- **Gmail** sends the alert, naming the possible causes

## How it works
1. Every day at 8:00, this workflow checks whether workflow 10 already proved it ran today
2. If workflow 10's heartbeat row is there, nothing happens — the expected, healthy case
3. If it's missing, an alert goes out immediately, rather than someone noticing days later that no digest emails have arrived

**Why this is separate from workflow 13:** #13 is reactive — it catches errors *during* execution. This one is a presence check — it catches the *absence* of an execution entirely, which produces no error event for #13 to react to in the first place.

**Known limitation (found and fixed during testing — kept here deliberately):** The first version queried `heartbeat_log` directly and branched on "0 rows returned." That broke in exactly the case it was built to catch: n8n skips downstream nodes entirely when a node outputs 0 items, so the empty-table case killed the execution chain *before* the IF or the alert ever ran — the monitor was silent exactly when it needed to speak. `alwaysOutputData` on the query node didn't fix it either (it has no effect on this node type with zero matches). The fix: a constant marker item is merged in alongside the query result with `append` mode, so the chain always carries at least one item regardless of what the query finds — then a Code node explicitly checks for a real timestamp among them. Verified against both real outcomes (table empty → alert sent, confirmed via Gmail's `SENT` response; table has today's row → no alert), not just a clean one.

## Nodes & Tools
- n8n Schedule Trigger
- n8n Data Table
- n8n Set
- n8n Merge
- n8n Code
- n8n IF Node
- Gmail (OAuth2)

## Background
A digest workflow that silently stops is worse than one that fails loudly — nobody gets paged, the inbox is simply emptier than usual, and by the time it's noticed, days of dunning cases, errors, and appointments may have gone unreviewed. This closes that specific gap for workflow 10 with the smallest possible addition on its side: one extra write. The monitor itself ended up needing more care than expected — n8n's zero-item behavior is a sharp edge worth knowing about before relying on "0 results" as a signal anywhere else in this portfolio.
