/* Titulinio puslapio mini skaičiuoklė (puodeliai kavos -> mg kofeino -> yerba mate puodeliai) */
(function () {
  var root = document.getElementById('hc');
  if (!root) return;
  var lang = document.documentElement.lang || 'lt';
  var per = { espresso: Number(root.getAttribute('data-espresso')), filter: Number(root.getAttribute('data-filter')) };
  var mate = Number(root.getAttribute('data-mate'));
  var pre = root.getAttribute('data-eq-pre') || '';
  var post = root.getAttribute('data-eq-post') || '';
  var s = { cups: 3, kind: 'filter' };
  var elCups = document.getElementById('hc-cups');
  var elMg = document.getElementById('hc-mg');
  var elEq = document.getElementById('hc-eq');
  var kindBtns = root.querySelectorAll('[data-kind]');

  function fmt(n) {
    var x = String(n);
    return lang === 'en' ? x : x.replace('.', ',');
  }
  function render() {
    var mg = s.cups * per[s.kind];
    var cupsMate = Math.round(mg / mate * 10) / 10;
    elCups.textContent = s.cups;
    elMg.textContent = mg;
    elEq.textContent = pre + fmt(cupsMate) + post;
    for (var i = 0; i < kindBtns.length; i++) {
      kindBtns[i].setAttribute('aria-pressed', kindBtns[i].getAttribute('data-kind') === s.kind ? 'true' : 'false');
    }
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b || !root.contains(b)) return;
    var act = b.getAttribute('data-act');
    var kind = b.getAttribute('data-kind');
    if (act === 'dec') s.cups = Math.max(1, s.cups - 1);
    else if (act === 'inc') s.cups = Math.min(8, s.cups + 1);
    else if (kind) s.kind = kind;
    render();
  });
  render();
})();
