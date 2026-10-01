# Worksheets & Checklists

Eigenständige Arbeitspapiere aus dem Selbststudium (Stand: Juli 2026) — die Methodik hinter den Workflows in diesem Portfolio. Während die nummerierten Ordner zeigen, *was* gebaut wurde, zeigen diese Dokumente *wie* ich an ein KI-Automatisierungsprojekt herangehe: von der ersten Analyse über Governance, Architektur und gestuften Rollout bis zum Betrieb.

## Einzeldokumente (nutzbar und editierbar als eigenständige Checklisten)

- **`Arbeitsprobe_Projekt-Worksheet_Guel_Cavuslar.pdf`** — Sieben-Phasen-Projektlebenszyklus (Analyse → Governance → Architektur → Implementierung → Test → Rollout → Betrieb), inkl. GitHub-Repository-Struktur für Projektdokumentation
- **`Arbeitsprobe_Fehlerbehandlung_n8n_1.pdf`** — Checkliste und Entscheidungslogik für Fehlerbehandlung in produktiven AI-Nodes: fünf Fallback-Strategien (Error Handling, Model Fallback, Human in the Loop, Alternativworkflow, Fallback auf gespeicherte Daten)
- **`Arbeitsprobe_Logging_Architektur_Guel_Cavuslar.pdf`** — Observability- und Logging-Architektur: Log-Typen nach Zweck getrennt (Execution, Error, Business, Audit Trail, AI Log, Security Log), was nie im Klartext gespeichert wird, DSGVO- und EU-AI-Act-Bezug
- **`Arbeitsprobe_Rollout-Checkliste_Guel_Cavuslar.pdf`** — Vierstufige Rollout- und Test-Checkliste zum Abhaken je Projekt (Infrastruktur → Strukturtest → Integrationstest → Produktivtest)

## Lesefassung

- **`AI_Automation_Arbeitsbuch.pdf`** — alle vier Dokumente zu einem durchgängigen 20-seitigen Nachschlagewerk zusammengefasst, Inhalt unverändert

## Bezug zum Workflow-Portfolio

Mehrere Konzepte aus diesen Papieren sind in den Workflows 10–15 (Cross-Domain: Compliance & Error Handling) konkret umgesetzt — etwa der zentrale Error-Trigger-Workflow (13) statt verstreuter Fehlerbehandlung, der Audit Trail mit `entschieden_von`/`begruendung` (12), und der Heartbeat-Monitor (15) als Ergänzung zur reinen Fehlerbehandlung.
