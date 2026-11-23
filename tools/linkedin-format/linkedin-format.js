/*
 * LinkedIn-Formatter — Markdown-Draft in LinkedIn-taugliche Zeichen umwandeln.
 *
 * LinkedIn kennt keine Formatierung. Beim Einfügen wird HTML verworfen; übrig bleibt
 * reiner Text. Online-Formatter "fetten" deshalb, indem sie Buchstaben durch
 * mathematische Unicode-Zeichen ersetzen (𝐁𝐨𝐥𝐝). Genau das macht diese Datei —
 * ohne Abhängigkeiten, damit sie unverändert ins Cockpit-Artefakt passt.
 *
 * Grenzen, die man kennen sollte:
 *  - Screenreader lesen 𝐁𝐨𝐥𝐝 oft Buchstabe für Buchstabe oder gar nicht vor, und die
 *    LinkedIn-Suche findet fettgesetzte Wörter nicht. Deshalb sparsam: erste Zeile.
 *  - ß und Satzzeichen haben keine Fettvariante und bleiben normal.
 *  - Umlaute werden als Grundbuchstabe + Trema (U+0308) gesetzt; das rendert auf
 *    LinkedIn ordentlich, kann aber in manchen Schriften leicht versetzt aussehen.
 *
 * Nutzung:  linkedinFormat(text, { stil: "serif" | "sans" })  -> String
 */
(function (global) {
  "use strict";

  const STILE = {
    serif: { fettGross: 0x1d400, fettKlein: 0x1d41a, fettZiffer: 0x1d7ce,
             kursivGross: 0x1d434, kursivKlein: 0x1d44e },
    sans:  { fettGross: 0x1d5d4, fettKlein: 0x1d5ee, fettZiffer: 0x1d7ec,
             kursivGross: 0x1d608, kursivKlein: 0x1d622 }
  };

  // Lücken im Unicode-Block "Mathematical Italic": h liegt woanders.
  const KURSIV_AUSNAHMEN = { serif: { h: 0x210e }, sans: {} };

  function zeichenUmsetzen(text, art, stil) {
    const t = STILE[stil];
    // NFD trennt ä in a + U+0308: der Grundbuchstabe wird umgesetzt, das Trema bleibt.
    let raus = "";
    for (const z of text.normalize("NFD")) {
      const c = z.codePointAt(0);
      let neu = null;
      if (c >= 65 && c <= 90) {
        neu = (art === "fett" ? t.fettGross : t.kursivGross) + (c - 65);
      } else if (c >= 97 && c <= 122) {
        if (art === "kursiv" && KURSIV_AUSNAHMEN[stil][z]) neu = KURSIV_AUSNAHMEN[stil][z];
        else neu = (art === "fett" ? t.fettKlein : t.kursivKlein) + (c - 97);
      } else if (c >= 48 && c <= 57 && art === "fett") {
        neu = t.fettZiffer + (c - 48);
      }
      raus += neu === null ? z : String.fromCodePoint(neu);
    }
    return raus;
  }

  function zeileFormatieren(zeile, stil) {
    // Escapes, wie sie Drive-Markdown manchmal liefert: \- \# \* \_
    let z = zeile.replace(/\\([-#*_[\]()])/g, "$1");

    // Überschrift -> fette Zeile
    const h = z.match(/^\s{0,3}#{1,6}\s+(.*)$/);
    if (h) return zeichenUmsetzen(h[1].trim(), "fett", stil);

    // Aufzählung
    z = z.replace(/^(\s*)[-*+]\s+/, "$1• ");

    // Links: [Text](URL) -> Text (URL)
    z = z.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, "$1 ($2)");

    // ***fettkursiv*** zuerst, dann **fett**, dann *kursiv* / _kursiv_
    z = z.replace(/\*\*\*([^*]+)\*\*\*/g, (_, s) => zeichenUmsetzen(s, "fett", stil));
    z = z.replace(/\*\*([^*]+)\*\*/g, (_, s) => zeichenUmsetzen(s, "fett", stil));
    z = z.replace(/__([^_]+)__/g, (_, s) => zeichenUmsetzen(s, "fett", stil));
    // Kursiv nur an Wortgrenzen, damit snake_case und URLs heil bleiben.
    z = z.replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:!?]|$)/g,
                  (_, vor, s) => vor + zeichenUmsetzen(s, "kursiv", stil));
    z = z.replace(/(^|[\s(])_([^_\s][^_]*?)_(?=[\s).,;:!?]|$)/g,
                  (_, vor, s) => vor + zeichenUmsetzen(s, "kursiv", stil));
    return z;
  }

  function linkedinFormat(text, optionen) {
    const stil = (optionen && optionen.stil === "sans") ? "sans" : "serif";
    const zeilen = String(text || "").replace(/\r\n?/g, "\n").split("\n")
      .map(z => zeileFormatieren(z, stil).replace(/[ \t]+$/, ""));
    // LinkedIn zeigt Leerzeilen; mehr als eine am Stück wirkt kaputt.
    return zeilen.join("\n").replace(/\n{3,}/g, "\n\n").trim();
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { linkedinFormat, zeichenUmsetzen };
  } else {
    global.linkedinFormat = linkedinFormat;
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
