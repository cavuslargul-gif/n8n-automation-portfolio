# 10 – Retail: Automatisierte Erfassung – Mahnwesen und Tagesgeschäft

## Use Case
Automatisiert die tägliche und wöchentliche Status-Übersicht für Handwerksbetriebe: offene Termine, technische Workflow-Fehler und zurückgestellte Mahnungen (offene Posten) werden gesammelt und per E-Mail an die Geschäftsführung verschickt. Neue Fälle werden zusätzlich automatisch als Google Task angelegt — inklusive Duplikat-Schutz, damit derselbe zurückgestellte Posten nicht jeden Tag erneut einen Task erzeugt.

## Workflow
Zwei unabhängige Ketten im selben Workflow — Täglich (7:00 Uhr) und Wöchentlich (Montag, 7:00 Uhr) — sammeln Termine (Google Calendar), Fehler (Data Table) und Mahnwesen (Data Table), fassen sie per Aggregate/Merge zusammen und verschicken eine Übersichtsmail (Gmail). Parallel dazu legt die Täglich-Kette Google Tasks für neue Fehler und neue zurückgestellte Mahnungen an.

<!-- Screenshot des Canvas hier einfügen -->

## How it was built
- **Schedule Trigger** (täglich 7:00 Uhr, wöchentlich Montag 7:00 Uhr) — zwei komplett getrennte Ketten statt einer gemeinsamen, um fragile Cross-Referenzen zwischen den Zeiträumen zu vermeiden (in einer Ausführung läuft immer nur ein Trigger)
- **Google Calendar** (Get Many) sammelt Termine für den jeweiligen Zeitraum
- **n8n Data Table** (`workflow_error_log`) liefert Fehlermeldungen der letzten 24h bzw. letzten 7 Tage
- **n8n Data Table** (`offene_posten`) liefert zurückgestellte Mahnungen; im Täglich-Pfad zusätzlich gefiltert auf `task_erstellt = false`, damit bereits bearbeitete Fälle nicht erneut auftauchen
- **Aggregate**-Nodes fassen Termine/Fehler/Mahnungen pro Zweig zu einem Datensatz zusammen, **Merge** kombiniert beide Zweige für die E-Mail
- **Gmail** verschickt eine Textmail mit allen drei Listen (Fallback: „Keine X" wenn eine Liste leer ist)
- **Google Tasks** legt parallel pro neuem Fehler und pro neuer zurückgestellter Mahnung einen Task an
- Eine eigene **Data-Table-Update-Node** setzt nach Task-Erstellung das Flag `task_erstellt = true` auf die jeweilige Rechnungsnummer — verhindert, dass derselbe Posten am nächsten Tag erneut einen Task erzeugt

## How it works
1. Der Trigger (täglich 7:00 Uhr bzw. wöchentlich Montag 7:00 Uhr) startet die jeweilige Kette
2. Termine, Fehler und zurückgestellte Mahnungen werden aus Google Calendar bzw. den Data Tables abgerufen
3. Für neue Fehler und neue zurückgestellte Mahnungen (nur Täglich-Kette) wird automatisch ein Google Task angelegt
4. Das Flag `task_erstellt` wird direkt danach auf `true` gesetzt — verhindert Duplikate bei künftigen Läufen
5. Alle drei Listen werden zu einer Übersichtsmail zusammengeführt und per Gmail an die Geschäftsführung verschickt

**Hinweis:** Die Duplikat-Schutz-Logik (`task_erstellt`-Flag) wurde nachträglich ergänzt, nachdem im Testbetrieb auffiel, dass der Täglich-Lauf pro Tag einen neuen Task für denselben bereits zurückgestellten Posten erzeugte — die ursprüngliche Filterbedingung kannte nur den Status, kein Zeit- oder Bearbeitungsfenster.

## Nodes

<!-- Screenshot der Node-Liste hier einfügen -->

## Tools
- n8n Schedule Trigger
- Google Calendar (OAuth2)
- n8n Data Table
- n8n Aggregate / Merge
- Gmail (OAuth2)
- Google Tasks (OAuth2)

## Background
Entwickelt für Handwerksbetriebe, die Mahnwesen, Termine und technische Fehler nicht in drei getrennten Systemen prüfen wollen. Zurückgestellte Mahnungen — etwa bei Ratenvereinbarung oder laufender Kundenanfrage — brauchen aktive Nachverfolgung statt stillem Vergessen. Die automatische Task-Erstellung mit Duplikat-Schutz sorgt dafür, dass jeder Fall genau einmal sichtbar wird, nicht täglich neu. Reiner Informationsworkflow: keine automatischen Kunden- oder Geschäftsaktionen, keine Zahlungsauslösung.
