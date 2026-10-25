/* Affichage commun d'une épreuve (contrôle surveillé ou série de révision) : aucune rédaction, uniquement des clics et des nombres. */
var Exam = (function () {
  var LET = "ABCDEFGH";
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function render(root, exam, ans, onChange, ro) {
    var h = "";
    var a = function (ex, k) { return (ans[ex] || {})[k] || ""; };
    function sel(ex, k, options, ph) {
      var cur = a(ex, k);
      var s = '<select data-ex="' + ex + '" data-k="' + k + '"' + (ro ? " disabled" : "") + '><option value="">' + ph + "</option>";
      options.forEach(function (o) { s += '<option value="' + esc(o[0]) + '"' + (cur === o[0] ? " selected" : "") + ">" + esc(o[1]) + "</option>"; });
      return s + "</select>";
    }
    function q(ex, k, label, control) {
      return '<div class="q" data-q="' + ex + ":" + k + '"><span class="lab">' + label + "</span>" + control + '<div class="note"></div></div>';
    }
    // Exercice 1
    h += '<section class="ex"><h2>Exercice 1 — Définitions <span class="pts">4 points</span></h2>' +
      '<p class="cons">Associe chaque terme à la définition qui lui correspond (une définition par terme).</p><div class="defs">';
    exam.ex1.defs.forEach(function (d, i) { h += '<div class="def"><b>' + LET[i] + "</b><span>" + esc(d.text) + "</span></div>"; });
    h += '</div><div class="grid">';
    var o1 = exam.ex1.defs.map(function (d, i) { return [d.id, "Définition " + LET[i]]; });
    exam.ex1.terms.forEach(function (t) { h += q("ex1", t.id, esc(t.label), sel("ex1", t.id, o1, "— choisir —")); });
    h += "</div></section>";
    // Exercice 2
    h += '<section class="ex"><h2>Exercice 2 — Vrai ou Faux <span class="pts">4 points</span></h2><p class="cons">Clique sur Vrai ou sur Faux.</p>';
    exam.ex2.forEach(function (x, i) {
      var cur = a("ex2", x.id);
      var vf = '<div class="vf" data-ex="ex2" data-k="' + x.id + '"><button type="button" data-v="V"' + (cur === "V" ? ' class="on"' : "") + (ro ? " disabled" : "") +
        '>Vrai</button><button type="button" data-v="F"' + (cur === "F" ? ' class="on"' : "") + (ro ? " disabled" : "") + ">Faux</button></div>";
      h += q("ex2", x.id, "<b>" + (i + 1) + ".</b> " + esc(x.text), vf);
    });
    h += "</section>";
    // Exercice 3
    h += '<section class="ex"><h2>Exercice 3 — Donne le terme <span class="pts">3 points</span></h2><p class="cons">Choisis le terme qui correspond à chaque définition (attention : certains termes de la liste sont en trop).</p>';
    var o3 = exam.ex3.bank.map(function (t) { return [t, t]; });
    exam.ex3.items.forEach(function (x, i) { h += q("ex3", x.id, "<b>" + (i + 1) + ".</b> " + esc(x.text), sel("ex3", x.id, o3, "— terme —")); });
    h += "</section>";
    // Exercice 4
    h += '<section class="ex"><h2>Exercice 4 — Conversions et calculs <span class="pts">4 points</span></h2>' +
      '<p class="cons">Écris uniquement le résultat (un nombre). En binaire, écris seulement des 0 et des 1. Pas besoin d\'écrire l\'unité.</p>';
    exam.ex4.forEach(function (x, i) {
      var ph = x.kind === "dec" ? "résultat (nombre)" : x.kind === "bin8" ? "8 chiffres 0/1" : "binaire";
      h += q("ex4", x.id, "<b>" + "abcdefgh"[i] + ")</b> " + esc(x.q),
        '<input type="text" data-ex="ex4" data-k="' + x.id + '" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="' + ph + '" value="' + esc(a("ex4", x.id)) + '"' + (ro ? " disabled" : "") + ">");
    });
    h += "</section>";
    // Exercice 5
    h += '<section class="ex"><h2>Exercice 5 — Schémas fonctionnels <span class="pts">5 points</span></h2><p class="cons">Complète les cases numérotées (ou lettrées) de chaque schéma en choisissant l\'élément correct.</p>';
    ["s1", "s2"].forEach(function (sk) {
      var S = exam.ex5[sk];
      var ob = S.bank.map(function (t) { return [t, t]; });
      h += '<h3>' + esc(S.title) + '</h3><img class="schema" src="' + S.img + '" alt="' + esc(S.title) + '"><div class="grid">';
      S.blanks.forEach(function (tag) { h += q("ex5", sk + "_" + tag, "Case <b>" + tag + "</b>", sel("ex5", sk + "_" + tag, ob, "— élément —")); });
      h += "</div>";
    });
    h += "</section>";
    root.innerHTML = h;

    if (ro) return;
    function set(ex, k, v) {
      ans[ex] = ans[ex] || {};
      if (v === "" || v == null) delete ans[ex][k]; else ans[ex][k] = v;
      if (onChange) onChange();
    }
    root.onchange = function (e) { var t = e.target; if (t.tagName === "SELECT") set(t.dataset.ex, t.dataset.k, t.value); };
    root.oninput = function (e) { var t = e.target; if (t.tagName === "INPUT") set(t.dataset.ex, t.dataset.k, t.value); };
    root.onclick = function (e) {
      var b = e.target.closest ? e.target.closest(".vf button") : null;
      if (!b) return;
      var box = b.parentNode, v = b.dataset.v;
      var already = b.classList.contains("on");
      Array.prototype.forEach.call(box.children, function (x) { x.classList.remove("on"); });
      if (!already) b.classList.add("on");
      set(box.dataset.ex, box.dataset.k, already ? "" : v);
    };
  }

  /* Affiche la correction détaillée sur une épreuve rendue en lecture seule. */
  function mark(root, exam, det) {
    Object.keys(det).forEach(function (ex) {
      Object.keys(det[ex]).forEach(function (k) {
        var d = det[ex][k];
        var box = root.querySelector('[data-q="' + ex + ":" + k + '"]');
        if (!box) return;
        box.classList.add(d.ok ? "ok" : "ko");
        var exp = d.exp;
        if (ex === "ex1") { var i = exam.ex1.defs.findIndex(function (x) { return x.id === exp; }); exp = "Définition " + LET[i]; }
        var n = box.querySelector(".note");
        if (d.ok) { n.innerHTML = "✓ Correct"; }
        else {
          n.innerHTML = "✗ Réponse attendue : <b>" + esc(exp) + "</b>" + (d.corr ? '<div class="why">' + esc(d.corr) + "</div>" : "");
        }
      });
    });
  }

  function fmt(x) { return String(x).replace(".", ","); }
  function scoreTable(r) {
    var names = { ex1: ["Ex. 1 — Définitions", 4], ex2: ["Ex. 2 — Vrai/Faux", 4], ex3: ["Ex. 3 — Termes", 3], ex4: ["Ex. 4 — Conversions", 4], ex5: ["Ex. 5 — Schémas", 5] };
    var h = '<table class="score"><tbody>';
    Object.keys(names).forEach(function (k) { h += "<tr><td>" + names[k][0] + "</td><td>" + fmt(r[k]) + " / " + names[k][1] + "</td></tr>"; });
    return h + '<tr class="tot"><td>TOTAL</td><td>' + fmt(r.total) + " / 20</td></tr></tbody></table>";
  }

  return { render: render, mark: mark, scoreTable: scoreTable, fmt: fmt, esc: esc };
})();
