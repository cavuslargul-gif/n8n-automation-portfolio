# 10 - Dunning Management with Admin Overview

## Use Case
Automates the daily and weekly status digest for craft/trade businesses: open appointments, technical workflow errors, and deferred dunning cases (overdue invoices put on hold) are collected and emailed to management. New cases are also automatically turned into a Google Task — with built-in duplicate protection so the same deferred case doesn't spawn a new task every day.

## Workflow
Two independent chains in the same workflow — Daily (7:00) and Weekly (Monday, 7:00) — pull appointments (Google Calendar), errors (Data Table) and dunning cases (Data Table), aggregate/merge them, and send a summary email (Gmail). The daily chain additionally creates Google Tasks for new errors and new deferred dunning cases.

<img width="1516" height="797" alt="image" src="https://github.com/user-attachments/assets/7b240844-3947-463a-aafc-a1ab09e87366" />

## How it was built
- **Schedule Trigger** (daily 7:00, weekly Monday 7:00) — two fully separate chains instead of one shared path, to avoid fragile cross-references between time ranges (only one trigger ever fires per execution)
- **Google Calendar** (Get Many) collects appointments for the respective time range
- **n8n Data Table** (`workflow_error_log`) returns error log entries from the last 24h / 7 days
- **n8n Data Table** (`offene_posten`) returns deferred dunning cases; the daily path additionally filters on `task_erstellt = false` so already-processed cases don't reappear
- **Aggregate** nodes collapse appointments/errors/dunning cases per branch into a single record, **Merge** combines both branches for the email
- **Gmail** sends a plain-text summary with all three lists (fallback: "None" shown when a list is empty)
- **Google Tasks** creates one task per new error and per new deferred dunning case, in parallel
- A dedicated **Data Table update node** sets the `task_erstellt = true` flag right after task creation, keyed on the invoice number — prevents the same case from creating another task the next day

## How it works
1. The trigger (daily 7:00 or weekly Monday 7:00) starts the respective chain
2. Appointments, errors, and deferred dunning cases are pulled from Google Calendar and the data tables
3. For new errors and new deferred dunning cases (daily chain only), a Google Task is created automatically
4. The `task_erstellt` flag is set to `true` right after — prevents duplicates on future runs
5. All three lists are merged into one summary email and sent to management via Gmail

**Note:** The duplicate-protection logic (`task_erstellt` flag) was added after testing surfaced that the daily run created a new task every day for the same already-deferred case — the original filter only checked status, with no time or processing window.

**Known limitation:** Error-handling (unhandled exceptions, routed to workflow 13) and this workflow's own fallback logic (e.g. showing "None" instead of breaking when a list is empty) are two different layers — the fallback keeps a run from crashing on expected edge cases, error-handling catches what the fallback doesn't cover. Replay (workflow 13b) only applies to the latter, and even there it re-triggers this workflow rather than reprocessing a specific failed payload — meaningful here since this workflow re-queries Google Calendar and the data tables fresh on every run anyway.

## Nodes & Tools
- n8n Schedule Trigger
- Google Calendar (OAuth2)
- n8n Data Table
- n8n Aggregate / Merge
- Gmail (OAuth2)
- Google Tasks (OAuth2)

## Background
Built for craft/trade businesses that don't want to check dunning status, appointments, and technical errors across three separate systems. Deferred dunning cases — e.g. due to a payment plan or an open customer inquiry — need active follow-up instead of quietly being forgotten. Automatic task creation with duplicate protection ensures every case becomes visible exactly once, not re-surfaced daily. Pure information workflow: no automatic customer-facing or billing actions, no payment triggers.
