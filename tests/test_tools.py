"""python3 -m unittest discover -s tests"""
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import metriken  # noqa: E402
import ton_zuweisung  # noqa: E402


class TonZuweisung(unittest.TestCase):
    def test_jeder_block_ist_ausgeglichen(self):
        for block in range(25):
            toene = [ton_zuweisung.ton_fuer(block * 4 + i) for i in range(4)]
            self.assertEqual(Counter(toene), Counter({"A": 2, "B": 2}), toene)

    def test_reproduzierbar(self):
        self.assertEqual([ton_zuweisung.ton_fuer(i) for i in range(20)],
                         [ton_zuweisung.ton_fuer(i) for i in range(20)])

    def test_reihenfolge_ist_nicht_starr(self):
        bloecke = {tuple(ton_zuweisung.ton_fuer(b * 4 + i) for i in range(4)) for b in range(10)}
        self.assertGreater(len(bloecke), 1)

    def test_deutsch_nicht_im_experiment(self):
        self.assertEqual(ton_zuweisung.zuweisen(3, "de"),
                         {"ton": "A", "experiment": False, "zuweisung_nr": None})


class Metriken(unittest.TestCase):
    def test_distanz_unveraendert_ist_null(self):
        self.assertEqual(metriken.nachschliff_distanz("a b c", "a  b\nc"), 0.0)

    def test_unicode_fett_zaehlt_nicht_als_aenderung(self):
        draft = "**The most quoted numbers** came from vendors."
        fassung = "𝐓𝐡𝐞 𝐦𝐨𝐬𝐭 𝐪𝐮𝐨𝐭𝐞𝐝 𝐧𝐮𝐦𝐛𝐞𝐫𝐬 came from vendors."
        self.assertEqual(metriken.nachschliff_distanz(draft, fassung), 0.0)

    def test_distanz_komplett_neu(self):
        self.assertEqual(metriken.nachschliff_distanz("a b c d", "w x y z"), 1.0)

    def test_engagement_rate(self):
        k = {"impressionen": 1000, "reaktionen": 20, "kommentare": 5, "reposts": 2}
        self.assertEqual(metriken.engagement_rate(k), 0.036)

    def test_engagement_rate_fehlender_wert(self):
        self.assertIsNone(metriken.engagement_rate({"impressionen": 1000}))
        self.assertIsNone(metriken.engagement_rate(
            {"impressionen": 0, "reaktionen": 1, "kommentare": 0, "reposts": 0}))

    def test_annahmequote_ignoriert_neu(self):
        q = metriken.annahmequoten([
            {"thema": "X", "status": "ausgewaehlt", "quellen": ["https://www.a.com/1"]},
            {"thema": "X", "status": "verworfen", "quellen": ["https://a.com/2"]},
            {"thema": "X", "status": "neu", "quellen": ["https://a.com/3"]},
        ])
        self.assertEqual(q["thema"]["X"], {"genommen": 1, "verworfen": 1, "quote": 0.5})
        self.assertEqual(q["quelle"]["a.com"]["quote"], 0.5)

    def test_annahmequote_je_typ(self):
        q = metriken.annahmequoten([
            {"thema": "X", "typ": "fallstudie", "status": "ausgewaehlt"},
            {"thema": "X", "typ": "meldung", "status": "verworfen"},
            {"thema": "X", "status": "verworfen"},
        ])
        self.assertEqual(q["typ"]["fallstudie"]["quote"], 1.0)
        self.assertEqual(q["typ"]["meldung"]["quote"], 0.0)
        self.assertEqual(q["typ"]["ohne"]["verworfen"], 1)

    def test_wirkung_je_typ(self):
        r = metriken.auswerten({
            "posts": [{"id": "a", "typ": "widerspruch", "draft": "x", "veroeffentlicht": "x"},
                      {"id": "b", "draft": "x", "veroeffentlicht": "x"}],
            "kennzahlen": [{"id": "a", "impressionen": 100, "reaktionen": 5,
                            "kommentare": 0, "reposts": 0}],
        })
        self.assertEqual(r["wirkung_je_typ"], {"widerspruch": {"n": 1, "median": 0.05,
                                                               "min": 0.05, "max": 0.05}})

    def test_verunreinigte_posts_fallen_aus_wirkungsvergleich(self):
        r = metriken.auswerten({
            "posts": [
                {"id": "p1", "draft": "a b c d e", "veroeffentlicht": "a b c d e"},
                {"id": "p2", "draft": "a b c d e", "veroeffentlicht": "v w x y z"},
            ],
            "kennzahlen": [
                {"id": "p1", "impressionen": 100, "reaktionen": 5, "kommentare": 0, "reposts": 0},
                {"id": "p2", "impressionen": 100, "reaktionen": 50, "kommentare": 0, "reposts": 0},
            ],
            "toene": [{"id": "p1", "ton": "B", "experiment": True},
                      {"id": "p2", "ton": "B", "experiment": True}],
        })
        b = r["ton_vergleich"]["B"]
        self.assertEqual(b["posts"], 2)
        self.assertEqual(b["durchgefallen_bei_matthias"], 1)
        self.assertEqual(b["engagement_rate"]["n"], 1)
        self.assertEqual(b["engagement_rate"]["median"], 0.05)


if __name__ == "__main__":
    unittest.main()
