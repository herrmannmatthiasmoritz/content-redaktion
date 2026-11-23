# content-redaktion

Multiagenten-System für Matthias' LinkedIn-Pipeline. Spezifikation:
Projekt „AI - Agenten" → `agent-02-content-redaktion-spec.md`. Regeln für alle Läufe:
[`CLAUDE.md`](CLAUDE.md).

```
Mo  Redaktionslauf   lern-agent → rechercheur ×5 (parallel) → redakteur → 01-Research
                     ↓
    Cockpit          Matthias: Nehmen / Weg / Draft anfordern
                     ↓
2×/Tag Draftlauf     ton_zuweisung.py → schreiber ⇄ kritiker → 02-Drafts
                     ↓
    LinkedIn         Matthias postet, erfasst Fassung + nach 7 Tagen Kennzahlen
                     ↓
1. d. M. Scoutlauf   scout → Vorschläge
```

## Aufbau

| Pfad | Inhalt |
|---|---|
| `.claude/agents/` | 6 Subagenten — bekommen Text, geben Text zurück, kein Drive-Zugriff |
| `.claude/skills/themen-recherche/` | Recherche-Skill (übernommen, Speicherort angepasst) |
| `runs/` | Ablauf je geplanter Aufgabe — die Hauptsession macht alle Drive-Zugriffe |
| `config/` | Themen, Drive-IDs, Regeln des Ton-Experiments |
| `formate/` | Dateiformate = Verträge mit dem Cockpit |
| `tools/` | Code statt Modell: Ton-Zuweisung, Kennzahlen, LinkedIn-Formatter |
| `tests/` | `python3 -m unittest discover -s tests` · `node tools/linkedin-format/linkedin-format.test.js` |
| `vault-seed/` | Startinhalt von `00-System` (schon in Drive angelegt am 23.11.2026) |
| `docs/cockpit-umbau.md` | geplante Änderungen am Cockpit-Artefakt |

## Lokal ausprobieren (Claude Code)

```bash
cd content-redaktion
claude
> Lies runs/draftlauf.md und mach einen Trockenlauf mit tests/fixtures/anforderung-beispiel.md.
  Schreib nach tests/out/ statt nach Drive.
```

## Geplante Aufgaben

Die Aufgaben laufen in der Cloud in einer Umgebung mit diesem Repo. Prompt jeweils nur:

| Aufgabe | Zeitplan | Prompt |
|---|---|---|
| Redaktionslauf | Mo 06:00 Europe/Berlin | `Führe runs/redaktionslauf.md aus. Unbeaufsichtigt.` |
| Draftlauf | täglich 12:00 und 19:00 | `Führe runs/draftlauf.md aus. Unbeaufsichtigt.` |
| Scoutlauf | am 1. um 06:00 | `Führe runs/scoutlauf.md aus. Unbeaufsichtigt.` |

Benötigte Connectoren: Google Drive. Für den Kurationszustand zusätzlich Lesezugriff auf das
Cockpit-Artefakt (sonst Klick-Protokoll aus dem Cockpit-Umbau, Punkt 5).

## Inbetriebnahme

1. Stil-Korpus füllen (`00-System/stil-korpus/`, 5–10 eigene Posts) → Stil A erzeugen lassen,
   abnicken.
2. Redaktionslauf eine Woche **parallel** zu den 5 alten Recherche-Aufgaben laufen lassen,
   vergleichen, dann die alten pausieren.
3. Cockpit-Umbau Punkt 1–3, dann Draftlauf einschalten → Ton-Experiment beginnt.
4. Cockpit-Umbau Punkt 4–5.
5. Scoutlauf nach ca. 6 Wochen einschalten.
