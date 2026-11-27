# Rohmaterial von Matthias, 25.11.2026

Ausgangspunkt für das Thema `ai-lernstoff` (Lernpfad-Fragen 1 und 2). Das sind Notizen, keine Quellen: Jede Aussage, die
in eine Karte oder einen Post geht, braucht trotzdem eine verlinkte Primärquelle
(Anbieter-Doku, Paper, Standard). Der Code ist ein Beispiel zum Verstehen, kein Post-Inhalt.

## 1. Agent Harness

In der Architektur von KI-Agenten ist der Agent Harness (wörtlich: „Geschirr“ oder
„Laufzeit-Rahmen“) die äußere Systemschicht, die das eigentliche Sprachmodell (LLM) umschließt,
steuert und überhaupt erst handlungsfähig macht. Das LLM erzeugt nur Text (oder strukturierte
JSON-Befehle). Der Harness übernimmt die gesamte deterministische Orchestrierung und
Infrastruktur drumherum.

Drei Schichten:
- **Kern (LLM):** das „Gehirn“. Trifft Entscheidungen, plant Schritte, formuliert Tool-Aufrufe,
  kann aber selbst keinen Code ausführen und auf keine API zugreifen.
- **Agent Harness (Laufzeitumgebung):** „Nervensystem und Skelett“. Fängt den Output ab, führt
  Tools aus, verwaltet den Kontext, fängt Fehler ab (Retries), erzwingt Guardrails und
  Permissions und füttert das Ergebnis zurück, bis die Aufgabe erledigt ist (Agentic Loop).
- **Observability/Tracing** (z. B. Langfuse, OpenTelemetry): der „Röntgenblick“ von außen.
  Klinkt sich als Wrapper in den Harness ein und protokolliert jeden Schleifendurchlauf, jeden
  Tool-Aufruf und die Token-Kosten.

Fertige Harnesses sind z. B. LangGraph, PydanticAI oder das OpenAI Agents SDK. Man kann auch
einen schlanken eigenen bauen, was oft robuster und transparenter ist.

Minimalbeispiel (Python, Langfuse):

```python
@observe(name="agent-harness-run")          # Root-Span
def run_agent_harness(user_prompt, max_steps=5):
    messages = [system_prompt, user_prompt]
    for step in range(max_steps):           # die Schleife steuert der Harness, nicht das LLM
        msg = llm(messages, tools=TOOLS)
        messages.append(msg)
        if not msg.tool_calls:              # kein Tool mehr angefordert -> fertig
            return msg.content
        for call in msg.tool_calls:         # Tool-Ausführung inkl. Guardrails
            messages.append(run_tool(call))
    raise RuntimeError("max_steps erreicht")
```

Beispiel-Tool im Original: `get_machine_telemetry("EOS-M290-04")`, Rückgabe
`{"status": "warning", "laser_power_w": 370, "o2_ppm": 120}` (simuliert).

Warum die Trennung zählt: Über den Erfolg eines Agenten entscheidet weniger ein paar Prozent
Benchmark als die Qualität des Harness:
- **Context Engineering:** Der Harness entscheidet, was gekürzt wird, bevor das Context Window
  überläuft.
- **Security und Permissions:** Vor einem Schreib-Tool prüft der Harness deterministisch per
  Code die Berechtigung, nie per Prompt.
- **Human-in-the-Loop:** Der Harness pausiert bei kritischen Aktionen und wartet auf Freigabe.

## 2. Trace (Ausführungsprotokoll)

Ein Trace ist die lückenlose Aufzeichnung eines kompletten Agenten-Durchlaufs vom Input bis zum
Output. Weil Agenten dynamisch entscheiden (welches Tool, welche Daten per RAG, wie viele
Schleifen), ist der Trace der „Blackbox-Flugschreiber“ für Observability und Debugging.

Aufbau, hierarchisch aus Spans wie ein Baum:
- **Root Span (der gesamte Run):** vom User-Prompt bis zur finalen Antwort, mit Gesamtdauer,
  Token-Verbrauch, Kosten.
- **Child Spans (Einzelschritte):**
  - LLM-Calls: System- und User-Prompt, Modellparameter (z. B. Temperature), Reasoning, Antwort
  - Tool-Calls: welches Tool mit welchen Parametern, was kam zurück, inkl. Fehler
  - Retrieval (RAG): welche Abfrage, welche Chunks mit welchem Relevanz-Score
  - Sub-Agent-Handoffs: Übergabe von Kontext und Aufgaben zwischen Agenten

Im Beispiel oben: `agent-harness-run` (Root) → LLM-Call entscheidet sich für das Tool →
Tool-Span (z. B. 45 ms) → LLM-Call formuliert die Antwort.

Wozu in der Praxis:
- **Root-Cause-Analyse:** zeigt, wo es gekippt ist (falscher API-Wert vs. falscher Schluss des
  Modells, Endlosschleife).
- **Latenz und Kosten:** welcher Schritt die Zeit frisst oder Tokens verbrennt.
- **Evaluation und Regression-Tests:** Traces aus dem Betrieb als Testdaten, um Prompt- oder
  Modelländerungen gegen echte Läufe zu prüfen (LangSmith, Langfuse, Arize Phoenix,
  OpenTelemetry).
