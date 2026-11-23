// node tools/linkedin-format/linkedin-format.test.js
const assert = require("assert");
const { linkedinFormat } = require("./linkedin-format.js");

let ok = 0;
function fall(name, fn) { fn(); ok++; console.log("ok  " + name); }

fall("fett serif wie im veröffentlichten Post vom 16.09.", () => {
  assert.strictEqual(linkedinFormat("**THE MOST**"), "𝐓𝐇𝐄 𝐌𝐎𝐒𝐓");
});

fall("fett sans", () => {
  assert.strictEqual(linkedinFormat("**Bold 42**", { stil: "sans" }), "𝗕𝗼𝗹𝗱 𝟰𝟮");
});

fall("Umlaute bleiben lesbar (Grundbuchstabe fett + Trema)", () => {
  // 𝐆 𝐫 𝐨+Trema ß 𝐞
  assert.strictEqual(linkedinFormat("**Größe**"), "𝐆𝐫\u{1D428}̈ß𝐞");
});

fall("kursiv mit Ausnahme h", () => {
  assert.strictEqual(linkedinFormat("*the*"), "𝑡ℎ𝑒");
});

fall("snake_case und URLs bleiben unangetastet", () => {
  const t = "see https://example.com/a_b_c and my_var_name";
  assert.strictEqual(linkedinFormat(t), t);
});

fall("Aufzählung, Überschrift, Link, Escapes", () => {
  const ein = "# Titel\n\n\\- eins\n- zwei\n\n[Quelle](https://x.org/p)";
  const aus = linkedinFormat(ein);
  assert.strictEqual(aus, "𝐓𝐢𝐭𝐞𝐥\n\n• eins\n• zwei\n\nQuelle (https://x.org/p)");
});

fall("mehrfache Leerzeilen werden zu einer", () => {
  assert.strictEqual(linkedinFormat("a\n\n\n\nb"), "a\n\nb");
});

fall("Text ohne Markdown bleibt gleich", () => {
  const t = "Look at the last vendor number you repeated. Who measured it?";
  assert.strictEqual(linkedinFormat(t), t);
});

console.log(`\n${ok} Tests grün`);
