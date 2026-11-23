# Format: Kennzahlen (03-Veroeffentlicht)

Dateiname: `<id>-kennzahlen-YYYYMMDD.md`. Bis zum Cockpit-Umbau legt Matthias die Datei in
Obsidian aus der Vorlage `00-System/vorlagen/kennzahlen.md` an.

```markdown
---
id: <karten-id>
gemessen_am: 2026-12-07
tage_nach_post: 7
impressionen: 2140
reaktionen: 38
kommentare: 6
reposts: 2
---

Notizen (optional): auffällige Kommentare, wer reagiert hat, Kontext.
```

`tools/metriken.py` liest nur das Frontmatter. Fehlt ein Wert, wird der Post für diese
Kennzahl übersprungen, nicht mit 0 gerechnet.
