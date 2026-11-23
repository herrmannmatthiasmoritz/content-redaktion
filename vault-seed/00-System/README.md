# 00-System

Das Gedächtnis der Content-Redaktion. Agenten schreiben hier, du liest und pflegst in Obsidian.

| Ordner/Datei | Wer schreibt | Was |
|---|---|---|
| `profil/` | lern-agent (wöchentlich), du (Abschnitt Positionierung) | Redaktionsprofil, jüngste Fassung gilt |
| `quellen.md` | du | Positiv- und Ausschlussliste |
| `stil/` | du + lern-agent (nur Stil A) | Stil A (dein Ton), Stil B (Claude-Ton, eingefroren) |
| `stil-korpus/` | du | deine eigenen alten Posts als Vorlage für Stil A |
| `performance/` | Redaktionslauf | Tabelle aller Posts mit Kennzahlen |
| `ton-experiment/` | Redaktionslauf | Summen A vs. B — ohne Zuordnung je Post |
| `scout/` | Scoutlauf (monatlich) | Vorschläge zu Themen und Quellen |
| `protokolle/` | alle Läufe | was ein Lauf getan hat |
| `vorlagen/` | — | Obsidian-Vorlage für Kennzahlen |
| `klicks/` | Cockpit (nach Umbau) | Protokoll deiner Nehmen/Weg-Klicks |

## Regeln
- **Jüngste Fassung gilt.** Agenten legen neue Dateien mit Zeitstempel an, statt zu
  überschreiben (der Drive-Connector kann keinen Inhalt ändern). Ältere Fassungen bleiben
  liegen — das ist die Historie.
- **Wenn du eine Datei änderst**, ändere die jüngste Fassung direkt in Obsidian. Drive for
  Desktop synchronisiert das.
- **Nicht öffnen:** den Drive-Ordner `LinkedIn-Experiment` (liegt neben diesem Vault). Dort
  steht, welcher Draft in welchem Ton geschrieben ist.

## Kennzahlen eintragen (bis das Cockpit es kann)
7 Tage nach einem Post: in `03-Veroeffentlicht` neue Notiz `<id>-kennzahlen-<YYYYMMDD>.md`
aus der Vorlage `vorlagen/kennzahlen.md`, vier Zahlen aus der LinkedIn-Post-Analyse eintragen.
Die `<id>` steht im Dateinamen der veröffentlichten Fassung.
