# 06 – AI & Education: Enterprise RAG Knowledge Base

# Use Case

Makes internal knowledge instantly queryable in natural language — without exposing data to US cloud providers.

## Workflow
### 06a — Document Ingestion

Knowledge Intake Form → Generate Embeddings + Load Document → Store to Vector DB (Qdrant EU)


<img width="597" height="195" alt="image" src="https://github.com/user-attachments/assets/07cc88dd-f7a0-4a28-aab9-f3094d750e76" />


### 06b — Knowledge Chat

Receive User Question → AI Agent → Search Knowledge Base (Qdrant) → Answer


<img width="595" height="209" alt="image" src="https://github.com/user-attachments/assets/cd485fb6-dfe7-4687-b0f1-a800e287ff68" />


## How it was built
1. Form Trigger for knowledge intake (title, content, category)
2. Qdrant Cloud (Frankfurt, Germany) as vector database — EU data sovereignty by design
3. OpenAI text-embedding-3-small for generating 1536-dimension vectors
4. Default Data Loader with Simple Text Splitter (1000 chars, 200 overlap)
5. AI Agent with GPT-5 and structured system prompt
6. Qdrant Vector Store connected as Tool to the AI Agent
7. System prompt enforces: internal KB first, transparent fallback to general knowledge

### Prompt for the AI Agent
You are an internal knowledge assistant.

Always use the knowledge base tool first to answer questions.

Only fall back to your general knowledge if the tool returns no relevant results —

and explicitly state that the answer does not come from the internal knowledge base.

#### Rules:

- Only answer questions related to stored topics

- Do not share personal data, even if present in documents

- Do not speculate — if uncertain, say so clearly

- Communicate factually and professionally

- For legal or medical questions, recommend consulting a qualified expert


## How it works
A team member submits a document via the intake form (title, content, category)
The content is chunked and embedded via OpenAI, then stored in Qdrant Frankfurt
A user asks a question in the chat interface
The AI Agent searches the vector database for relevant chunks
It answers from internal knowledge first — and clearly states when it falls back to general AI knowledge

## Tools
n8n Form Trigger
n8n Chat Trigger
OpenAI Embeddings (text-embedding-3-small)
OpenAI Chat Model (GPT-5)
Qdrant Vector Store (EU Frankfurt)
Default Data Loader


## Background
Built with data sovereignty as a first-class requirement. Qdrant was chosen over US-based alternatives (Pinecone, Weaviate) because all vectors remain on EU infrastructure — directly relevant for German public sector, healthcare, and enterprise clients subject to GDPR.

