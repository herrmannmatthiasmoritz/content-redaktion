# Cockpit-Umbau (Artefakt „Content-Kuration")

**Stand 23.11.2026:** Punkte 1–3 umgesetzt (plus Marke „Redaktion" für den Parallelbetrieb).
Offen: 4 (Kennzahlen) und 5 (Klick-Protokoll, nicht dringend, weil das Artefakt lesbar ist).

Gezielte Änderungen, keine Neufassung. **Vorher das Cockpit überall schließen**: Das Cockpit
publiziert bei jedem Klick seine geladene Fassung neu. Ist es offen, während der Umbau
veröffentlicht wird, kann ein Klick den Umbau überschreiben oder umgekehrt.

## 1. „Für LinkedIn kopieren" (höchste Priorität)

Heute kopiert „Text kopieren" den Draft roh — `**fett**` landet als Sternchen in LinkedIn,
und HTML-Formatierung überlebt das Einfügen ohnehin nicht. Neu:

- `tools/linkedin-format/linkedin-format.js` unverändert als eigenen `<script>`-Block einfügen
  (setzt `globalThis.linkedinFormat`).
- Im Handler von „Text kopieren" in `renderEntwurf()`:
  `navigator.clipboard.writeText(linkedinFormat(entwurf.post || ""))`
- Knopf umbenennen in „Für LinkedIn kopieren"; Stil `serif` wie bisher genutzt.

Damit entfällt der Umweg über den Online-Formatter.

## 2. Score und „Warum jetzt" aus der Recherchedatei

In `zerlegeRecherche()` zusätzlich lesen:
- `^Score:[ \t]*(\d)` → `score`
- Abschnitt `## Warum jetzt` bis zur nächsten Überschrift → `hook`

`rohAlsKarte()` und `rohUebernehmen()` übernehmen `hook` (heute fest `""`) und `score`.
`renderList()` sortiert im Tab „Neu" nach `score` absteigend, dann Datum.
Karte zeigt den Score klein in `.karte-meta`.

## 3. Sprache je Anforderung

Neben „Draft anfordern" ein Umschalter `EN | DE` (Standard EN). `anforderungstext()` schreibt
`"sprache": "de"` in den JSON-Block, wenn DE gewählt ist.

## 4. Kennzahlen-Eingabe

Auf veröffentlichten Karten, deren Fassung ≥ 7 Tage alt ist und für die keine
`<id>-kennzahlen-*.md` existiert: Hinweis „Kennzahlen fällig" + vier Zahlenfelder.
Sichern legt die Datei nach `formate/kennzahlen-datei.md` in 03 an (gleiche Bauart wie
`veroeffentlichungSichern()`).

## 5. Klick-Protokoll

In `statusSetzen()` und `rohUebernehmen()` zusätzlich eine Datei
`00-System/klicks/<stempel>-<id>-<status>.md` anlegen (Frontmatter: id, status, thema,
zeitpunkt). Grund: Der Kurationszustand liegt nur im Artefakt; ein Lauf, der das Artefakt
nicht lesen kann, sieht sonst keine Klicks.

## Nicht ändern

- Den Ton eines Drafts **nie** anzeigen. Er steht ohnehin nicht im Draft.
- Bestehende Dateinamen-Konventionen (`anforderung-`, `-draft.md`, `-veroeffentlicht-`).
