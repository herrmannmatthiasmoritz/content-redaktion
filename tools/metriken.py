#!/usr/bin/env python3
"""Kennzahlen für Lern-Agent und Scout. Rechnet, interpretiert nicht.

Eingabe: ein JSON-Dokument (Datei oder stdin) mit
{
  "karten":   [{"id", "thema", "typ", "status", "quellen": [url, ...]}],  # aus dem Cockpit-Zustand
  "posts":    [{"id", "typ", "draft": str, "veroeffentlicht": str}],   # aus 03-Veroeffentlicht
  "kennzahlen": [{"id", "impressionen", "reaktionen", "kommentare", "reposts"}],
  "toene":    [{"id", "ton", "experiment": bool}]                      # aus LinkedIn-Experiment
}
`typ` ist der Fundtyp der Karte (optional, fehlt -> "ohne").
Ausgabe: JSON mit Annahmequoten (je Thema, Quelle, Typ), Post-Tabelle, Wirkung je Typ
und Ton-Vergleich.

    python3 tools/metriken.py eingabe.json > metriken.json
"""
import json
import statistics
import sys
from collections import defaultdict
from urllib.parse import urlparse

VERUNREINIGT_AB = 0.4
GENOMMEN = {"ausgewaehlt", "draft", "veroeffentlicht"}


def levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    vorher = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        jetzt = [i]
        for j, cb in enumerate(b, 1):
            jetzt.append(min(vorher[j] + 1, jetzt[j - 1] + 1, vorher[j - 1] + (ca != cb)))
        vorher = jetzt
    return vorher[-1]


def _woerter(text: str) -> list:
    return " ".join(text.split()).split(" ") if text.strip() else []


def nachschliff_distanz(draft: str, fassung: str) -> float:
    """Wortbasierte Editierdistanz, normiert auf 0..1.

    Wortbasiert statt zeichenbasiert: ein umformulierter Satz soll mehr zählen als
    ein Tippfehler, und Unicode-Fettschrift in der ersten Zeile (LinkedIn-Formatter)
    soll nicht als komplette Neufassung gelten — deshalb vorher normalisieren.
    """
    a, b = _woerter(normalisieren(draft)), _woerter(normalisieren(fassung))
    if not a and not b:
        return 0.0
    return round(levenshtein(a, b) / max(len(a), len(b)), 3)


def normalisieren(text: str) -> str:
    """Mathematische Alphanumerik (𝐁𝐨𝐥𝐝, 𝘐𝘵𝘢𝘭𝘪𝘤 …) auf ASCII zurückführen, ** entfernen."""
    import unicodedata
    raus = []
    for z in unicodedata.normalize("NFKC", text):
        raus.append(z)
    return "".join(raus).replace("**", "")


def engagement_rate(k: dict):
    try:
        imp = float(k["impressionen"])
        if imp <= 0:
            return None
        return round((float(k["reaktionen"]) + 2 * float(k["kommentare"])
                      + 3 * float(k["reposts"])) / imp, 4)
    except (KeyError, TypeError, ValueError):
        return None


def domain(url: str) -> str:
    try:
        return urlparse(url).netloc.removeprefix("www.")
    except Exception:
        return ""


def annahmequoten(karten: list) -> dict:
    je_thema = defaultdict(lambda: [0, 0])
    je_quelle = defaultdict(lambda: [0, 0])
    je_typ = defaultdict(lambda: [0, 0])
    for k in karten:
        st = k.get("status")
        if st not in GENOMMEN and st != "verworfen":
            continue  # "neu" ist noch keine Entscheidung
        genommen = st in GENOMMEN
        je_thema[k.get("thema", "?")][0 if genommen else 1] += 1
        je_typ[k.get("typ") or "ohne"][0 if genommen else 1] += 1
        for d in {domain(u) for u in k.get("quellen", []) if u}:
            je_quelle[d][0 if genommen else 1] += 1

    def fassen(d):
        return {name: {"genommen": g, "verworfen": v, "quote": round(g / (g + v), 3)}
                for name, (g, v) in sorted(d.items())}
    return {"thema": fassen(je_thema), "quelle": fassen(je_quelle), "typ": fassen(je_typ)}


def spanne(werte: list) -> dict:
    if not werte:
        return {"n": 0}
    return {"n": len(werte), "median": round(statistics.median(werte), 4),
            "min": min(werte), "max": max(werte)}


def auswerten(daten: dict) -> dict:
    kennz = {k["id"]: k for k in daten.get("kennzahlen", [])}
    toene = {t["id"]: t for t in daten.get("toene", [])}
    tabelle = []
    for p in daten.get("posts", []):
        t = toene.get(p["id"], {})
        dist = nachschliff_distanz(p.get("draft", ""), p.get("veroeffentlicht", ""))
        er = engagement_rate(kennz[p["id"]]) if p["id"] in kennz else None
        tabelle.append({"id": p["id"], "typ": p.get("typ") or "ohne", "ton": t.get("ton"), "experiment": bool(t.get("experiment")),
                        "nachschliff_distanz": dist, "engagement_rate": er,
                        "verunreinigt": dist > VERUNREINIGT_AB})

    vergleich = {}
    for ton in ("A", "B"):
        im = [z for z in tabelle if z["experiment"] and z["ton"] == ton]
        vergleich[ton] = {
            "posts": len(im),
            "durchgefallen_bei_matthias": sum(z["verunreinigt"] for z in im),
            "nachschliff_distanz": spanne([z["nachschliff_distanz"] for z in im]),
            "engagement_rate": spanne([z["engagement_rate"] for z in im
                                       if not z["verunreinigt"] and z["engagement_rate"] is not None]),
        }
    # Wirkung je Fundtyp: alle Posts mit Kennzahl, Ton egal. Verunreinigte zählen mit,
    # hier geht es um das Thema, nicht um den Ton.
    je_typ = defaultdict(list)
    for z in tabelle:
        if z["engagement_rate"] is not None:
            je_typ[z["typ"]].append(z["engagement_rate"])
    wirkung_je_typ = {typ: spanne(w) for typ, w in sorted(je_typ.items())}

    return {"annahmequoten": annahmequoten(daten.get("karten", [])),
            "posts": tabelle, "wirkung_je_typ": wirkung_je_typ, "ton_vergleich": vergleich}


def main() -> None:
    quelle = open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin
    print(json.dumps(auswerten(json.load(quelle)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
