/* Greitieji įrankiai: keitiklis, palyginimas, paskutinis puodelis, laikmatis, sekiklis, kofeinas organizme.
   Duomenys: window.ARBATA_DATA (assets/data.js, generuojamas iš caff.py). Tekstai: <script id="i18n">. */
(function () {
  var root = document.getElementById('tool');
  if (!root || !window.ARBATA_DATA) return;
  var D = window.ARBATA_DATA;
  var T = JSON.parse(document.getElementById('i18n').textContent);
  var lang = document.documentElement.lang || 'lt';
  var kind = root.getAttribute('data-tool');
  var body = document.getElementById('tool-body');
  var extra = document.getElementById('tool-extra');
  var $ = function (id) { return document.getElementById(id); };
  var byId = {};
  D.drinks.forEach(function (d) { byId[d.id] = d; });
  var TEAS = D.drinks.filter(function (d) { return d.group === 'tea'; });

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function num(n) { var x = String(n); return lang === 'en' ? x : x.replace('.', ','); }
  function r1(x) { return Math.round(x * 10) / 10; }
  function nm(d) { return d.names[lang]; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function hhmm(min) { min = ((Math.round(min) % 1440) + 1440) % 1440; return pad(Math.floor(min / 60)) + ':' + pad(min % 60); }
  function parseHM(v, def) { var m = /^(\d{1,2}):?(\d{2})$/.exec(v || ''); if (!m) return def; var h = +m[1], mi = +m[2]; return h < 24 && mi < 60 ? h * 60 + mi : def; }
  function pills(attr, items, cur) {
    return items.map(function (i) { return '<button type="button" ' + attr + '="' + esc(i[0]) + '" aria-pressed="' + (String(i[0]) === String(cur) ? 'true' : 'false') + '">' + esc(i[1]) + '</button>'; }).join('');
  }
  function select(id, list, cur) {
    return '<select class="sel" id="' + id + '">' + list.map(function (d) { return '<option value="' + d.id + '"' + (d.id === cur ? ' selected' : '') + '>' + esc(nm(d)) + '</option>'; }).join('') + '</select>';
  }
  function setPressed(sel, attr, val) {
    var els = root.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++) els[i].setAttribute('aria-pressed', els[i].getAttribute(attr) === String(val) ? 'true' : 'false');
  }
  function stepper(idDec, idInc, idOut) {
    return '<div class="stepper"><button type="button" id="' + idDec + '" aria-label="−">−</button><output id="' + idOut + '"></output><button type="button" id="' + idInc + '" aria-label="+">+</button></div>';
  }
  function localISO(dt) { dt = dt || new Date(); return dt.getFullYear() + '-' + pad(dt.getMonth() + 1) + '-' + pad(dt.getDate()); }
  var Q = new URLSearchParams(location.search);
  function pick(name, allowed, def) { var v = Q.get(name); return allowed.indexOf(v) >= 0 ? v : def; }
  var params = null; // funkcija, grąžinanti ?query
  function sync() {
    if (!params) return;
    var qs = params();
    try { history.replaceState(null, '', qs); } catch (e) {}
    var u = $('share-url');
    if (u) u.value = location.origin + location.pathname + qs;
  }
  var ids = D.drinks.map(function (d) { return d.id; });
  var coffeeIds = ['espresso', 'filter'];
  var teaIds = TEAS.map(function (d) { return d.id; });

  // ---------- 1. keitiklis ----------
  function convert() {
    var s = { k: pick('k', coffeeIds, 'filter'), c: Math.min(10, Math.max(1, parseInt(Q.get('c'), 10) || 3)), tea: pick('tea', teaIds, 'black') };
    body.innerHTML =
      '<div class="tool-in">' +
      '<div class="fld"><span class="fld-label">' + esc(T.coffee_kind) + '</span><div class="pills">' + pills('data-k', coffeeIds.map(function (i) { return [i, nm(byId[i])]; }), s.k) + '</div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.cups) + '</span>' + stepper('c-dec', 'c-inc', 'c-out') + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.target) + '</span><div class="pills">' + pills('data-tea', TEAS.map(function (d) { return [d.id, nm(d)]; }), s.tea) + '</div></div></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.result) + '</span><div style="margin-top:6px"><span class="big" id="r-big"></span></div><span class="per" id="r-sub"></span></div>' +
      '<div class="bars"><div class="bar-top"><span>' + esc(T.out_coffee) + '</span><b id="r-cof"></b></div><div class="bar-top"><span>' + esc(T.out_tea) + '</span><b id="r-tea"></b></div></div>' +
      '<p class="tool-note" style="color:var(--leaf-2)">' + esc(T.note_limit) + '</p></div>';
    function render() {
      var cof = byId[s.k], tea = byId[s.tea];
      var tl = cof.lo * s.c, th = cof.hi * s.c, tt = cof.typ * s.c;
      var mid = Math.max(1, Math.round(tt / tea.typ * 2) / 2);
      var lo = Math.max(0.5, Math.round(tt / tea.hi * 2) / 2), hi = Math.round(tt / tea.lo * 2) / 2;
      $('c-out').textContent = s.c;
      $('r-big').textContent = num(mid);
      $('r-sub').textContent = T.out_eq + ' (' + T.range + ' ' + num(lo) + '–' + num(hi) + ')';
      $('r-cof').textContent = tl + '–' + th + ' mg';
      $('r-tea').textContent = tea.lo + '–' + tea.hi + ' mg';
      setPressed('[data-k]', 'data-k', s.k); setPressed('[data-tea]', 'data-tea', s.tea);
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-k')) s.k = b.getAttribute('data-k');
      else if (b.hasAttribute('data-tea')) s.tea = b.getAttribute('data-tea');
      else if (b.id === 'c-dec') s.c = Math.max(1, s.c - 1);
      else if (b.id === 'c-inc') s.c = Math.min(10, s.c + 1);
      else return;
      render(); sync();
    });
    params = function () { return '?k=' + s.k + '&c=' + s.c + '&tea=' + s.tea; };
    render();
  }

  // ---------- 2. palyginimas ----------
  function compare() {
    var s = { a: pick('a', ids, 'filter'), b: pick('b', ids, 'black') };
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><label class="fld-label" for="sa">' + esc(T.a) + '</label>' + select('sa', D.drinks, s.a) + '</div>' +
      '<div class="fld"><label class="fld-label" for="sb">' + esc(T.b) + '</label>' + select('sb', D.drinks, s.b) + '</div>' +
      '<div id="tbl"></div></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.result) + '</span><div style="margin-top:6px"><span class="big" id="r-big" style="font-size:40px;line-height:1.1"></span></div></div>' +
      '<div class="bars" id="r-bars"></div></div>';
    function row(label, a, b) { return '<tr><th scope="row">' + esc(label) + '</th><td>' + a + '</td><td>' + b + '</td></tr>'; }
    function render() {
      var A = byId[s.a], B = byId[s.b];
      var rg = function (d) { return d.lo === d.hi ? d.lo + ' mg' : d.lo + '–' + d.hi + ' mg'; };
      var p100 = function (d) { return num(r1(d.typ / d.ml * 100)); };
      $('tbl').innerHTML = '<table class="cmp"><thead><tr><th></th><th>' + esc(nm(A)) + '</th><th>' + esc(nm(B)) + '</th></tr></thead><tbody>' +
        row(T.per_cup, rg(A), rg(B)) + row(T.volume, A.ml + ' ml', B.ml + ' ml') + row(T.per100, p100(A), p100(B)) + '</tbody></table>';
      var ratio = A.typ / B.typ, txt;
      if (ratio > 0.85 && ratio < 1.18) txt = T.ratio_same;
      else if (ratio >= 1) txt = T.ratio_pre + ' ' + nm(A) + ' – ' + num(r1(ratio)) + ' ' + T.ratio_mid + ' ' + nm(B);
      else txt = T.ratio_pre + ' ' + nm(B) + ' – ' + num(r1(1 / ratio)) + ' ' + T.ratio_mid + ' ' + nm(A);
      $('r-big').textContent = txt;
      var max = Math.max(A.hi, B.hi, 1);
      function bar(d, me) { return '<div><div class="bar-top"><span>' + esc(nm(d)) + '</span><b>' + rg(d) + '</b></div><div class="bar"><i class="' + (me ? 'me' : '') + '" style="width:' + Math.max(2, Math.round(d.typ / max * 100)) + '%"></i></div></div>'; }
      $('r-bars').innerHTML = bar(A, true) + bar(B, false);
    }
    root.addEventListener('change', function (e) {
      if (e.target.id === 'sa') s.a = e.target.value; else if (e.target.id === 'sb') s.b = e.target.value; else return;
      render(); sync();
    });
    params = function () { return '?a=' + s.a + '&b=' + s.b; };
    render();
  }

  // ---------- 3. paskutinis puodelis ----------
  function lastcup() {
    var TH = [25, 50, 100];
    var s = { b: parseHM(Q.get('b'), 23 * 60), d: pick('d', ids, 'filter'), s: Math.min(2, Math.max(0, parseInt(Q.get('s'), 10) || 1)) };
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><label class="fld-label" for="bt">' + esc(T.bedtime) + '</label><input class="sel" type="time" id="bt" value="' + hhmm(s.b) + '"></div>' +
      '<div class="fld"><label class="fld-label" for="sd">' + esc(T.drink) + '</label>' + select('sd', D.drinks, s.d) + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.sens) + '</span><div class="pills">' + pills('data-s', T.sens_names.map(function (n, i) { return [i, n]; }), s.s) + '</div></div></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.result) + '</span><div style="margin-top:6px"><span class="small" id="r-pre" style="color:var(--leaf)"></span><br><span class="big" id="r-big"></span></div><span class="per" id="r-sub"></span></div>' +
      '<p class="tool-note" style="color:var(--leaf-2)">' + esc(T.method) + '</p></div>';
    function render() {
      var mg = byId[s.d].typ, thr = TH[s.s];
      setPressed('[data-s]', 'data-s', s.s);
      if (mg <= thr) { $('r-pre').textContent = ''; $('r-big').textContent = '✓'; $('r-sub').textContent = T.out_any; return; }
      var f = Math.log(mg / thr) / Math.LN2; // pusėjimo trukmių skaičius
      var mid = s.b - 5 * f * 60, early = s.b - 7 * f * 60, late = s.b - 3 * f * 60;
      $('r-pre').textContent = T.out_pre;
      $('r-big').textContent = hhmm(mid);
      $('r-sub').textContent = T.out_range + ' ' + hhmm(early) + ' ' + T.out_to + ' ' + hhmm(late);
    }
    root.addEventListener('input', function (e) { if (e.target.id === 'bt') { s.b = parseHM(e.target.value, s.b); render(); sync(); } });
    root.addEventListener('change', function (e) { if (e.target.id === 'sd') { s.d = e.target.value; render(); sync(); } });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-s]'); if (!b) return;
      s.s = +b.getAttribute('data-s'); render(); sync();
    });
    params = function () { return '?b=' + hhmm(s.b).replace(':', '') + '&d=' + s.d + '&s=' + s.s; };
    render();
  }

  // ---------- 4. laikmatis ----------
  function timer() {
    var tl = teaIds.filter(function (i) { return i !== 'matcha'; });
    var s = { tea: pick('tea', tl, 'black'), m: Math.min(5, Math.max(2, parseInt(Q.get('m'), 10) || 4)) };
    var left = 0, running = false, tick = null, endAt = 0;
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><span class="fld-label">' + esc(T.drink) + '</span><div class="pills">' + pills('data-tea', tl.map(function (i) { return [i, nm(byId[i])]; }), s.tea) + '</div></div>' +
      '<div class="fld"><label class="fld-label" for="tm">' + esc(T.steeping) + ': <b id="tm-v"></b></label><input type="range" id="tm" min="2" max="5" step="1" value="' + s.m + '" style="width:100%"></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.temp_hint) + ': <b id="tp"></b></span></div></div>' +
      '<div class="tool-out"><div><span class="eyebrow" id="r-label">' + esc(T.est) + '</span><div style="margin-top:6px"><span class="big" id="r-est"></span> <span class="unit">mg</span></div></div>' +
      '<div><span class="big" id="clock" aria-live="off" style="font-size:72px"></span></div>' +
      '<div class="row-btns"><button class="btn btn-amber" type="button" id="go"></button><button class="btn btn-outline-light" type="button" id="rs">' + esc(T.reset) + '</button></div>' +
      '<p class="tool-note" id="done" style="color:var(--amber-l);font-weight:700" role="status"></p></div>';
    function clock(sec) { return pad(Math.floor(sec / 60)) + ':' + pad(sec % 60); }
    function render() {
      var tea = byId[s.tea], f = D.timeF[s.m];
      $('tm-v').textContent = s.m + ' ' + T.minutes;
      $('tp').textContent = T.temp[s.tea] || '';
      $('r-est').textContent = Math.round(2 * tea.perg[0] * f) + '–' + Math.round(2 * tea.perg[1] * f);
      setPressed('[data-tea]', 'data-tea', s.tea);
      if (!running && left === 0) $('clock').textContent = clock(s.m * 60);
      $('go').textContent = running ? T.pause : (left > 0 ? T.resume : T.start);
    }
    function beep() {
      try {
        var Ctx = window.AudioContext || window.webkitAudioContext, a = new Ctx();
        [0, 0.35, 0.7].forEach(function (t) { var o = a.createOscillator(), g = a.createGain(); o.frequency.value = 880; o.connect(g); g.connect(a.destination); g.gain.setValueAtTime(0.2, a.currentTime + t); o.start(a.currentTime + t); o.stop(a.currentTime + t + 0.2); });
      } catch (e) {}
      try { if (navigator.vibrate) navigator.vibrate([200, 100, 200]); } catch (e) {}
    }
    function stop() { running = false; clearInterval(tick); }
    function step() {
      left = Math.max(0, Math.round((endAt - Date.now()) / 1000));
      $('clock').textContent = clock(left);
      if (left <= 0) { stop(); left = 0; $('done').textContent = T.done; beep(); render(); $('clock').textContent = clock(0); }
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-tea')) { s.tea = b.getAttribute('data-tea'); render(); sync(); return; }
      if (b.id === 'go') {
        if (running) { stop(); render(); return; }
        if (left <= 0) left = s.m * 60;
        $('done').textContent = '';
        endAt = Date.now() + left * 1000; running = true; tick = setInterval(step, 250); step(); render();
      } else if (b.id === 'rs') { stop(); left = 0; $('done').textContent = ''; render(); }
    });
    root.addEventListener('input', function (e) { if (e.target.id === 'tm') { s.m = +e.target.value; if (!running) left = 0; render(); sync(); } });
    params = function () { return '?tea=' + s.tea + '&m=' + s.m; };
    render();
  }

  // ---------- 5. sekiklis ----------
  function tracker() {
    var KEY = 'arbata_tracker_v1';
    var today = localISO();
    var st = { date: today, items: [], profile: 0 };
    var storage = null;
    try { storage = window.localStorage; var raw = storage.getItem(KEY); if (raw) { var p = JSON.parse(raw); if (p && p.date === today && Array.isArray(p.items)) st = p; else if (p) st.profile = p.profile === 1 ? 1 : 0; } } catch (e) { storage = null; }
    st.items = st.items.filter(function (i) { return byId[i.d] && i.n > 0 && i.n <= 20; });
    var pick1 = 'filter', n = 1;
    function save() { try { if (storage) storage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
    var LIM = [D.limits.adult_day, D.limits.pregnancy_day];
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><span class="fld-label">' + esc(T.profile) + '</span><div class="pills">' + pills('data-p', T.profiles.map(function (x, i) { return [i, x]; }), st.profile) + '</div></div>' +
      '<div class="fld"><label class="fld-label" for="sd">' + esc(T.drink) + '</label>' + select('sd', D.drinks, pick1) + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.cups) + '</span><div class="fld-row">' + stepper('n-dec', 'n-inc', 'n-out') + '<button class="btn btn-forest btn-sm" type="button" id="add">' + esc(T.add) + '</button></div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.today) + '</span><ul id="list" class="tlist"></ul><button class="btn btn-outline btn-sm" type="button" id="clr" style="align-self:flex-start">' + esc(T.clear) + '</button></div>' +
      '<span class="small">' + esc(T.save_note) + '</span></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.total) + '</span><div style="margin-top:6px"><span class="big" id="r-big"></span> <span class="unit">mg</span></div><span class="per" id="r-sub"></span></div>' +
      '<div class="bars"><div class="bar-top"><span>' + esc(T.limit) + '</span><b id="r-lim"></b></div><div class="bar"><i class="me" id="r-bar" style="width:0"></i></div><b id="r-state"></b></div>' +
      '<p class="tool-note" id="r-pn" style="color:var(--leaf-2)"></p></div>';
    function render() {
      var lo = 0, hi = 0, typ = 0;
      var html = st.items.map(function (i, idx) {
        var d = byId[i.d]; lo += d.lo * i.n; hi += d.hi * i.n; typ += d.typ * i.n;
        return '<li><span>' + i.n + '× ' + esc(nm(d)) + '</span><button type="button" data-rm="' + idx + '" aria-label="' + esc(T.remove) + '">×</button></li>';
      }).join('');
      $('list').innerHTML = html || '<li class="small">' + esc(T.empty) + '</li>';
      var lim = LIM[st.profile];
      $('r-big').textContent = lo === hi ? lo : lo + '–' + hi;
      $('r-sub').textContent = '';
      $('r-lim').textContent = lim + ' mg';
      $('r-bar').style.width = Math.min(100, Math.round(typ / lim * 100)) + '%';
      $('r-state').textContent = typ >= lim ? T.over : (typ >= lim * 0.75 ? T.near : T.ok);
      $('r-pn').textContent = st.profile === 1 ? T.pregnancy_note : '';
      $('n-out').textContent = n;
      setPressed('[data-p]', 'data-p', st.profile);
    }
    root.addEventListener('change', function (e) { if (e.target.id === 'sd') pick1 = e.target.value; });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-p')) st.profile = +b.getAttribute('data-p');
      else if (b.id === 'n-dec') n = Math.max(1, n - 1);
      else if (b.id === 'n-inc') n = Math.min(10, n + 1);
      else if (b.id === 'add') { st.items.push({ d: pick1, n: n }); n = 1; }
      else if (b.hasAttribute('data-rm')) st.items.splice(+b.getAttribute('data-rm'), 1);
      else if (b.id === 'clr') st.items = [];
      else return;
      save(); render();
    });
    render();
  }

  // ---------- 6. kofeinas organizme ----------
  function bodyChart() {
    var KEY = 'arbata_body_v1';
    var today = localISO();
    var st = { date: today, items: [{ d: 'filter', t: 8 * 60 }, { d: 'filter', t: 13 * 60 }] };
    var storage = null;
    try { storage = window.localStorage; var raw = storage.getItem(KEY); if (raw) { var p = JSON.parse(raw); if (p && p.date === today && Array.isArray(p.items)) st = p; } } catch (e) { storage = null; }
    st.items = st.items.filter(function (i) { return byId[i.d] && i.t >= 0 && i.t < 1440; });
    var pickD = 'filter', pickT = 9 * 60;
    function save() { try { if (storage) storage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><label class="fld-label" for="sd">' + esc(T.drink) + '</label>' + select('sd', D.drinks, pickD) + '</div>' +
      '<div class="fld"><label class="fld-label" for="st">' + esc(T.time) + '</label><div class="fld-row"><input class="sel" type="time" id="st" value="09:00"><button class="btn btn-forest btn-sm" type="button" id="add">' + esc(T.add) + '</button></div></div>' +
      '<ul id="list" class="tlist"></ul><span class="small">' + esc(T.save_note) + '</span></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.peak) + '</span><div style="margin-top:6px"><span class="big" id="r-big"></span> <span class="unit">mg</span></div><span class="per" id="r-sub"></span></div>' +
      '<p class="tool-note" style="color:var(--leaf-2)">' + esc(T.method) + '</p></div>';
    extra.innerHTML = '<div class="chart-card"><svg id="chart" viewBox="0 0 640 280" role="img" aria-label="' + esc(T.h1) + '" preserveAspectRatio="xMidYMid meet"></svg></div>';
    function level(t, h, pick) { // t minutėmis; pick: 'lo'|'typ'|'hi'
      var sum = 0;
      st.items.forEach(function (i) { if (t >= i.t) sum += byId[i.d][pick] * Math.pow(0.5, (t - i.t) / 60 / h); });
      return sum;
    }
    function render() {
      $('list').innerHTML = st.items.map(function (i, idx) {
        return '<li><span>' + hhmm(i.t) + ' · ' + esc(nm(byId[i.d])) + '</span><button type="button" data-rm="' + idx + '" aria-label="' + esc(T.remove) + '">×</button></li>';
      }).join('') || '<li class="small">' + esc(T.empty) + '</li>';
      var X0 = 44, X1 = 608, Y0 = 250, Y1 = 14, TMAX = 30 * 60, step = 10;
      var lines = [], hiL = [], loL = [], peak = 0, peakT = 0, below = null;
      for (var t = 0; t <= TMAX; t += step) {
        var m = level(t, 5, 'typ'), h = level(t, 7, 'hi'), l = level(t, 3, 'lo');
        lines.push([t, m]); hiL.push([t, h]); loL.push([t, l]);
        if (m > peak) { peak = m; peakT = t; }
      }
      for (var k = 0; k < lines.length; k++) { if (lines[k][0] > peakT && lines[k][1] < 50) { below = lines[k][0]; break; } }
      var ymax = Math.max(100, Math.ceil(Math.max.apply(null, hiL.map(function (p) { return p[1]; })) / 50) * 50);
      var sx = function (t) { return X0 + (X1 - X0) * t / TMAX; }, sy = function (v) { return Y0 - (Y0 - Y1) * v / ymax; };
      var path = function (a) { return a.map(function (p, i) { return (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join(''); };
      var band = path(hiL) + loL.slice().reverse().map(function (p) { return 'L' + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join('') + 'Z';
      var grid = '', tx = '';
      for (var hh = 0; hh <= 30; hh += 6) { grid += '<line x1="' + sx(hh * 60) + '" x2="' + sx(hh * 60) + '" y1="' + Y1 + '" y2="' + Y0 + '" class="ch-g"/>'; tx += '<text x="' + sx(hh * 60) + '" y="270" text-anchor="middle" class="ch-t">' + pad(hh % 24) + ':00</text>'; }
      for (var v = 0; v <= ymax; v += ymax / 4) { grid += '<line x1="' + X0 + '" x2="' + X1 + '" y1="' + sy(v) + '" y2="' + sy(v) + '" class="ch-g"/>'; tx += '<text x="' + (X0 - 6) + '" y="' + (sy(v) + 4) + '" text-anchor="end" class="ch-t">' + Math.round(v) + '</text>'; }
      var dots = st.items.map(function (i) { return '<circle cx="' + sx(i.t) + '" cy="' + Y0 + '" r="5" class="ch-d"/>'; }).join('');
      $('chart').innerHTML = grid + '<line x1="' + X0 + '" x2="' + X1 + '" y1="' + sy(50) + '" y2="' + sy(50) + '" class="ch-th"/>' +
        '<path d="' + band + '" class="ch-band"/><path d="' + path(lines) + '" class="ch-line"/>' + dots + tx;
      var pk = Math.round(peak), lo = Math.round(Math.max.apply(null, [0].concat(loL.map(function (p) { return p[1]; })))), hi = Math.round(Math.max.apply(null, hiL.map(function (p) { return p[1]; })));
      $('r-big').textContent = pk;
      $('r-sub').textContent = st.items.length ? (hhmm(peakT) + ' · ' + T.range + ' ' + lo + '–' + hi + ' mg · ' + (below !== null ? T.below + ' ' + hhmm(below) : T.never)) : '';
    }
    root.addEventListener('change', function (e) { if (e.target.id === 'sd') pickD = e.target.value; });
    root.addEventListener('input', function (e) { if (e.target.id === 'st') pickT = parseHM(e.target.value, pickT); });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.id === 'add') { st.items.push({ d: pickD, t: pickT }); st.items.sort(function (a, c) { return a.t - c.t; }); }
      else if (b.hasAttribute('data-rm')) st.items.splice(+b.getAttribute('data-rm'), 1);
      else return;
      save(); render();
    });
    render();
  }

  // ---------- 7. perėjimo planas ----------
  function plan() {
    function addDays(iso, n) { var p = iso.split('-'); var dt = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2] + n)); return dt.toISOString().slice(0, 10); }
    function nextMonday() { var dt = new Date(); var add = (8 - dt.getDay()) % 7 || 7; dt.setDate(dt.getDate() + add); return localISO(dt); }
    function human(iso) { var p = iso.split('-'); try { return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])).toLocaleDateString(lang, { day: 'numeric', month: 'short', timeZone: 'UTC' }); } catch (e) { return iso; } }
    var qs0 = Q.get('start');
    var s = { k: pick('k', coffeeIds, 'filter'), c: Math.min(10, Math.max(1, parseInt(Q.get('c'), 10) || 4)), tea: pick('tea', teaIds, 'black'), w: Math.min(6, Math.max(2, parseInt(Q.get('w'), 10) || 4)), g: ['same', 'less', 'free'].indexOf(Q.get('g')) >= 0 ? Q.get('g') : 'same', start: /^\d{4}-\d{2}-\d{2}$/.test(qs0 || '') ? qs0 : nextMonday() };
    body.innerHTML =
      '<div class="tool-in">' +
      '<div class="fld"><span class="fld-label">' + esc(T.coffee_kind) + '</span><div class="pills">' + pills('data-k', coffeeIds.map(function (i) { return [i, nm(byId[i])]; }), s.k) + '</div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.cups) + '</span>' + stepper('c-dec', 'c-inc', 'c-out') + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.target) + '</span><div class="pills">' + pills('data-tea', TEAS.map(function (d) { return [d.id, nm(d)]; }), s.tea) + '</div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.weeks) + '</span><div class="pills">' + pills('data-w', [2, 3, 4, 5, 6].map(function (x) { return [x, x]; }), s.w) + '</div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.goal) + '</span><div class="pills">' + pills('data-g', [['same', T.g_same], ['less', T.g_less], ['free', T.g_free]], s.g) + '</div><p class="small">' + esc(T.g_note) + '</p></div>' +
      '<div class="fld"><label class="fld-label" for="sd">' + esc(T.start) + '</label><input class="sel" type="date" id="sd" value="' + s.start + '"></div></div>' +
      '<div class="tool-out"><div class="fld-row"><button class="btn btn-amber btn-sm" type="button" id="ics">' + esc(T.ics) + '</button><button class="btn btn-outline-light btn-sm" type="button" id="prn">' + esc(T.print) + '</button></div>' +
      '<p class="tool-note" style="color:var(--leaf-2)">' + esc(T.plan_note) + '</p></div>';
    extra.innerHTML = '<div class="chart-card"><table class="cmp" id="ptbl"></table></div><div class="chart-card"><h3 class="small" style="margin:0 0 8px">' + esc(T.bars) + '</h3><div id="pbars"></div></div><div class="chart-card" id="ptips"></div>';
    function rows() {
      var cof = byId[s.k], tea = byId[s.tea], out = [];
      for (var w = 0; w <= s.w; w++) {
        var cc = w === 0 ? s.c : Math.round(s.c * (1 - w / s.w)), tc = 0, fc = 0;
        if (w > 0) {
          if (s.g === 'same') tc = Math.min(6, Math.round((s.c - cc) * cof.typ / tea.typ));
          else if (s.g === 'less') tc = Math.min(6, s.c - cc);
          else fc = Math.min(6, s.c - cc);
        }
        out.push({ w: w, c: cc, t: tc, f: fc, lo: cc * cof.lo + tc * tea.lo, hi: cc * cof.hi + tc * tea.hi });
      }
      return out;
    }
    function render() {
      $('c-out').textContent = s.c;
      setPressed('[data-k]', 'data-k', s.k); setPressed('[data-tea]', 'data-tea', s.tea); setPressed('[data-w]', 'data-w', s.w); setPressed('[data-g]', 'data-g', s.g);
      var fr = s.g === 'free';
      var h = '<thead><tr><th>' + esc(T.week) + '</th><th>' + esc(T.coffee) + '</th><th>' + esc(fr ? T.free : T.tea) + '</th><th>' + esc(T.mg) + '</th></tr></thead><tbody>';
      rows().forEach(function (r) {
        var label = r.w === 0 ? esc(T.today) : (esc(T.week) + ' ' + r.w + '<br><span class="small">' + esc(human(addDays(s.start, (r.w - 1) * 7))) + '</span>');
        h += '<tr><th scope="row">' + label + '</th><td>' + r.c + '</td><td>' + (fr ? r.f : r.t) + '</td><td>' + r.lo + '–' + r.hi + ' mg</td></tr>';
      });
      $('ptbl').innerHTML = h + '</tbody>';
      var rs = rows(), mx = 400; rs.forEach(function (r) { if (r.hi > mx) mx = r.hi; });
      var b = '';
      rs.forEach(function (r) {
        b += '<div class="pbar"><span class="pbar-l">' + (r.w === 0 ? esc(T.today) : esc(T.week) + ' ' + r.w) + '</span><span class="pbar-t"><i class="pbar-hi" style="width:' + (r.hi / mx * 100) + '%"></i><i class="pbar-lo" style="width:' + (r.lo / mx * 100) + '%"></i><em class="pbar-lim" style="left:' + (400 / mx * 100) + '%"></em></span><span class="pbar-v">' + r.lo + '–' + r.hi + '</span></div>';
      });
      $('pbars').innerHTML = b + '<p class="small">' + esc(T.limit) + '</p>' + (mx > 400 ? '<p class="small" style="color:#C77F12">' + esc(T.over) + '</p>' : '');
      var U = T.urls || {};
      function a(k, t) { return U[k] ? '<li><a href="' + U[k] + '" target="_blank" rel="noopener">' + esc(t) + '</a></li>' : ''; }
      $('ptips').innerHTML = '<h3 class="small" style="margin:0 0 8px">' + esc(T.tips_h) + '</h3><ul class="small">' + a('a', T.tip_a) + a('b', T.tip_b) + a('c', T.tip_c) + a('d', T.tip_d) + a('e', T.tip_e) + '</ul>';
    }
    function ymd(iso) { return iso.replace(/-/g, ''); }
    function icsText(x) { return String(x).replace(/\\/g, '\\\\').replace(/;/g, '\;').replace(/,/g, '\\,').replace(/\n/g, '\\n'); }
    function makeIcs() {
      var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Arbata//Plan//EN', 'CALSCALE:GREGORIAN'];
      var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
      rows().forEach(function (r) {
        if (r.w === 0) return;
        var a = addDays(s.start, (r.w - 1) * 7), b = addDays(a, 7);
        var d = (s.g === 'free' ? T.ev_d_f : T.ev_d).replace('{c}', r.c).replace('{t}', r.t).replace('{f}', r.f).replace('{lo}', r.lo).replace('{hi}', r.hi);
        L.push('BEGIN:VEVENT', 'UID:arbata-' + ymd(s.start) + '-w' + r.w + '-' + Math.floor(Math.random() * 1e6) + '@arbata.pajusk.lt', 'DTSTAMP:' + stamp,
          'DTSTART;VALUE=DATE:' + ymd(a), 'DTEND;VALUE=DATE:' + ymd(b), 'SUMMARY:' + icsText(T.ev + ' · ' + T.week + ' ' + r.w), 'DESCRIPTION:' + icsText(d), 'TRANSP:TRANSPARENT', 'END:VEVENT');
      });
      L.push('END:VCALENDAR');
      return L.join('\r\n') + '\r\n';
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-k')) s.k = b.getAttribute('data-k');
      else if (b.hasAttribute('data-tea')) s.tea = b.getAttribute('data-tea');
      else if (b.hasAttribute('data-w')) s.w = +b.getAttribute('data-w');
      else if (b.hasAttribute('data-g')) s.g = b.getAttribute('data-g');
      else if (b.id === 'c-dec') s.c = Math.max(1, s.c - 1);
      else if (b.id === 'c-inc') s.c = Math.min(10, s.c + 1);
      else if (b.id === 'prn') { window.print(); return; }
      else if (b.id === 'ics') {
        var blob = new Blob([makeIcs()], { type: 'text/calendar;charset=utf-8' }), a = document.createElement('a');
        a.href = URL.createObjectURL(blob); a.download = 'arbata-plan.ics'; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000); return;
      } else return;
      render(); sync();
    });
    root.addEventListener('change', function (e) { if (e.target.id === 'sd' && /^\d{4}-\d{2}-\d{2}$/.test(e.target.value)) { s.start = e.target.value; render(); sync(); } });
    params = function () { return '?k=' + s.k + '&c=' + s.c + '&tea=' + s.tea + '&w=' + s.w + '&g=' + s.g + '&start=' + s.start; };
    render();
  }

  // ---------- 8. dienoraštis ----------
  function diary() {
    var KEY = 'arbata_diary_v1', st = { entries: {} }, storage = null;
    try { storage = window.localStorage; var raw = storage.getItem(KEY); if (raw) { var p = JSON.parse(raw); if (p && p.entries && typeof p.entries === 'object') st = p; } } catch (e) { storage = null; }
    function save() { try { if (storage) storage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
    var today = localISO();
    var cur = st.entries[today] || { c: 0, t: 0, e: 3, s: [], n: '' };
    cur = { c: +cur.c || 0, t: +cur.t || 0, e: Math.min(5, Math.max(1, +cur.e || 3)), s: Array.isArray(cur.s) ? cur.s.filter(function (i) { return i >= 0 && i < 4; }) : [], n: String(cur.n || '').slice(0, 280) };
    var armed = false;
    body.innerHTML =
      '<div class="tool-in"><div class="fld"><span class="fld-label">' + esc(T.coffee) + '</span>' + stepper('c-dec', 'c-inc', 'c-out') + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.tea) + '</span>' + stepper('t-dec', 't-inc', 't-out') + '</div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.energy) + '</span><div class="pills">' + pills('data-e', T.lvl.map(function (x, i) { return [i + 1, x]; }), cur.e) + '</div></div>' +
      '<div class="fld"><span class="fld-label">' + esc(T.symptoms) + '</span><div class="pills">' + T.sym.map(function (x, i) { return '<button type="button" data-sy="' + i + '" aria-pressed="false">' + esc(x) + '</button>'; }).join('') + '</div></div>' +
      '<div class="fld"><label class="fld-label" for="nt">' + esc(T.note) + '</label><textarea class="code" id="nt" rows="3" maxlength="280" style="background:#fff;border:1px solid var(--line-2);font-family:inherit;font-size:16px">' + esc(cur.n) + '</textarea></div>' +
      '<div class="fld-row"><button class="btn btn-forest btn-sm" type="button" id="sv">' + esc(T.save) + '</button><span class="small" id="svd" role="status"></span></div>' +
      '<span class="small">' + esc(T.save_note) + '</span></div>' +
      '<div class="tool-out"><div><span class="eyebrow">' + esc(T.streak) + '</span><div style="margin-top:6px"><span class="big" id="r-big"></span></div><span class="per" id="r-sub"></span></div>' +
      '<div><span class="fld-label" style="color:var(--leaf)">' + esc(T.history) + '</span><ul id="hist" class="tlist hist"></ul></div>' +
      '<div class="fld-row"><button class="btn btn-outline-light btn-sm" type="button" id="exp">' + esc(T.export) + '</button><button class="btn btn-outline-light btn-sm" type="button" id="del">' + esc(T.del_) + '</button></div></div>';
    function streak() {
      var n = 0, dt = new Date();
      if (!st.entries[localISO(dt)]) dt.setDate(dt.getDate() - 1);
      for (;;) { var e = st.entries[localISO(dt)]; if (!e || +e.c !== 0) break; n++; dt.setDate(dt.getDate() - 1); }
      return n;
    }
    function keys() { return Object.keys(st.entries).sort().reverse(); }
    function line(k) {
      var e = st.entries[k];
      return k + ' · ' + T.coffee + ' ' + (+e.c || 0) + ' · ' + T.tea + ' ' + (+e.t || 0) + ' · ' + T.energy + ' ' + (+e.e || 0) + '/5' + ((e.s && e.s.length) ? ' · ' + e.s.map(function (i) { return T.sym[i]; }).filter(Boolean).join(', ') : '') + (e.n ? ' · ' + e.n : '');
    }
    function render() {
      $('c-out').textContent = cur.c; $('t-out').textContent = cur.t;
      setPressed('[data-e]', 'data-e', cur.e);
      var sy = root.querySelectorAll('[data-sy]');
      for (var i = 0; i < sy.length; i++) sy[i].setAttribute('aria-pressed', cur.s.indexOf(+sy[i].getAttribute('data-sy')) >= 0 ? 'true' : 'false');
      $('r-big').textContent = streak();
      $('r-sub').textContent = T.days + ': ' + keys().length;
      $('hist').innerHTML = keys().slice(0, 7).map(function (k) { return '<li><span>' + esc(line(k)) + '</span></li>'; }).join('') || '<li class="small">' + esc(T.empty) + '</li>';
      $('del').textContent = armed ? T.confirm : T.del_;
    }
    root.addEventListener('input', function (e) { if (e.target.id === 'nt') cur.n = e.target.value.slice(0, 280); });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.id === 'c-dec') cur.c = Math.max(0, cur.c - 1); else if (b.id === 'c-inc') cur.c = Math.min(10, cur.c + 1);
      else if (b.id === 't-dec') cur.t = Math.max(0, cur.t - 1); else if (b.id === 't-inc') cur.t = Math.min(10, cur.t + 1);
      else if (b.hasAttribute('data-e')) cur.e = +b.getAttribute('data-e');
      else if (b.hasAttribute('data-sy')) { var i = +b.getAttribute('data-sy'), at = cur.s.indexOf(i); if (at >= 0) cur.s.splice(at, 1); else cur.s.push(i); }
      else if (b.id === 'sv') { st.entries[today] = { c: cur.c, t: cur.t, e: cur.e, s: cur.s.slice(), n: cur.n }; save(); render(); $('svd').textContent = T.saved; return; }
      else if (b.id === 'exp') {
        var txt = keys().reverse().map(line).join('\n');
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { b.textContent = T.exported; setTimeout(function () { b.textContent = T.export; }, 2000); });
        return;
      } else if (b.id === 'del') { if (!armed) { armed = true; render(); return; } st.entries = {}; save(); armed = false; cur = { c: 0, t: 0, e: 3, s: [], n: '' }; $('nt').value = ''; }
      else return;
      if (b.id !== 'del') armed = false;
      $('svd').textContent = '';
      render();
    });
    render();
  }

  // ---------- 9. arbatos testas ----------
  function quiz() {
    var QS = T.qs, SC = T.sc, n = QS.length, ans = [], step = 0;
    var qa = Q.get('a');
    if (qa && /^\d+$/.test(qa) && qa.length === n) {
      var okAns = true, tmp = [];
      for (var i = 0; i < n; i++) { var v = +qa.charAt(i); if (v >= QS[i][1].length) okAns = false; tmp.push(v); }
      if (okAns) { ans = tmp; step = n; }
    }
    body.innerHTML = '<div class="tool-in" style="flex:1 1 100%" id="qbox"></div>';
    function result() {
      var scores = TEAS.map(function (d) {
        var tot = 0, per = [];
        for (var q = 0; q < n; q++) { var p = SC[q][ans[q]][d.id] || 0; tot += p; per.push([p, q]); }
        per.sort(function (a, b) { return b[0] - a[0]; });
        return { d: d, tot: tot, per: per };
      }).sort(function (a, b) { return b.tot - a.tot; }).slice(0, 3);
      var h = '<span class="eyebrow">' + esc(T.top) + '</span><ol class="qres">';
      scores.forEach(function (r) {
        var why = r.per.filter(function (x) { return x[0] > 0; }).slice(0, 2).map(function (x) { return QS[x[1]][1][ans[x[1]]]; });
        h += '<li><b>' + esc(nm(r.d)) + '</b><span class="small">' + esc(T.cup) + ': ' + r.d.lo + '–' + r.d.hi + ' mg</span>' +
          (why.length ? '<span>' + esc(T.because) + ' ' + esc(why.join(' · ')) + '</span>' : '') + '</li>';
      });
      $('qbox').innerHTML = h + '</ol><button class="btn btn-outline btn-sm" type="button" id="again" style="align-self:flex-start">' + esc(T.again) + '</button><span class="small">' + esc(T.note_q) + '</span>';
    }
    function render() {
      if (step >= n) { result(); return; }
      var q = QS[step];
      $('qbox').innerHTML = '<span class="eyebrow">' + esc(T.q_of) + ' ' + (step + 1) + ' ' + esc(T.of) + ' ' + n + '</span><h2 style="font-family:var(--display);font-size:24px">' + esc(q[0]) + '</h2>' +
        '<div class="qopts">' + q[1].map(function (o, i) { return '<button type="button" class="qopt" data-o="' + i + '" aria-pressed="' + (ans[step] === i ? 'true' : 'false') + '">' + esc(o) + '</button>'; }).join('') + '</div>' +
        (step > 0 ? '<button class="btn btn-outline btn-sm" type="button" id="qback" style="align-self:flex-start">' + esc(T.back) + '</button>' : '');
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-o')) { ans[step] = +b.getAttribute('data-o'); step++; }
      else if (b.id === 'qback') step = Math.max(0, step - 1);
      else if (b.id === 'again') { ans = []; step = 0; }
      else return;
      render(); sync();
    });
    params = function () { return step >= n ? '?a=' + ans.join('') : ''; };
    render();
  }

  var map = { convert: convert, compare: compare, lastcup: lastcup, timer: timer, tracker: tracker, body: bodyChart, plan: plan, diary: diary, quiz: quiz };
  if (map[kind]) map[kind]();
  sync();

  // ---------- dalijimasis ----------
  var copyBtn = $('copy-btn');
  if (copyBtn) {
    var cl = $('copy-label');
    copyBtn.addEventListener('click', function () {
      var u = $('share-url'), text = u ? u.value : location.href;
      function done() { if (cl) cl.textContent = copyBtn.getAttribute('data-copied'); setTimeout(function () { if (cl) cl.textContent = copyBtn.getAttribute('data-copy'); }, 2500); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { if (u) { u.select(); document.execCommand('copy'); done(); } });
      else if (u) { u.select(); document.execCommand('copy'); done(); }
    });
  }
  var eb = $('embed-btn'), ep = $('embed-panel');
  if (eb && ep) {
    $('embed-code').value = '<iframe src="' + root.getAttribute('data-embed-src') + '" width="100%" height="640" style="border:0" title="' + esc(root.getAttribute('data-title') || '') + '" loading="lazy"></iframe>';
    eb.addEventListener('click', function () {
      var open = ep.hasAttribute('hidden');
      if (open) ep.removeAttribute('hidden'); else ep.setAttribute('hidden', '');
      eb.setAttribute('aria-expanded', open ? 'true' : 'false');
      $('embed-label').textContent = eb.getAttribute(open ? 'data-hide' : 'data-show');
    });
  }
})();
