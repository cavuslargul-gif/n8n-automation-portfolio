# 01 – Public Administration: Project Request Intake

## Use Case
Automates incoming project requests in a public administration context.

## Workflow
Form submission → Google Sheets (logging) → Gmail (confirmation)

<img width="737" height="397" alt="image" src="https://github.com/user-attachments/assets/93326e17-2ed7-4b28-981b-d922a8dc516b" />

## How it was built
- Trigger: n8n Form Trigger (no external auth required)
- Google Sheets connected via OAuth2
- Gmail connected via OAuth2
- Nodes connected in sequence on the n8n canvas
- Tested end-to-end with live form submission

## How it works
1. User fills out the n8n form (project name, applicant, priority)
2. On submission, data is written to Google Sheets as a new row
3. A confirmation email is automatically sent via Gmail

## Tools
- n8n Form Trigger
- Google Sheets
- Gmail

## Background
Based on real project management experience in German public administration.
