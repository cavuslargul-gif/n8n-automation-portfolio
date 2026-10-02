# 03 – Jobcenter: Appointment Routing by Age

## Use Case
Automates the intake and internal routing of new clients registering for an employment consultation appointment at a Jobcenter. Based on the client's date of birth, the system routes them to the appropriate department (U25 youth services or standard employment services) — without the client being aware of the internal logic.

## Workflow
Form submission → Normalize date of birth → Valid? (IF) → Age check (IF, under 25?) → Gmail (confirmation email) · invalid dates → Gmail (manual review)

<p align="center">
<img width="961" height="661" alt="image" src="https://github.com/user-attachments/assets/7585e51d-06bb-40f9-a71c-b36f2e00caed" />
</p>

## How it was built
- Trigger: n8n Form Trigger (no external auth required), date of birth as a date field
- Set node parses the date of birth explicitly, day first as is standard in German-speaking countries (`d.M.yyyy`, `d/M/yyyy`, or `yyyy-MM-dd`), into one ISO format; anything unreadable, non-existent (31.02.), in the future, or before 1900 becomes empty
- IF node ("valid?") sends empty/invalid values to a manual-review email instead of letting the age check run on them
- IF Node with date comparison: normalized date of birth is after `$now.minus(25, 'years')`
- Gmail connected via OAuth2
- Three Gmail nodes — one per branch (under 25, over 25) plus the manual-review notification
- Connected to the central error handler (workflow 13) via the Error Workflow setting
- Tested end-to-end with both U25 and Ü25 test cases, then against deliberately bad input (see below)

## How it works
1. Client submits the online registration form (first name, last name, date of birth, work capacity)
2. The date of birth is normalized; if it can't be read reliably, staff get a "manual review" email with the raw value and the case stops there
3. Otherwise the IF Node checks whether the client is under 25
4. If yes (TRUE) → confirmation email sent, internally routed to youth services (U25)
5. If no (FALSE) → confirmation email sent, internally routed to standard employment services
6. The client always receives the same neutral confirmation — internal routing is invisible

**Known-bad-payload test (found and fixed):** The first version compared the raw form text field against a cutoff date. Testing with deliberately bad input surfaced two problems:
- An empty or unreadable date of birth (`""`, `letzten Sommer`) made the IF node crash outright — no fallback, no email, nothing for staff to act on.
- A more dangerous one: the ambiguous German date `05.10.2001` was read with day and month swapped (10 May instead of 5 October) and silently routed to "over 25" although the person is still 24. No error, just a wrong department.

The fix is explicit parsing instead of letting n8n guess, plus a review branch for anything it can't read. Re-verified with real cases: the ambiguous boundary date now routes to under 25, an empty value, free text, a future date (`2031-01-01`) and a non-existent one (`31.02.2000`) all land in manual review, and a plain German-format date (`12.05.1990`) still routes to over 25. A third, smaller bug showed up while extending this: the first fix required two-digit days, so the very common `5.10.2001` was wrongly rejected — it now parses with or without a leading zero, and `5/10/2001` is read day-first too. The key cases (boundary date, no leading zero, empty, free text) were also re-run against the published workflow in production mode, not only as manual test runs. The form field is now a date picker as well, so real users rarely hit the review path — the validation covers submissions that bypass the form UI.

## Tools
- n8n Form Trigger
- n8n Set / Edit Fields
- IF Node
- Gmail

## Background
Based on real experience as a Fachassistentin at a German Jobcenter. New clients registering for unemployment benefits were automatically assigned to either the U25 youth department or the standard Arbeitsvermittlung — the routing happened internally without client input. This workflow simulates that logic using n8n-native tools as a stand-in for the SAP-based systems used in practice.
