# 05 – Education: AI Learning Request Routing.md

## Use Case
Automatically classifies incoming learning requests by skill level using AI and sends personalized resource recommendations via email — designed for educational providers, online courses, or internal training programs.
Workflow
Form Trigger → OpenAI (AI classification) → Switch (3-way routing) → Gmail (personalized recommendations) + Gmail (error notification)

## How it was built
Form Trigger configured with three fields: name, learning topic, and self-assessment (Anfänger / Fortgeschritten / Experte)
OpenAI node connected via API to classify requests using GPT-4o-mini
Switch node in Rules mode routing to three separate branches based on AI output
Three Gmail nodes connected via OAuth2, each with level-specific resource recommendations
Error handling configured on the OpenAI node (Continue using error output) with a dedicated Fehlerbericht Gmail node
Tested end-to-end with all three routing paths

## How it works
A learner submits their request via the form (name, topic, self-assessment)
OpenAI analyzes the topic and self-assessment and returns one word: Anfänger, Fortgeschritten, or Experte
The Switch node routes the request to the matching branch
A personalized email with level-appropriate resources is sent automatically
If the OpenAI API fails, a Fehlerbericht email is sent instead

## Tools
n8n Form Trigger
OpenAI Node (Message a Model / GPT-4o-mini)
Switch Node (Rules mode, 3 outputs)
Gmail (×4: Anfänger, Fortgeschrittene, Experten, Fehlerbericht)
Error Handling (Continue using error output)

## Background
Built to demonstrate AI-powered routing in an educational context. The workflow simulates how training providers or HR departments could automatically match learners to the right resources without manual triage — using AI classification instead of simple keyword matching.

