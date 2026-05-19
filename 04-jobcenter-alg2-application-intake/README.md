# 04 – Jobcenter: ALG II Application Intake

## Use Case
Automates the intake of new ALG II (Bürgergeld) applications at a Jobcenter. When a client submits the online form, their data is automatically logged in Google Sheets and they receive an email confirmation.

## Workflow
Form submission → Google Sheets (logging) → Gmail (confirmation)

## How it was built
- Trigger: n8n Form Trigger (no external auth required)
- Google Sheets connected via OAuth2
- Gmail connected via OAuth2
- Nodes connected in sequence on the n8n canvas
- Tested end-to-end with live form submission

## How it works
1. Client submits the online application form (first name, last name, date of birth, household type)
2. Data is automatically written to Google Sheets as a new row
3. Client receives an email confirmation that their application has been received
4. Staff can monitor all incoming applications directly in the Google Sheet

## Tools
- n8n Form Trigger
- Google Sheets
- Gmail

## Background
Based on real experience as a Fachassistentin at a German Jobcenter processing ALG II applications. The household type (Bedarfsgemeinschaft) is a key field in German social welfare law — it determines benefit amounts and eligibility. In practice this process runs in SAP; this workflow simulates the intake logic using n8n-native tools.
