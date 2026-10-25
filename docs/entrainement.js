/* Page d'entraînement : tirage et notation, entièrement dans le navigateur (rien n'est envoyé ni enregistré). Utilise exam.js (Exam.render, Exam.mark, Exam.scoreTable). */
(function () {
  var data = window.TRAINING;
  var LETTERS = "abcdefgh";

  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = a[i];
      a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function rid() { return "d" + Math.random().toString(36).slice(2, 8); }

  /* Tirage : retourne { exam, key } ; key contient les bonnes réponses (jamais affichées avant la fin). */
  function draw(serie) {
    var S = data[serie], key = { ex1: {}, ex2: {}, ex3: {}, ex4: {}, ex5: {} };
    var exam = {};

    var defs = shuffle(S.ex1.map(function (x) { return { id: rid(), text: x.text }; }).map(function (d, i) { d.src = i; return d; }));
    var idOf = {};
    defs.forEach(function (d) { idOf[d.src] = d.id; });
    exam.ex1 = {
      terms: S.ex1.map(function (x, i) { key.ex1["t" + i] = idOf[i]; return { id: "t" + i, label: x.term }; }),
      defs: defs.map(function (d) { return { id: d.id, text: d.text }; })
    };

    exam.ex2 = S.ex2.map(function (x, i) {
      key.ex2["q" + i] = { v: x.a ? "V" : "F", corr: x.corr };
      return { id: "q" + i, text: x.text };
    });

    exam.ex3 = {
      items: S.ex3.items.map(function (x, i) { key.ex3["q" + i] = x.a; return { id: "q" + i, text: x.text }; }),
      bank: shuffle(S.ex3.items.map(function (x) { return x.a; }).concat(S.ex3.distract))
    };

    exam.ex4 = S.ex4.map(function (x, i) {
      key.ex4["q" + i] = { a: String(x.a), kind: x.kind, detail: x.detail };
      return { id: "q" + i, q: x.q, kind: x.kind };
    });

    exam.ex5 = {};
    key.ex5 = {};
    ["s1", "s2"].forEach(function (sk) {
      var s = S.ex5[sk];
      var blanks = s.answers.map(function (a, j) { return sk === "s1" ? String(j + 1) : LETTERS[j]; });
      blanks.forEach(function (tag, j) { key.ex5[sk + "_" + tag] = s.answers[j]; });
      exam.ex5[sk] = { title: s.title, img: s.img, bank: shuffle(s.bank), blanks: blanks };
    });
    return { exam: exam, key: key };
  }

  function round05(x) { return Math.round(x * 2) / 2; }

  /* Nombre au début de la saisie (espaces tolérés) */
  function leadingNumber(s) {
    var m = /^\s*(\d+)/.exec(s || "");
    return m ? m[1] : null;
  }
  function stripZeros(s) { return s.replace(/^0+(?=\d)/, ""); }

  function checkEx4(k, given) {
    var n = leadingNumber(given);
    if (n === null) return false;
    if (k.kind === "dec") return parseInt(n, 10) === parseInt(k.a, 10);
    if (!/^[01]+$/.test(n)) return false;
    if (k.kind === "bin") return stripZeros(n) === stripZeros(k.a);
    return n === k.a; // bin8
  }

  function grade(exam, key, ans) {
    var det = { ex1: {}, ex2: {}, ex3: {}, ex4: {}, ex5: {} };
    var raw = { ex1: 0, ex2: 0, ex3: 0, ex4: 0, ex5: 0 };
    var a = function (ex, k) { return (ans[ex] || {})[k] || ""; };

    Object.keys(key.ex1).forEach(function (k) {
      var ok = a("ex1", k) === key.ex1[k];
      if (ok) raw.ex1 += 1;
      det.ex1[k] = { ok: ok, exp: key.ex1[k] };
    });
    Object.keys(key.ex2).forEach(function (k) {
      var ok = a("ex2", k) === key.ex2[k].v;
      if (ok) raw.ex2 += 0.5;
      det.ex2[k] = { ok: ok, exp: key.ex2[k].v === "V" ? "Vrai" : "Faux", corr: key.ex2[k].corr };
    });
    Object.keys(key.ex3).forEach(function (k) {
      var ok = a("ex3", k) === key.ex3[k];
      if (ok) raw.ex3 += 0.5;
      det.ex3[k] = { ok: ok, exp: key.ex3[k] };
    });
    Object.keys(key.ex4).forEach(function (k) {
      var ok = checkEx4(key.ex4[k], a("ex4", k));
      if (ok) raw.ex4 += 0.5;
      det.ex4[k] = { ok: ok, exp: key.ex4[k].detail };
    });
    Object.keys(key.ex5).forEach(function (k) {
      var ok = a("ex5", k) === key.ex5[k];
      if (ok) raw.ex5 += 0.5;
      det.ex5[k] = { ok: ok, exp: key.ex5[k] };
    });

    var r = { total: 0 };
    Object.keys(raw).forEach(function (ex) { r[ex] = round05(raw[ex]); r.total += r[ex]; });
    return { det: det, r: r };
  }

  /* "_{2}" -> indice, "^{6}" -> exposant, dans les textes affichés (le texte est déjà échappé par exam.js) */
  var SCRIPT_RE = /([_^])\{([^}]*)\}/g;
  function fixScripts(root) {
    var nodes = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false), n;
    while ((n = w.nextNode())) {
      if (n.parentNode.nodeName !== "OPTION" && n.nodeValue.indexOf("{") !== -1) nodes.push(n);
    }
    nodes.forEach(function (node) {
      var txt = node.nodeValue, last = 0, m, frag = document.createDocumentFragment();
      SCRIPT_RE.lastIndex = 0;
      while ((m = SCRIPT_RE.exec(txt))) {
        frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var el = document.createElement(m[1] === "_" ? "sub" : "sup");
        el.textContent = m[2];
        frag.appendChild(el);
        last = m.index + m[0].length;
      }
      if (!last) return;
      frag.appendChild(document.createTextNode(txt.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }

  /* Interface */
  var $ = function (id) { return document.getElementById(id); };
  var current = null, answers = {};

  function show(step) {
    $("step-choice").hidden = step !== "step-choice";
    $("step-exam").hidden = step === "step-choice"; // la correction s'affiche sous le résultat
    $("step-result").hidden = step !== "step-result";
    window.scrollTo(0, 0);
  }

  function start() {
    var serie = document.querySelector('input[name="serie"]:checked').value;
    current = draw(serie);
    current.serie = serie;
    answers = {};
    $("exam-title").textContent = data[serie].title;
    Exam.render($("exam-root"), current.exam, answers, null, false);
    fixScripts($("exam-root"));
    $("finish").hidden = false;
    show("step-exam");
  }

  function finish() {
    var g = grade(current.exam, current.key, answers);
    Exam.render($("exam-root"), current.exam, answers, null, true);
    Exam.mark($("exam-root"), current.exam, g.det);
    fixScripts($("exam-root"));
    $("result-title").textContent = data[current.serie].title;
    $("result-note").innerHTML = "<b>" + Exam.fmt(g.r.total) + "</b> / 20";
    $("result-table").innerHTML = Exam.scoreTable(g.r);
    $("finish").hidden = true;
    show("step-result");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var box = $("series");
    Object.keys(data).forEach(function (k, i) {
      var l = document.createElement("label");
      l.className = "serie";
      l.innerHTML = '<input type="radio" name="serie" value="' + k + '"' + (i === 0 ? " checked" : "") + "><span>" + Exam.esc(data[k].title) + "</span>";
      box.appendChild(l);
    });
    $("start").onclick = start;
    $("finish").onclick = finish;
    $("restart").onclick = start;
    $("change").onclick = function () { show("step-choice"); };
    show("step-choice");
  });
})();
