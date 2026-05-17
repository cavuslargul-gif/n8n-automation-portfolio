# 03 – Jobcenter: Appointment Routing by Age

## Use Case
Automates the intake and internal routing of new clients registering for an employment consultation appointment at a Jobcenter. Based on the client's date of birth, the system routes them to the appropriate department (U25 youth services or standard employment services) — without the client being aware of the internal logic.

## Workflow
Form submission → IF (date of birth after cutoff = under 25?) → Gmail (confirmation email)

## How it was built
- Trigger: n8n Form Trigger (no external auth required)
- IF Node with date comparison: date of birth is after `$now.minus(25, 'years')`
- "Convert types where required" enabled for date string comparison
- Gmail connected via OAuth2
- Two separate Gmail nodes — one per branch (true/false)
- Tested end-to-end with both U25 and Ü25 test cases

## How it works
1. Client submits the online registration form (first name, last name, date of birth, work capacity)
2. The IF Node checks whether the client is under 25
3. If yes (TRUE) → confirmation email sent, internally routed to youth services (U25)
4. If no (FALSE) → confirmation email sent, internally routed to standard employment services
5. The client always receives the same neutral confirmation — internal routing is invisible

## Tools
- n8n Form Trigger
- IF Node
- Gmail

## Background
Based on real experience as a Fachassistentin at a German Jobcenter. New clients registering for unemployment benefits were automatically assigned to either the U25 youth department or the standard Arbeitsvermittlung — the routing happened internally without client input. This workflow simulates that logic using n8n-native tools as a stand-in for the SAP-based systems used in practice.
