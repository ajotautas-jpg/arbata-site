<?php
// Privatumą tausojanti lankomumo statistika: be slapukų, be IP išsaugojimo, be trečiųjų šalių.
// Gauna {p: kelias, r: nukreipėjas, e: įvykis, x: papildoma reikšmė, d: įrenginys (m/t/d)} ir prideda eilutę į <duomenų šaknis>/analytics/YYYY-MM.jsonl (žr. dataroot.php).
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
function done($code = 204) { http_response_code($code); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { done(405); }
// gerbiame „Do Not Track“ ir „Global Privacy Control“
if (($_SERVER['HTTP_DNT'] ?? '') === '1' || ($_SERVER['HTTP_SEC_GPC'] ?? '') === '1') { done(); }

$ua = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
if ($ua === '' || preg_match('/bot|crawl|spider|slurp|facebookexternalhit|preview|headless|lighthouse|pingdom|uptime|monitor|curl|wget|python|java\//i', $ua)) { done(); }

// tik iš savo svetainės
$host = strtolower(preg_replace('/^www\./', '', (string)preg_replace('/:\d+$/', '', (string)($_SERVER['HTTP_HOST'] ?? ''))));
$origin = (string)($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? ''));
$oh = strtolower(preg_replace('/^www\./', '', (string)parse_url($origin, PHP_URL_HOST)));
if ($oh === '' || $oh !== $host) { done(); }

$raw = file_get_contents('php://input', false, null, 0, 2048);
$j = json_decode((string)$raw, true);
if (!is_array($j)) { done(); }

$p = (string)($j['p'] ?? '');
$p = preg_replace('/[?#].*$/', '', $p);
if ($p === '' || $p[0] !== '/' || strlen($p) > 200 || !preg_match('#^[A-Za-z0-9/_\-.%]+$#', $p)) { done(); }
if (!preg_match('#^/(lt|en|it)(/|$)#', $p) && $p !== '/') { done(); }
$lang = preg_match('#^/(lt|en|it)(/|$)#', $p, $m) ? $m[1] : '';

$e = preg_replace('/[^a-z0-9_:-]/', '', strtolower((string)($j['e'] ?? 'pv')));
$e = substr($e === '' ? 'pv' : $e, 0, 24);
$x = substr(preg_replace('/[^A-Za-z0-9_.:\/-]/', '', (string)($j['x'] ?? '')), 0, 60);
$d = in_array($j['d'] ?? '', ['m', 't', 'd'], true) ? $j['d'] : '';
$r = '';
if (!empty($j['r'])) {
    $rh = strtolower(preg_replace('/^www\./', '', (string)parse_url((string)$j['r'], PHP_URL_HOST)));
    if ($rh !== '' && $rh !== $host && preg_match('/^[a-z0-9.-]{3,60}$/', $rh)) { $r = $rh; }
}

require_once __DIR__ . '/dataroot.php';
$dir = arbata_data_root() . '/analytics';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
if (!is_file($dir . '/.htaccess')) { @file_put_contents($dir . '/.htaccess', "Require all denied\nOrder allow,deny\nDeny from all\n"); }

// lankytojo žymė galioja tik vieną dieną: sūdas keičiasi kasdien, seni sūdai ištrinami, IP niekur nesaugomas
$day = gmdate('Ymd');
$saltFile = $dir . '/salt-' . $day;
if (!is_file($saltFile)) {
    @file_put_contents($saltFile, bin2hex(random_bytes(16)), LOCK_EX);
    foreach (glob($dir . '/salt-*') ?: [] as $f) { if ($f !== $saltFile) { @unlink($f); } }
}
$salt = (string)@file_get_contents($saltFile);
$v = substr(hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . '|' . $ua . '|' . $salt), 0, 12);

// paprastas apribojimas: iki 300 įrašų per valandą iš vienos dienos žymės
$rk = $dir . '/rate-' . substr(hash('sha256', $v . gmdate('YmdH')), 0, 16) . '.cnt';
$c = is_file($rk) ? (int)@file_get_contents($rk) : 0;
if ($c >= 300) { done(); }
@file_put_contents($rk, (string)($c + 1), LOCK_EX);
foreach (glob($dir . '/rate-*.cnt') ?: [] as $f) { if (filemtime($f) < time() - 7200) { @unlink($f); } }

$line = json_encode(['t' => time(), 'p' => $p, 'e' => $e, 'x' => $x, 'r' => $r, 'l' => $lang, 'd' => $d, 'v' => $v], JSON_UNESCAPED_SLASHES);
$file = $dir . '/' . gmdate('Y-m') . '.jsonl';
@file_put_contents($file, $line . "\n", FILE_APPEND | LOCK_EX);

// duomenys saugomi ne ilgiau kaip 14 mėnesių
if (mt_rand(1, 200) === 1) {
    foreach (glob($dir . '/*.jsonl') ?: [] as $f) { if (filemtime($f) < time() - 14 * 31 * 86400) { @unlink($f); } }
}
done();
