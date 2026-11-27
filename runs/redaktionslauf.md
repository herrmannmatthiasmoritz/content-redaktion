# Redaktionslauf (wöchentlich, Montag ca. 06:00 Europe/Berlin)

Unbeaufsichtigt. Erst `CLAUDE.md` lesen. IDs aus `config/drive.yaml`.
Stempel für diesen Lauf: aktuelle UTC-Zeit als `YYYYMMDDTHHMMSS`, Datum als `YYYY-MM-DD`.

## 1. Einlesen (Hauptsession)

1. `config/themen.yaml` lesen, nur `aktiv: true`.
2. Jüngstes Redaktionsprofil aus `00-System/profil/` (höchster Stempel im Dateinamen).
3. `00-System/quellen.md`.
4. Kurationszustand aus dem Cockpit:
   - bevorzugt: Artefakt `cockpit_slug` lesen (read_artifact) und den JSON-Block
     `<script type="application/json" id="pipeline-state">` parsen
   - sonst: alle Dateien in `00-System/klicks/` (nach dem Cockpit-Umbau)
   - geht beides nicht: ohne Klicks weiter, im Protokoll vermerken
5. Je Thema die Fakten aus `01-Research` → `bereits_gesehen`: Fakten mit `[meldung]` (oder
   ohne Typ, ältere Dateien) der letzten 3 Wochen, alle anderen Typen der letzten 12 Wochen.
   Grund: Ältere Fallstudien und Studien dürfen gefunden werden, sollen aber nicht jede
   Woche wiederkommen.
6. Zu jeder Karte aus 1.4 den Fundtyp ergänzen: in der zugehörigen Datei in `01-Research`
   die Zeile `Typ:` lesen. Fehlt sie (Dateien vor dem 27.11.2026, alte Aufgaben) →
   `typ: "ohne"`.
7. Veröffentlichte Fassungen und Kennzahlen aus `03-Veroeffentlicht`, Ton-Zuweisungen aus
   `LinkedIn-Experiment`. Jeder Post erbt den `typ` seiner Karte (gleiche id).

## 2. Lernen

1. Aus Schritt 1.4, 1.6 und 1.7 das Eingabe-JSON für `tools/metriken.py` bauen (Format im Kopf der
   Datei), nach `/tmp/metriken-ein.json` schreiben, ausführen:
   `python3 tools/metriken.py /tmp/metriken-ein.json > /tmp/metriken.json`
2. Subagent **lern-agent**, Modus `wochenauswertung`, mit altem Profil, Klicks, Metriken.
3. Ablegen (neu anlegen, nie überschreiben):
   - `00-System/profil/redaktionsprofil-<stempel>.md`
   - `00-System/performance/performance-<stempel>.md`
   - `00-System/ton-experiment/stand-<stempel>.md` — **ohne Ton je Post-ID**, nur Summen je
     Ton. Dieser Ordner liegt im Vault, Matthias sieht ihn.

Ab hier gilt das **neue** Profil.

## 3. Recherche (parallel)

Für jedes aktive Thema **gleichzeitig** einen Subagenten **rechercheur** starten (alle
Task-Aufrufe in einer Nachricht). Mitgeben: Thema, Fokus, `zeitfenster` (Standard aus
`standard_zeitfenster`, überschrieben durch ein `zeitfenster:` am Thema), Quellenlisten,
Profil-Auszug, `bereits_gesehen` dieses Themas.

Themen mit `art: lernstoff` zusätzlich:
- `art`, `zeitraum` und `lernpfad` aus `config/themen.yaml`
- `material`: Inhalt aller Dateien im angegebenen Repo-Ordner (z. B. `config/lernstoff/`)
- `bereits_gesehen` hier aus den letzten **12** Wochen statt 3, sonst wiederholt sich der
  Lernpfad zu schnell. Maßgeblich sind die `# Recherche: AI verstehen: <Leitfrage>`-Zeilen.

Schlägt ein Rechercheur fehl: einmal neu starten, dann ohne dieses Thema weiter.

## 4. Redaktion

Subagent **redakteur** mit allen Reports, Profil, Positionierung, letzten 8 Post-Themen.
Jeden Report mit seiner `thema_id` und `art` (falls gesetzt) kennzeichnen, damit der
Redakteur Erklärstücke (`art: lernstoff`) nach seinen Sonderregeln behandelt.
Vor dem Anlegen prüfen: Jede Datei hat eine Zeile `Typ:` und einen Abschnitt `## Warum jetzt`
mit `Hypothese:` und `Winkel:`. Fehlt etwas → Redakteur einmal erneut fragen, sonst so
ablegen und im Protokoll vermerken.
Antwort ist ein JSON-Array. Für jeden Eintrag mit `inhalt`:
- Steht in `config/themen.yaml` `parallelbetrieb: true`: vor `.md` den Zusatz ` (Redaktion)`
  einfügen, z. B. `2026-11-30 AI Trends Mittelstand (Redaktion).md`. Sonst gleichnamige
  Dateien der alten Aufgaben → Kollision.
- Datei `01-Research/<dateiname>` anlegen (text/markdown, keine Konvertierung)
- Gibt es den Dateinamen schon: nicht anlegen, im Protokoll vermerken (das Cockpit würde
  sonst zwei Karten mit derselben id bauen)

## 5. Abschluss

- Protokoll `00-System/protokolle/redaktionslauf-<stempel>.md`: Themen, Funde je Thema und Typ,
  verworfene Dubletten, angelegte Dateien, Profiländerungen, Fehler.
- Letzte Ausgabe, eine Zeile: `Redaktionslauf <datum>: <n> Dateien, Typen: <typ×anzahl, …>, beste Karte: <thema> (Score <s>).`
- **Keine Datei per Chat schicken.**
