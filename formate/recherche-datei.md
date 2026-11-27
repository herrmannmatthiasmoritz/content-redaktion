# Format: Recherche-Datei (01-Research)

Vertrag mit dem Cockpit (`zerlegeRecherche()`). Dateiname: `YYYY-MM-DD <dateiname aus themen.yaml>.md`.
Das Cockpit macht aus dem Dateinamen die Karten-id — derselbe Name darf nie zweimal vorkommen.

```markdown
# Recherche: <Thema>

Datum: 2026-11-30
Zeitraum: Meldungen 7 Tage, sonst bis 12 Monate
Score: 4
Typ: fallstudie

## Warum jetzt

Hypothese: <für wen ist das interessant und warum — ein Satz, vom Redakteur>
Winkel: <was Matthias dazu sagen könnte, das andere nicht sagen — ein Satz>

## Fakten

- [<typ>] <interessantester Fund zuerst> (<Quelle>, <Datum>)
- [<typ>] <zweitinteressantester Fund> (<Quelle>, <Datum>)
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
- `## Warum jetzt` → Feld „Warum jetzt" der Karte (Inhalt seit 27.11.2026: Hypothese + Winkel;
  die Überschrift bleibt, damit das Cockpit sie findet)

Bis dahin stören beide Zeilen nicht; sie werden ignoriert.

## Was nur die Läufe lesen (Cockpit ignoriert es)
- `Typ:` → Fundtyp des besten Funds: `meldung`, `fallstudie`, `studie`, `widerspruch`,
  `patent`, `debatte`, `muster`. Der Redaktionslauf liest ihn, um die Annahmequote je Typ
  zu messen (Lean-Startup-Test: was findet Matthias, was findet die Zielgruppe interessant?).
- `[typ]` am Anfang jedes Fakts → Herkunft für den Redakteur. Steht auch im TL;DR; das ist
  gewollt, Matthias sieht so den Typ auf der Karte.
