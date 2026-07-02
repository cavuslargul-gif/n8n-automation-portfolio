# 07 – AI & Education: AI Content Generator



## Use Case
Automatically generates platform-specific social media posts and newsletter drafts using AI — based on topic, target audience, tone, and platform. Designed for solopreneurs, content creators, and small businesses who want to produce consistent content without manual writing.


## Workflow
Form submission → OpenAI (content generation) → Switch (platform routing) → Gmail (generated content delivered by email)

<img width="1043" height="591" alt="image" src="https://github.com/user-attachments/assets/01fe73d9-22f0-4c0d-b5e8-f723d28d14ec" />


## How it was built
- Trigger: n8n Form Trigger with four fields (topic, target audience, tone, platform)
- OpenAI node (GPT-4o-mini) with a two-message setup: system prompt defining the role, user prompt injecting all four form variables dynamically
- Prompt engineering for platform-specific output: LinkedIn (150–200 words, professional, 3–5 hashtags), Instagram (50–80 words, emotional, emojis and hashtags), Newsletter (subject line + body, 200–250 words)
- Switch node in Rules mode routing based on the selected platform (LinkedIn / Instagram / Newsletter)
- Three Gmail nodes connected via OAuth2, one per platform with tailored subject lines
- Error handling configured on the OpenAI node (Continue using error output) with a dedicated Fehlerbericht Gmail node
- Tested end-to-end with all three platforms and multiple topics
  

## How it works
1. User submits the form with topic, target audience, tone, and platform
2. OpenAI generates platform-appropriate content in German based on all four inputs
3. The Switch node routes to the matching branch based on the selected platform
4. The generated content is sent via email with a platform-specific subject line
5. If the OpenAI API fails, a Fehlerbericht email is sent automatically instead


## Tools
- n8n Form Trigger
- OpenAI Node (Message a Model / GPT-4o-mini)
- Switch Node (Rules mode, 3 outputs)
- Gmail (×4: LinkedIn, Instagram, Newsletter, Fehlerbericht)
- Error Handling (Continue using error output)


## Background
Built to demonstrate AI-powered content generation for the German freelance and solopreneur market. Content creation is one of the most time-consuming tasks for small businesses — this workflow replaces manual writing with a structured AI prompt that adapts to platform requirements and audience, making it directly sellable as a service on platforms like Upwork or Fiverr.

