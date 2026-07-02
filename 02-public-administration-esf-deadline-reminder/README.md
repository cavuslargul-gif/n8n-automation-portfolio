# 02 – Public Administration: ESF Deadline Reminder

## Use Case
Automatically reminds project participants to submit their ESF reports 
before the deadline — based on real workflow from ESF-funded projects 
in German public administration.

## Workflow
Schedule Trigger (daily 8am) → Google Sheets (read participants) → IF (deadline within 7 days) → Gmail (reminder email)

<img width="685" height="395" alt="image" src="https://github.com/user-attachments/assets/740c68e5-b6cc-4c95-a27a-1d64521f7dcd" />

## How it was built
- Schedule Trigger configured for daily execution at 8am
- Google Sheets connected via OAuth2
- IF Node with date comparison (is before or equal to now + 7 days)
- Gmail connected via OAuth2
- Tested end-to-end with live data

## How it works
1. Every morning at 8am the workflow runs automatically
2. It reads all participants and deadlines from Google Sheets
3. For each row it checks if the deadline is within 7 days
4. If yes — a personalized reminder email is sent automatically
5. If no — nothing happens

## Tools
- n8n Schedule Trigger
- Google Sheets
- IF Node
- Gmail

## Background
Based on real project management experience coordinating ESF-funded 
projects in German public administration, where report deadlines 
were critical for funding compliance.
