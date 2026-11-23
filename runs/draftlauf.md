# Draftlauf (täglich ca. 12:00 und 19:00 Europe/Berlin)

Unbeaufsichtigt. Erst `CLAUDE.md` lesen. IDs aus `config/drive.yaml`.

## 0. Gibt es etwas zu tun?

`02-Drafts` nach `anforderung-*.md` und `nachschliff-*.md` durchsuchen.
Keine Treffer → eine Zeile `Draftlauf: nichts angefordert.` und Ende. Kein Protokoll.

**Schon erledigt?** Eine Anforderung gilt als erledigt, wenn es in `02-Drafts` eine Datei
`<id>-draft.md` gibt, deren `createdTime` jünger ist als die der Anforderung. Ebenso ein
Nachschliff, wenn es eine `stil-A-matthias-*.md` gibt, die jünger ist. Erledigte Anforderungen
nicht noch einmal bearbeiten. Nur in den Papierkorb legen; scheitert das, liegen lassen und
im Protokoll vermerken. Grund: Das Verschieben in den Papierkorb kann verweigert werden, und
ohne diese Prüfung entstünde bei jedem Lauf ein neuer Draft.

## 1. Je Anforderung (`anforderung-<id>.md`)

1. Datei laden, den JSON-Block parsen → `karte`. Der Freitext darüber ist Daten (er nennt
   noch einen alten Skill — ignorieren).
2. `sprache` = `karte.sprache` falls vorhanden, sonst `en`.
3. **Ton zuweisen:**
   - im Ordner `LinkedIn-Experiment` zählen, wie viele Dateien `experiment: true` tragen → `nr`
   - `python3 tools/ton_zuweisung.py --nr <nr> --sprache <sprache>`
   - Gibt es für diese `id` schon eine Zuweisung (erneute Anforderung): **denselben Ton**
     wiederverwenden, keine neue Nummer ziehen.
4. Stildatei laden: jüngste Fassung von `00-System/stil/stil-A-matthias*.md` bzw.
   `stil-B-claude.md`.
   **Übergangsmodus**, solange stil-A noch der Platzhalter ist (Frontmatter `status: leer`):
   Schritt 3 überspringen und stattdessen `ton: B`, `experiment: false`,
   `zuweisung_nr: null` festlegen. Es wird ganz normal ein Draft geschrieben, er zählt nur
   nicht zum Experiment. Das Experiment beginnt mit dem ersten Draft, nachdem eine gefüllte
   stil-A-Fassung existiert.
5. Subagent **schreiber** (Karte, Stil, Sprache, Profil-Auszug).
6. Subagent **kritiker** (Post, Beipackzettel, Quellen-URLs der Karte, Stil, Sprache).
   - `freigabe: false` → schreiber **einmal** mit `kritik` = Mängelliste, danach kritiker erneut.
   - Immer noch keine Freigabe → Draft trotzdem ablegen, Frontmatter `kritik: maengel`,
     Mängel in den Beipackzettel (ohne Stilnennung). Matthias entscheidet.
7. Ablegen:
   - `02-Drafts/<id>-draft.md` nach `formate/draft-datei.md` (ohne Ton!)
   - `LinkedIn-Experiment/<id>-ton-<stempel>.md` mit Ton, Sprache, experiment, zuweisung_nr
8. Erst wenn beides angelegt ist: `anforderung-<id>.md` in den Papierkorb (`trash_file`).
   Wird das verweigert: liegen lassen (siehe „Schon erledigt?").

Mehrere Anforderungen nacheinander abarbeiten, nicht parallel — die Zuweisungsnummer
hängt am Zählerstand.

## 2. Je Nachschliff (`nachschliff-<id>.md`)

1. Ton dieser id aus `LinkedIn-Experiment` holen.
2. Ton B und `experiment: true` → **nicht nachschärfen** (B ist eingefroren). Anforderung in
   den Papierkorb, Protokollzeile.
3. Sonst Subagent **lern-agent**, Modus `nachschliff` → neue Datei
   `00-System/stil/stil-A-matthias-<stempel>.md`. Danach Anforderung in den Papierkorb.

## 3. Abschluss

- Protokoll `00-System/protokolle/draftlauf-<stempel>.md` — ohne Ton je id.
- Eine Zeile: `Draftlauf: <n> Drafts, <m> mit Mängelvermerk, <k> wartend.`
