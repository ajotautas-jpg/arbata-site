/* Privatumą tausojanti statistika: be slapukų ir be naršyklės saugyklos. Gerbia Do Not Track / Global Privacy Control. */
(function () {
  var nav = navigator;
  if (nav.doNotTrack === '1' || window.doNotTrack === '1' || nav.globalPrivacyControl) return;
  var d = window.innerWidth < 600 ? 'm' : window.innerWidth < 1024 ? 't' : 'd';
  function send(e, x) {
    var body = JSON.stringify({ p: location.pathname, r: document.referrer, e: e, x: x || '', d: d });
    try {
      if (nav.sendBeacon) { nav.sendBeacon('/a.php', new Blob([body], { type: 'text/plain' })); return; }
    } catch (err) {}
    try { fetch('/a.php', { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'text/plain' } }); } catch (err) {}
  }
  window.arbataTrack = send;
  send('pv');
  var toolSent = false;
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    var a = t.closest ? t.closest('a[href]') : null;
    if (a && /^https?:/i.test(a.getAttribute('href')) && a.hostname !== location.hostname) {
      send('out', a.hostname.replace(/^www\./, ''));
      return;
    }
    var tool = document.getElementById('tool');
    if (!toolSent && tool && tool.contains(t) && t.closest && t.closest('button,input,select,.pill')) {
      toolSent = true;
      send('tool', tool.getAttribute('data-tool') || '');
    }
  }, true);
})();
