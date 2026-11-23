# Format: Recherche-Datei (01-Research)

Vertrag mit dem Cockpit (`zerlegeRecherche()`). Dateiname: `YYYY-MM-DD <dateiname aus themen.yaml>.md`.
Das Cockpit macht aus dem Dateinamen die Karten-id — derselbe Name darf nie zweimal vorkommen.

```markdown
# Recherche: <Thema>

Datum: 2026-11-30
Zeitraum: letzte 7 Tage
Score: 4

## Warum jetzt

<1–2 Sätze vom Redakteur>

## Fakten

- <bester Fund zuerst> (<Quelle>, <Datum>)
- <zweitbester Fund> (<Quelle>, <Datum>)
- ...

## Offene Fragen

- ...

## Quellen

- [<Titel>](<https-URL>)
- ...
```

## Was das Cockpit heute liest
- `# Recherche:` → Thema, `Datum:` → Datum
- `## Fakten` → die **ersten zwei** Punkte werden zum TL;DR
- `## Quellen` → Links im Format `[Titel](URL)`

## Was das Cockpit erst nach dem Umbau liest (docs/cockpit-umbau.md)
- `Score:` → Sortierung in „Neu"
- `## Warum jetzt` → Feld „Warum jetzt" der Karte

Bis dahin stören beide Zeilen nicht; sie werden ignoriert.
