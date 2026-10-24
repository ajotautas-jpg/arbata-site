/* Kofeino skaičiuoklė: veikia ir pilname puslapyje, ir įterpiamoje versijoje.
   Duomenys (mg / g sausos arbatos) paimami iš mygtukų atributų, kuriuos sugeneruoja build.py. */
(function () {
  var root = document.getElementById('calc');
  if (!root) return;
  var lang = document.documentElement.lang || 'lt';
  var TIME_F = { 2: 0.65, 3: 0.85, 4: 0.93, 5: 1 };
  var MAX_BAR = 120;
  var FILTER = 96;

  var teaBtns = root.querySelectorAll('[data-tea]');
  var timeBtns = root.querySelectorAll('[data-time]');
  var $ = function (id) { return document.getElementById(id); };

  var s = { tea: teaBtns.length ? teaBtns[0].getAttribute('data-tea') : 'black', g: 2, ml: 250, m: 4 };

  // būsena iš nuorodos
  try {
    var q = new URLSearchParams(location.search);
    var tea = q.get('tea');
    for (var i = 0; i < teaBtns.length; i++) if (teaBtns[i].getAttribute('data-tea') === tea) s.tea = tea;
    var g = parseFloat(q.get('g'));
    if (g >= 0.5 && g <= 10) s.g = Math.round(g * 2) / 2;
    var ml = parseInt(q.get('ml'), 10);
    if (ml >= 100 && ml <= 500) s.ml = Math.round(ml / 50) * 50;
    var m = parseInt(q.get('m'), 10);
    if (TIME_F[m]) s.m = m;
  } catch (e) {}

  function fmt(n) {
    var x = String(n);
    return lang === 'en' ? x : x.replace('.', ',');
  }
  function teaData() {
    for (var i = 0; i < teaBtns.length; i++) {
      var b = teaBtns[i];
      if (b.getAttribute('data-tea') === s.tea) {
        return { lo: Number(b.getAttribute('data-lo')), hi: Number(b.getAttribute('data-hi')), whole: b.getAttribute('data-whole') === '1' };
      }
    }
    return { lo: 7, hi: 24, whole: false };
  }
  function setPressed(list, attr, val) {
    for (var i = 0; i < list.length; i++) {
      list[i].setAttribute('aria-pressed', String(list[i].getAttribute(attr)) === String(val) ? 'true' : 'false');
    }
  }
  function pct(v) { return Math.min(100, Math.round(v / MAX_BAR * 100)) + '%'; }
  function setText(id, txt) { var e = $(id); if (e) e.textContent = txt; }

  function render() {
    var d = teaData();
    var f = d.whole ? 1 : TIME_F[s.m];
    var lo = Math.round(s.g * d.lo * f);
    var hi = Math.round(s.g * d.hi * f);
    var mid = (lo + hi) / 2;

    setPressed(teaBtns, 'data-tea', s.tea);
    setPressed(timeBtns, 'data-time', s.m);
    setText('o-grams', fmt(s.g) + ' g');
    setText('o-water', s.ml + ' ml');
    setText('o-range', lo + '–' + hi);

    var per = $('o-per');
    if (per) {
      var a = Math.round(lo / s.ml * 100 * 10) / 10;
      var b = Math.round(hi / s.ml * 100 * 10) / 10;
      per.textContent = '≈ ' + fmt(a) + '–' + fmt(b) + ' mg / 100 ml';
    }
    var vs = $('o-vs');
    if (vs) vs.textContent = '≈ ' + Math.round(mid / FILTER * 100) + '% ' + (vs.getAttribute('data-vs') || '');

    var barCup = $('bar-cup');
    if (barCup) {
      barCup.style.width = pct(mid);
      setText('bar-cup-v', lo + '–' + hi + ' mg');
    }

    // nuoroda su pasirinkimais
    var qs = '?tea=' + s.tea + '&g=' + s.g + '&ml=' + s.ml + '' + '&m=' + s.m;
    try { history.replaceState(null, '', qs); } catch (e) {}
    var url = $('share-url');
    if (url) url.value = location.origin && location.origin !== 'null' ? location.origin + location.pathname + qs : location.href;
  }

  root.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b || !root.contains(b)) return;
    if (b.hasAttribute('data-tea')) s.tea = b.getAttribute('data-tea');
    else if (b.hasAttribute('data-time')) s.m = Number(b.getAttribute('data-time'));
    else if (b.getAttribute('data-act') === 'g-dec') s.g = Math.max(0.5, Math.round((s.g - 0.5) * 10) / 10);
    else if (b.getAttribute('data-act') === 'g-inc') s.g = Math.min(10, Math.round((s.g + 0.5) * 10) / 10);
    else if (b.getAttribute('data-act') === 'w-dec') s.ml = Math.max(100, s.ml - 50);
    else if (b.getAttribute('data-act') === 'w-inc') s.ml = Math.min(500, s.ml + 50);
    else return;
    render();
  });

  // dalijimasis
  var copyBtn = $('copy-btn');
  if (copyBtn) {
    var copyLabel = $('copy-label');
    copyBtn.addEventListener('click', function () {
      var url = $('share-url');
      var text = url ? url.value : location.href;
      function done() {
        if (copyLabel) copyLabel.textContent = copyBtn.getAttribute('data-copied');
        setTimeout(function () { if (copyLabel) copyLabel.textContent = copyBtn.getAttribute('data-copy'); }, 2500);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { if (url) { url.select(); document.execCommand('copy'); done(); } });
      } else if (url) { url.select(); document.execCommand('copy'); done(); }
    });
  }

  // įterpimo kodas
  var embedBtn = $('embed-btn');
  var embedPanel = $('embed-panel');
  if (embedBtn && embedPanel) {
    var src = root.getAttribute('data-embed-src');
    var title = root.getAttribute('data-title') || '';
    $('embed-code').value = '<iframe src="' + src + '" width="100%" height="560" style="border:0" title="' + title + '" loading="lazy"></iframe>';
    embedBtn.addEventListener('click', function () {
      var open = embedPanel.hasAttribute('hidden');
      if (open) embedPanel.removeAttribute('hidden'); else embedPanel.setAttribute('hidden', '');
      embedBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      $('embed-label').textContent = embedBtn.getAttribute(open ? 'data-hide' : 'data-show');
    });
  }

  render();
})();
