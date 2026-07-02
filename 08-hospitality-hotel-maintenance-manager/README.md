# 08 – Hospitality: Hotel Maintenance Manager

## Use Case
Digitizes maintenance reporting in hotels — staff submit issues via form, the system logs them automatically in Notion and notifies the team via Slack.

## Workflow
Maintenance Report Form → Log to Notion Database → Slack Notification

<img width="953" height="519" alt="image" src="https://github.com/user-attachments/assets/cbcd155c-cb70-4617-8536-608bcab9104c" />


## How it was built
- ### n8n Form Trigger with fields:
  room number (Number), problem category (Dropdown: Elektrik, Sanitär, Möbel, Sonstiges), priority (Dropdown: Niedrig, Mittel, Hoch), description (Textarea) Auto-generated Vorgangsnummer (ticket ID) in format WM-{room}-{category} — e.g. WM-302-Elektrik — built directly from form data, no manual input required
- ### Notion Database as central maintenance log with columns:
  Vorgangsnummer (Title), Zimmernummer (Number), Problemkategorie (Select), Priorität (Select), Beschreibung (Text), Status (Select: Offen → In Bearbeitung → Erledigt)
- ### Slack Bot (n8n-maintenance-bot):
  posts to #wartungsstatus-maintenance with all relevant details and a direct link to the Notion entry

## How it works
1. A staff member submits the form — room number, category, priority, and description
2. n8n generates a unique ticket ID (WM-302-Elektrik) and creates a new entry in the Notion database
3. The maintenance team receives an instant Slack notification with all details and a direct Notion link
4. The technician updates the Status field in Notion directly (Offen → In Bearbeitung → Erledigt)
5. Management views the full status overview in Notion — filterable by status, room, or category
   
Nodes

<img width="637" height="237" alt="image" src="https://github.com/user-attachments/assets/3d9e7877-3dd4-468c-b816-620f9955a704" />

## Tools
- n8n Form Trigger
- Notion Database (OAuth2)
- Slack Bot API

## Background
Designed for hotels with multiple rooms and departments. The auto-generated ticket ID (WM-{room}-{category}) makes it easy to track and reference issues without manual numbering. Status management stays in Notion — the team updates it directly without needing access to n8n. Built for GDPR-compliant internal use: no external ticketing system, data stays within the organization's own Notion workspace.
