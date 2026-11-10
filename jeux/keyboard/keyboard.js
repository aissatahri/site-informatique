// keyboard.js - clavier AZERTY interactif (dessiné en HTML/CSS : aucune image, aucun décalage)
// - Mode « Découvrir » : clic sur une zone -> description
// - Mode « Quiz » : trouver la zone demandée
// - Testeur : la touche pressée s'allume sur le clavier
(function () {
  'use strict';

  // ---------- Zones ----------
  var ZONES = {
    'zone-fn': {
      name: 'Les touches de fonction', color: 'Orange',
      desc: 'Rangée du haut : Échap, F1 à F12, Impr écran, Arrêt défil et Pause. Leur rôle dépend du logiciel utilisé (F1 ouvre souvent l\'aide, F5 actualise, F11 passe en plein écran…).'
    },
    'zone-alpha': {
      name: 'Le clavier alphanumérique', color: 'Rouge',
      desc: 'La grande zone centrale : lettres, chiffres, signes de ponctuation, ainsi que Tab, Verr Maj, Maj (Shift), Ctrl, Alt, Alt Gr, Espace, Retour arrière et Entrée.'
    },
    'zone-navi': {
      name: 'Les touches de mouvement du curseur', color: 'Bleue',
      desc: 'Les quatre flèches, ainsi que Inser, Suppr, Début, Fin, Page précédente et Page suivante. Elles servent à déplacer le curseur et à supprimer du texte.'
    },
    'zone-num': {
      name: 'Le pavé numérique', color: 'Violette',
      desc: 'À droite : chiffres 0 à 9, opérations + − × ÷, virgule et Entrée. Il est activé par la touche Verr Num et facilite la saisie de nombres.'
    }
  };
  var ZONE_IDS = Object.keys(ZONES);

  // ---------- Disposition (unités de touche) ----------
  var keys = [];
  function add(zone, code, x, y, w, h, main, top) {
    keys.push({ zone: 'zone-' + zone, code: code, x: x, y: y, w: w || 1, h: h || 1, main: main, top: top || '' });
  }
  var i;

  // Zone des touches de fonction
  add('fn', 'Escape', 0, 0, 1, 1, 'Échap');
  var f = 1, fx = [2, 6.5, 11];
  fx.forEach(function (x0) { for (i = 0; i < 4; i++, f++) add('fn', 'F' + f, x0 + i, 0, 1, 1, 'F' + f); });
  add('fn', 'PrintScreen', 15.5, 0, 1, 1, 'Impr écran');
  add('fn', 'ScrollLock', 16.5, 0, 1, 1, 'Arrêt défil');
  add('fn', 'Pause', 17.5, 0, 1, 1, 'Pause');

  // Clavier alphanumérique
  var row1 = [['Backquote', '', '²'], ['Digit1', '1', '&'], ['Digit2', '2', 'é'], ['Digit3', '3', '"'], ['Digit4', '4', '\''],
    ['Digit5', '5', '('], ['Digit6', '6', '-'], ['Digit7', '7', 'è'], ['Digit8', '8', '_'], ['Digit9', '9', 'ç'],
    ['Digit0', '0', 'à'], ['Minus', '°', ')'], ['Equal', '+', '=']];
  row1.forEach(function (k, n) { add('alpha', k[0], n, 1.5, 1, 1, k[2], k[1]); });
  add('alpha', 'Backspace', 13, 1.5, 2, 1, '⌫ Retour');

  add('alpha', 'Tab', 0, 2.5, 1.5, 1, 'Tab ⇥');
  var row2 = [['KeyQ', 'A'], ['KeyW', 'Z'], ['KeyE', 'E'], ['KeyR', 'R'], ['KeyT', 'T'], ['KeyY', 'Y'], ['KeyU', 'U'],
    ['KeyI', 'I'], ['KeyO', 'O'], ['KeyP', 'P'], ['BracketLeft', '^', '¨'], ['BracketRight', '$', '£']];
  row2.forEach(function (k, n) { add('alpha', k[0], 1.5 + n, 2.5, 1, 1, k[1], k[2]); });
  add('alpha', 'Enter', 13.5, 2.5, 1.5, 2, 'Entrée ↵');

  add('alpha', 'CapsLock', 0, 3.5, 1.5, 1, 'Verr Maj');
  var row3 = [['KeyA', 'Q'], ['KeyS', 'S'], ['KeyD', 'D'], ['KeyF', 'F'], ['KeyG', 'G'], ['KeyH', 'H'], ['KeyJ', 'J'],
    ['KeyK', 'K'], ['KeyL', 'L'], ['Semicolon', 'M'], ['Quote', 'ù', '%'], ['Backslash', '*', 'µ']];
  row3.forEach(function (k, n) { add('alpha', k[0], 1.5 + n, 3.5, 1, 1, k[1], k[2]); });

  add('alpha', 'ShiftLeft', 0, 4.5, 1.25, 1, '⇧ Maj');
  add('alpha', 'IntlBackslash', 1.25, 4.5, 1, 1, '<', '>');
  var row4 = [['KeyZ', 'W'], ['KeyX', 'X'], ['KeyC', 'C'], ['KeyV', 'V'], ['KeyB', 'B'], ['KeyN', 'N'],
    ['KeyM', ',', '?'], ['Comma', ';', '.'], ['Period', ':', '/'], ['Slash', '!', '§']];
  row4.forEach(function (k, n) { add('alpha', k[0], 2.25 + n, 4.5, 1, 1, k[1], k[2]); });
  add('alpha', 'ShiftRight', 12.25, 4.5, 2.75, 1, '⇧ Maj');

  add('alpha', 'ControlLeft', 0, 5.5, 1.25, 1, 'Ctrl');
  add('alpha', 'MetaLeft', 1.25, 5.5, 1.25, 1, '⊞');
  add('alpha', 'AltLeft', 2.5, 5.5, 1.25, 1, 'Alt');
  add('alpha', 'Space', 3.75, 5.5, 6.25, 1, 'Espace');
  add('alpha', 'AltRight', 10, 5.5, 1.25, 1, 'Alt Gr');
  add('alpha', 'MetaRight', 11.25, 5.5, 1.25, 1, '⊞');
  add('alpha', 'ContextMenu', 12.5, 5.5, 1.25, 1, '☰');
  add('alpha', 'ControlRight', 13.75, 5.5, 1.25, 1, 'Ctrl');

  // Touches de mouvement
  add('navi', 'Insert', 15.5, 1.5, 1, 1, 'Inser');
  add('navi', 'Home', 16.5, 1.5, 1, 1, 'Début ↖');
  add('navi', 'PageUp', 17.5, 1.5, 1, 1, 'Pg préc ⇞');
  add('navi', 'Delete', 15.5, 2.5, 1, 1, 'Suppr');
  add('navi', 'End', 16.5, 2.5, 1, 1, 'Fin');
  add('navi', 'PageDown', 17.5, 2.5, 1, 1, 'Pg suiv ⇟');
  add('navi', 'ArrowUp', 16.5, 4.5, 1, 1, '↑');
  add('navi', 'ArrowLeft', 15.5, 5.5, 1, 1, '←');
  add('navi', 'ArrowDown', 16.5, 5.5, 1, 1, '↓');
  add('navi', 'ArrowRight', 17.5, 5.5, 1, 1, '→');

  // Pavé numérique
  add('num', 'NumLock', 19, 1.5, 1, 1, 'Verr Num');
  add('num', 'NumpadDivide', 20, 1.5, 1, 1, '/');
  add('num', 'NumpadMultiply', 21, 1.5, 1, 1, '*');
  add('num', 'NumpadSubtract', 22, 1.5, 1, 1, '−');
  [['7', 2.5], ['4', 3.5], ['1', 4.5]].forEach(function (r) {
    var d = +r[0];
    for (i = 0; i < 3; i++) add('num', 'Numpad' + (d + i), 19 + i, r[1], 1, 1, String(d + i));
  });
  add('num', 'NumpadAdd', 22, 2.5, 1, 2, '+');
  add('num', 'NumpadEnter', 22, 4.5, 1, 2, 'Entrée ↵');
  add('num', 'Numpad0', 19, 5.5, 2, 1, '0');
  add('num', 'NumpadDecimal', 21, 5.5, 1, 1, '.');

  // ---------- Dessin ----------
  var OX = 0.45, OY = 0.45, W = 23.9, H = 7.4, PAD = 0.3;
  var stage = document.getElementById('kb-stage');
  if (!stage) return;

  function pct(v, total) { return (v / total * 100).toFixed(3) + '%'; }
  function place(el, x, y, w, h) {
    el.style.left = pct(x + OX, W);
    el.style.top = pct(y + OY, H);
    el.style.width = pct(w, W);
    el.style.height = pct(h, H);
  }
  stage.style.aspectRatio = W + ' / ' + H;

  var zoneEls = {}, keyEls = {};

  ZONE_IDS.forEach(function (id) {
    var zk = keys.filter(function (k) { return k.zone === id; });
    var x1 = Math.min.apply(null, zk.map(function (k) { return k.x; }));
    var y1 = Math.min.apply(null, zk.map(function (k) { return k.y; }));
    var x2 = Math.max.apply(null, zk.map(function (k) { return k.x + k.w; }));
    var y2 = Math.max.apply(null, zk.map(function (k) { return k.y + k.h; }));
    var z = document.createElement('button');
    z.type = 'button';
    z.className = 'kb-zone ' + id;
    z.setAttribute('data-zone-id', id);
    z.setAttribute('aria-label', ZONES[id].name);
    z.title = ZONES[id].name;
    place(z, x1 - PAD, y1 - PAD, x2 - x1 + 2 * PAD, y2 - y1 + 2 * PAD);
    stage.appendChild(z);
    zoneEls[id] = z;
  });

  keys.forEach(function (k) {
    var el = document.createElement('span');
    el.className = 'kb-key ' + k.zone;
    el.setAttribute('data-code', k.code);
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = (k.top ? '<i>' + k.top + '</i>' : '') + '<b>' + k.main + '</b>';
    if (k.main.length > 2) el.classList.add('kb-long');
    place(el, k.x, k.y, k.w, k.h);
    stage.appendChild(el);
    keyEls[k.code] = el;
  });

  // légende (aussi cliquable)
  var legend = document.getElementById('kb-legend');
  var info = document.getElementById('zone-info');
  var prompt = document.getElementById('kb-prompt');
  ZONE_IDS.forEach(function (id) {
    var li = document.createElement('li');
    li.innerHTML = '<button type="button" class="kb-chip ' + id + '" data-zone-id="' + id + '">' +
      '<span class="kb-dot"></span>' + ZONES[id].name + '</button>';
    legend.appendChild(li);
  });

  // ---------- Modes ----------
  var mode = 'discover';
  var btnDiscover = document.getElementById('mode-discover');
  var btnQuiz = document.getElementById('mode-quiz');
  var quiz = { asked: [], current: null, score: 0, total: 8, done: false };

  function setMode(m) {
    mode = m;
    btnDiscover.classList.toggle('on', m === 'discover');
    btnQuiz.classList.toggle('on', m === 'quiz');
    btnDiscover.setAttribute('aria-pressed', m === 'discover');
    btnQuiz.setAttribute('aria-pressed', m === 'quiz');
    clearMarks();
    if (m === 'discover') {
      prompt.textContent = 'Clique sur une zone colorée du clavier pour la découvrir.';
      renderInfo(null);
    } else {
      startQuiz();
    }
  }
  btnDiscover.addEventListener('click', function () { setMode('discover'); });
  btnQuiz.addEventListener('click', function () { setMode('quiz'); });

  function clearMarks() {
    ZONE_IDS.forEach(function (id) { zoneEls[id].classList.remove('selected', 'good', 'bad'); });
  }

  function renderInfo(id) {
    if (!id) {
      info.innerHTML = '<p class="hint">Choisis une zone pour afficher sa description.</p>';
      return;
    }
    var z = ZONES[id];
    info.innerHTML = '<h3><span class="kb-dot ' + id + '"></span>' + z.name + ' <small>(zone ' + z.color.toLowerCase() + ')</small></h3><p>' + z.desc + '</p>';
  }

  // ---------- Quiz ----------
  function nextQuestion() {
    var pool = ZONE_IDS.filter(function (id) { return id !== quiz.current; });
    quiz.current = pool[Math.floor(Math.random() * pool.length)];
    prompt.innerHTML = '<strong>Question ' + (quiz.asked.length + 1) + ' / ' + quiz.total + ' :</strong> clique sur la zone « ' + ZONES[quiz.current].name + ' ».';
  }
  function startQuiz() {
    quiz = { asked: [], current: null, score: 0, total: 8, done: false };
    info.innerHTML = '<p class="hint">Score : 0 / ' + quiz.total + '</p>';
    nextQuestion();
  }
  function answerQuiz(id) {
    if (quiz.done) return;
    clearMarks();
    var ok = id === quiz.current;
    zoneEls[id].classList.add(ok ? 'good' : 'bad');
    if (!ok) zoneEls[quiz.current].classList.add('good');
    if (ok) quiz.score++;
    quiz.asked.push(quiz.current);
    var msg = ok ? '✅ Bonne réponse !' : '❌ Non : c\'était la zone « ' + ZONES[quiz.current].name + ' ».';
    info.innerHTML = '<p>' + msg + '</p><p class="hint">Score : ' + quiz.score + ' / ' + quiz.total + '</p>';
    if (quiz.asked.length >= quiz.total) {
      quiz.done = true;
      prompt.innerHTML = '<strong>Terminé : ' + quiz.score + ' / ' + quiz.total + '.</strong> ' +
        (quiz.score === quiz.total ? 'Parfait !' : 'Recommence pour t\'améliorer.') +
        ' <button type="button" id="quiz-again" class="secondary">Rejouer</button>';
      document.getElementById('quiz-again').addEventListener('click', startQuiz);
    } else {
      setTimeout(function () { if (mode === 'quiz' && !quiz.done) { clearMarks(); nextQuestion(); } }, 1100);
    }
  }

  function onZone(id) {
    if (mode === 'quiz') { answerQuiz(id); return; }
    clearMarks();
    zoneEls[id].classList.add('selected');
    renderInfo(id);
  }
  stage.addEventListener('click', function (e) {
    var z = e.target.closest('.kb-zone');
    if (z) onZone(z.getAttribute('data-zone-id'));
  });
  legend.addEventListener('click', function (e) {
    var b = e.target.closest('[data-zone-id]');
    if (b && mode === 'discover') onZone(b.getAttribute('data-zone-id'));
  });
  renderInfo(null);

  // ---------- Testeur de touches ----------
  var tester = document.getElementById('kb-tester');
  var result = document.getElementById('kb-result');
  var countEl = document.getElementById('kb-count');
  var totalEl = document.getElementById('kb-total');
  var clearBtn = document.getElementById('kb-clear');
  var found = {};
  totalEl.textContent = keys.length;

  function niceKey(e) {
    var k = e.key;
    var names = { ' ': 'Espace', 'Control': 'Ctrl', 'Shift': 'Maj (Shift)', 'AltGraph': 'Alt Gr', 'Backspace': 'Retour arrière',
      'Delete': 'Suppr', 'Enter': 'Entrée', 'CapsLock': 'Verr Maj', 'Escape': 'Échap', 'Insert': 'Inser',
      'ArrowUp': 'Flèche haut', 'ArrowDown': 'Flèche bas', 'ArrowLeft': 'Flèche gauche', 'ArrowRight': 'Flèche droite',
      'PageUp': 'Page précédente', 'PageDown': 'Page suivante', 'Home': 'Début', 'End': 'Fin', 'NumLock': 'Verr Num',
      'ContextMenu': 'Menu contextuel', 'Meta': 'Windows', 'PrintScreen': 'Impr écran', 'ScrollLock': 'Arrêt défil' };
    return names[k] || k;
  }

  tester.addEventListener('focus', function () { tester.classList.add('active'); });
  tester.addEventListener('blur', function () { tester.classList.remove('active'); });

  tester.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') e.preventDefault(); // évite F5, F1, Alt+… pendant le test
    var el = keyEls[e.code];
    var zone = el ? ZONES[el.className.match(/zone-\w+/)[0]].name : 'touche non représentée';
    if (el) {
      el.classList.add('pressed', 'found');
      if (!found[e.code]) { found[e.code] = true; countEl.textContent = Object.keys(found).length; }
    }
    result.innerHTML = 'Touche : <kbd>' + niceKey(e) + '</kbd> · code <code>' + e.code + '</code> · zone : ' + zone;
  });
  tester.addEventListener('keyup', function (e) {
    var el = keyEls[e.code];
    if (el) el.classList.remove('pressed');
  });
  tester.addEventListener('blur', function () {
    Object.keys(keyEls).forEach(function (c) { keyEls[c].classList.remove('pressed'); });
  });
  clearBtn.addEventListener('click', function () {
    found = {};
    countEl.textContent = '0';
    Object.keys(keyEls).forEach(function (c) { keyEls[c].classList.remove('found', 'pressed'); });
    result.textContent = 'Aucune touche pour le moment.';
  });
})();
