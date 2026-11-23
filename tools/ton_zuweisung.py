#!/usr/bin/env python3
"""Ton-Zuweisung für das Experiment A/B — blockrandomisiert, reproduzierbar.

Warum nicht das Modell würfeln lassen: Sprachmodelle würfeln schlecht und nicht
nachprüfbar. Hier gilt: Blöcke à 4 Zuweisungen, in jedem Block genau 2×A und 2×B,
Reihenfolge je Block aus einem festen Seed. Damit bleibt das Verhältnis auch bei
wenigen Posts ausgeglichen, und Matthias kann den nächsten Ton nicht erraten.

Aufruf:
    python3 tools/ton_zuweisung.py --nr 7 --sprache en
    -> {"ton": "B", "experiment": true, "zuweisung_nr": 7}

--nr ist die laufende Nummer der Zuweisung im Experiment (0-basiert), also die
Anzahl der bereits vorhandenen Zuweisungen mit experiment: true.
"""
import argparse
import json
import random

SEED = "content-redaktion-2026-11-23"
BLOCK = ("A", "A", "B", "B")


def ton_fuer(nr: int) -> str:
    if nr < 0:
        raise ValueError("nr muss >= 0 sein")
    block_nr, stelle = divmod(nr, len(BLOCK))
    block = list(BLOCK)
    random.Random(f"{SEED}:{block_nr}").shuffle(block)
    return block[stelle]


def zuweisen(nr: int, sprache: str) -> dict:
    if sprache != "en":
        # Deutsche Posts laufen außerhalb des Experiments immer in Matthias' Ton.
        return {"ton": "A", "experiment": False, "zuweisung_nr": None}
    return {"ton": ton_fuer(nr), "experiment": True, "zuweisung_nr": nr}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--nr", type=int, required=True)
    p.add_argument("--sprache", default="en")
    a = p.parse_args()
    print(json.dumps(zuweisen(a.nr, a.sprache)))


if __name__ == "__main__":
    main()
