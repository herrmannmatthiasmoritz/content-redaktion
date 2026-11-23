---
name: themen-recherche
description: >-
  Führt eine strukturierte Web-Recherche zu einem vorgegebenen Thema durch (z. B.
  Wettbewerber-News, Patentanmeldungen, Branchenentwicklungen, Technologietrends) und
  liefert das Ergebnis als datierte Markdown-Datei mit Quellenangaben. Trennt Fakten
  strikt von offenen Fragen, verwendet keine Bewertung, Scores oder Prozentangaben.
  Nutze diesen Skill IMMER, wenn ein Recherche-Thema übergeben wird, ob als expliziter
  Auftrag im Chat, als Parameter eines Scheduled Tasks, oder als knappe Eingabe wie ein
  reiner Themenname ohne weitere Erklärung (Beispiele: "Akkutechnologie Wettbewerber"
  oder "KI-Regulierung EU").
---

# Themen-Recherche

Genereller Recherche-Skill für wiederkehrende oder ad-hoc Themenrecherchen. Ersetzt das
manuelle `news_agent.py`-Script durch eine Cowork-Skill-Variante, die auch unbeaufsichtigt
über einen Scheduled Task laufen kann.

## Zweck

Zu einem vorgegebenen Thema aktuelle, relevante Entwicklungen finden (News, Patente,
Publikationen, Marktbewegungen) und daraus einen kurzen, faktenbasierten Report erzeugen —
ohne Bewertung oder Interpretation, die über das Belegbare hinausgeht.

## Eingabe

Der Skill wird mit mindestens einem **Thema** aufgerufen, z. B.:
- "Patentanmeldungen Wettbewerber Akkutechnologie E-Bike"
- "News Hardware Scale-ups München"
- "KI-Regulierung EU"

Optional können mitgegeben werden:
- **Zeitraum** (Default: letzte 7 Tage — passend für wöchentliche Scheduled Tasks; bei
  selteneren Läufen entsprechend anpassen, z. B. letzte 30 Tage)
- **Fokus/Kontext** (z. B. "Fokus auf Relevanz für Hardware-Scale-ups im Raum München")

Fehlt der Zeitraum, wird der Default verwendet. Fehlt der Fokus, wird allgemein zum Thema
recherchiert.

## Rechercheprozess

1. Websuche zum Thema, eingegrenzt auf den angegebenen Zeitraum.
2. 3–7 relevante Treffer sammeln. Weniger, aber wirklich relevante Treffer sind besser als
   aufgefüllte Ergebnislisten.
3. Für jeden Treffer: Was wurde berichtet, von wem, wann, mit Quelle.
4. Prüfen, ob sich Treffer widersprechen oder unbestätigt sind — das gehört in die offenen
   Fragen, nicht in die Fakten.
5. Gleiche Skepsis gegenüber bekannten und unbekannten Quellen anwenden — eine Meldung von
   einem großen Medienhaus ist nicht automatisch verlässlicher als eine Fachpublikation, und
   umgekehrt ist eine unbekannte Quelle nicht automatisch unseriös.
6. Keine Bewertung, kein Score, keine Prozentangabe zu "Relevanz" oder "Wichtigkeit" — die
   Einordnung, was wichtig ist, bleibt beim Leser.

## Ausgabeformat

```markdown
# Recherche: {Thema}

Datum: {YYYY-MM-DD}
Zeitraum: {z. B. letzte 7 Tage}

## Fakten

- {Kurzbeschreibung des Fundes} ({Quelle}, {Datum})
- {Kurzbeschreibung des Fundes} ({Quelle}, {Datum})
- ...

## Offene Fragen

- {Was ist unklar, unbestätigt, oder sollte manuell nachrecherchiert werden}
- ...

## Quellen

- {Quelle 1 mit Link}
- {Quelle 2 mit Link}
- ...
```

Falls in einem Durchlauf keine relevanten Treffer gefunden werden, wird das explizit unter
"Fakten" vermerkt ("Keine relevanten Treffer im Zeitraum gefunden") statt die Datei leer zu
lassen oder Treffer zu erzwingen.

## Speicherort

In diesem Repo legt der Skill **nichts selbst ab**. Der Subagent `rechercheur` gibt den
Report als Text an die Hauptsession zurück; abgelegt wird er erst nach dem Redakteur in
`01-Research` (Format: `formate/recherche-datei.md`).

Ausserhalb des Repos (Chat, alter Scheduled Task) gilt weiter: datierte Markdown-Datei
`{thema-slug}-{datum}.md`.

## Hinweise für Scheduled Tasks

Wenn dieser Skill über einen Scheduled Task ausgelöst wird, liefert die Task-Konfiguration
das Thema (und ggf. Zeitraum/Fokus) als festen Parameter. Der Skill selbst muss dafür nicht
angepasst werden — pro Scheduled Task wird lediglich ein anderes Thema übergeben, z. B.:

- Task "Wöchentliche Wettbewerbsrecherche" → Thema: "Patentanmeldungen Wettbewerber
  Akkutechnologie E-Bike", wöchentlich montags
- Task "Branchen-News Hardware Scale-ups" → Thema: "News Hardware Scale-ups München",
  wöchentlich

Mehrere Scheduled Tasks können denselben Skill mit unterschiedlichen Themen nutzen, statt für
jedes Thema einen eigenen Skill zu bauen.

## Qualitätsprinzipien

- Fakten und offene Fragen bleiben getrennt — wie bei Stellenanzeigen-Check und
  Firmenscanner.
- Keine Scores, keine Prozentangaben, keine "Relevanz-Ratings".
- Jede Aussage unter "Fakten" braucht eine nachvollziehbare Quelle.
- Im Zweifel gehört ein Punkt eher unter "Offene Fragen" als unbelegt unter "Fakten".
