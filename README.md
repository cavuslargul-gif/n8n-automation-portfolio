# n8n-Automation-Portfolio
n8n workflow automations covering real business processes — plus reusable compliance and error-handling patterns that apply across all of them

## About me
I'm a career changer with a background spanning public administration, 
employment services, retail management, education (M.Ed.) and hospitality. 
Each workflow in this portfolio reflects one of those domains — this is not 
a generic tutorial portfolio, every automation solves a problem I've 
encountered in practice.

## Workflows

| # | Domain | Use Case | Tools |
|---|--------|----------|-------|
| 01 | Public Administration | Project request intake | n8n Form, Google Sheets, Gmail |
| 02 | Public Administration | ESF Deadline Reminder | Schedule Trigger, Google Sheets, IF Node, Gmail |
| 03 | Jobcenter | Appointment Routing by Age | n8n Form, IF Node, Gmail |
| 04 | Jobcenter | ALG II Application Intake | n8n Form, Google Sheets, Gmail |
| 05 | AI & Education | AI Learning Request Routing | n8n Form, OpenAI, Switch Node, Gmail |
| 06a | AI & Education | Enterprise RAG – Document Ingestion | n8n Form Trigger, Default Data Loader, OpenAI Embeddings, Qdrant |
| 06b | AI & Education | Enterprise RAG – Knowledge Chat | n8n Chat Trigger, AI Agent, OpenAI GPT-5, Qdrant |
| 07 | AI & Education | AI Content Generator | n8n Form, OpenAI, Switch Node, Gmail |
| 08 | Hospitality | Hotel Maintenance Manager | n8n Form Trigger, Notion, Slack |
| 09a | Hospitality | Guest Feedback Analysis | n8n Form, OpenAI, Switch Node, Gmail |
| 09b | Hospitality | Sentiment Eval Suite (for 09) | Manual Trigger, Google Sheets, OpenAI |
| 10 | Retail | Dunning Management with Admin Overview | Schedule Trigger, Google Calendar, n8n Data Table, Aggregate, Merge, Gmail, Google Tasks |
| 11 | Retail | AI Customer Inquiry Routing | n8n Webhook, Basic LLM Chain, Groq Chat Model, Set, Gmail, Data Table |

## Cross-Domain: Compliance & Error Handling

Workflows that don't belong to one specific domain — they sit underneath or alongside the domain workflows above.

| # | Topic | Use Case | Tools |
|---|-------|----------|-------|
| 12 | Compliance & Error Handling | Dunning Approval with Human-in-the-Loop and Audit Trail | Schedule Trigger, n8n Data Table, Gmail Send-and-Wait, IF Node, Set |
| 13 | Compliance & Error Handling | Central Error Handler with Audit Log | n8n Error Trigger, n8n Data Table |
| 14a/14b | Compliance & Error Handling | Error Handling Main/Sub Pattern | Schedule Trigger, Set, Stop and Error, Error Trigger |
| 15 | Compliance & Error Handling | Heartbeat Monitor for Daily Admin Run | Schedule Trigger, n8n Data Table, Set, Merge, Code, IF Node, Gmail |

**Note on error handling:** Workflows 13 and 14 cover error handling in depth — a central audit-log 
handler (13) and an alternative Main/Sub extraction pattern (14). Workflows 05, 07 and the 09 eval 
suite (09b) additionally implement inline continue-on-error handling with dedicated notification 
emails for that specific use case.

## Methodology: Worksheets & Checklists

The [`worksheets/`](worksheets) folder holds the methodology behind these workflows — project 
lifecycle, AI-node error handling, logging/observability architecture, and rollout checklists, 
written up as standalone, reusable reference documents rather than left implicit in the workflow 
JSONs.
