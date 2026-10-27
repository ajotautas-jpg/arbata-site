// Patikra PO diegimo: įklijuoti į naršyklės langą (konsolę ar javascript įrankį), atidarius https://arbata.pajusk.lt/lt/
// Grąžina sąrašą FAIL eilučių (tuščias = viskas gerai).
(async () => {
  const fails = [], ok = [];
  const get = async (u, o) => { try { const r = await fetch(u + (u.includes('?') ? '&' : '?') + 'x=' + Date.now(), Object.assign({ cache: 'no-store' }, o)); return { r, t: r.status === 204 ? '' : await r.text() }; } catch (e) { return { r: { status: 0 }, t: '' }; } };
  const v = await get('/version.txt'); const m = v.t.match(/(\d{4})-(\d\d)-(\d\d) (\d\d):(\d\d)/);
  if (!m) fails.push('version.txt'); else { const age = (Date.now() - Date.UTC(+m[1], m[2] - 1, +m[3], +m[4], +m[5])) / 60000; ok.push('diegimas prieš ' + Math.round(age) + ' min.'); }
  for (const p of ['/lt/', '/en/', '/it/', '/lt/blog/', '/lt/biblioteka/', '/lt/ritualai/', '/lt/markes/', '/lt/irankiai/', '/sitemap.xml', '/robots.txt', '/assets/style.css', '/assets/a.js']) { const x = await get(p); if (x.r.status !== 200) fails.push(p + ' → ' + x.r.status); }
  for (const p of ['/_data/subscribers.csv', '/_data/analytics/2026-10.jsonl', '/.git/config']) { const x = await get(p); if (x.r.status === 200) fails.push('ATVIRA: ' + p); }
  const a = await get('/a.php', { method: 'POST', body: '{}' }); if (a.r.status !== 204) fails.push('a.php → ' + a.r.status);
  const s = await get('/stats/'); if (![200, 401, 403].includes(s.r.status)) fails.push('/stats/ → ' + s.r.status);
  const h = await get('/lt/'); if (/noindex/.test(h.t)) fails.push('/lt/ turi noindex');
  const rb = await get('/robots.txt'); if (!/Sitemap:/.test(rb.t) || /^Disallow:\s*\/\s*$/m.test(rb.t)) fails.push('robots.txt');
  return JSON.stringify({ fails, ok });
})()
