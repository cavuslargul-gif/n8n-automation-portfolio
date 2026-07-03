# n8n-Automation-Portfolio
n8n workflow automations across 6 domains — public administration, education, retail, hospitality management and AI

## About me
I'm a career changer with a background spanning public administration, 
employment services, retail management, education (M.Ed.) and hospitality. 
This diverse experience shapes how I think about automation — I understand 
the real processes behind the workflows I build.

## Why 6 domains?
Each workflow reflects a domain I've worked in professionally. 
This is not a generic tutorial portfolio — every automation solves 
a problem I've encountered in practice.

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
| 09 | Hospitality | Guest Feedback Analysis | n8n Form, OpenAI, Switch Node, Gmail |
| 10 | Retail | coming soon | — |
| 11 | Retail | coming soon | — |


**Note on error handling:** Error handling is implemented exemplarily in workflows 05, 07 and the 09 eval suite (09b)
(Continue-on-error with dedicated error notification emails). The remaining workflows focus on core 
process logic — a deliberate scope decision for this portfolio. Error workflows are covered in depth 
in n8n Course Level 2 (certified: [community.n8n.io/u/guel](https://community.n8n.io/u/guel)).
