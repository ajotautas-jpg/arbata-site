<?php
// Statistikos skydelis. Prieiga tik su slaptu raktu (čia saugoma tik jo SHA-256 maiša).
const KEY_HASH = '70adb688370e2bad1a87814bee19515d6a229d0aeb9bbf7897a502fc9e3de6d6';
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
$secure = !empty($_SERVER['HTTPS']);
session_set_cookie_params(['lifetime' => 0, 'path' => '/stats/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Strict']);
session_name('arbata_stats');
session_start();

function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$dir = dirname(__DIR__) . '/_data/analytics';

// atsijungimas
if (isset($_GET['out'])) { $_SESSION = []; session_destroy(); header('Location: /stats/'); exit; }

// prisijungimas (iki 8 bandymų per 15 min. iš vieno IP, IP nesaugomas, tik maiša)
if (empty($_SESSION['ok'])) {
    $err = '';
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
        $rk = $dir . '/login-' . substr(hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH') . intdiv((int)date('i'), 15)), 0, 16) . '.cnt';
        if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
        $n = is_file($rk) ? (int)@file_get_contents($rk) : 0;
        if ($n >= 8) { http_response_code(429); $err = 'Too many attempts. Try again in 15 minutes.'; }
        else {
            @file_put_contents($rk, (string)($n + 1), LOCK_EX);
            if (hash_equals(KEY_HASH, hash('sha256', trim((string)($_POST['key'] ?? ''))))) {
                session_regenerate_id(true); $_SESSION['ok'] = 1; header('Location: /stats/'); exit;
            }
            $err = 'Wrong key.';
        }
    }
    ?><!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Stats</title>
<style>body{font:16px system-ui,sans-serif;background:#f4f6f1;color:#16231c;display:grid;place-items:center;min-height:100vh;margin:0}form{background:#fff;padding:28px;border-radius:20px;border:1px solid #e3e8df;width:min(360px,90vw)}input,button{font:inherit;width:100%;box-sizing:border-box;padding:12px 14px;border-radius:12px;border:1px solid #c9d3cb;margin-top:12px}button{background:#1e4d36;color:#fff;border:0;font-weight:700;cursor:pointer}.e{color:#b3261e;margin:10px 0 0}@media(prefers-color-scheme:dark){body{background:#101712;color:#e7efe8}form{background:#17211b;border-color:#2b3a30}input{background:#101712;color:inherit;border-color:#2b3a30}}</style></head>
<body><form method="post"><strong>Arbata stats</strong><input type="password" name="key" placeholder="Access key" autocomplete="current-password" autofocus required><button type="submit">Open</button><?php if ($err) echo '<p class="e">' . h($err) . '</p>'; ?></form></body></html><?php
    exit;
}

// ---- duomenys ----
$days = (int)($_GET['d'] ?? 30);
if (!in_array($days, [1, 7, 30, 90, 365], true)) { $days = 30; }
$from = time() - $days * 86400;
$rows = [];
foreach (glob($dir . '/*.jsonl') ?: [] as $f) {
    $ym = basename($f, '.jsonl');
    if ($ym < gmdate('Y-m', $from)) { continue; }
    $fh = @fopen($f, 'rb'); if (!$fh) continue;
    while (($ln = fgets($fh)) !== false) {
        $r = json_decode($ln, true);
        if (is_array($r) && ($r['t'] ?? 0) >= $from) { $rows[] = $r; }
    }
    fclose($fh);
}

function section($p) {
    $s = explode('/', trim($p, '/'));
    $k = $s[1] ?? '';
    $map = ['irankiai' => 'Tools', 'tools' => 'Tools', 'strumenti' => 'Tools', 'blog' => 'Blog', 'kofeinas' => 'Caffeine pages', 'caffeine' => 'Caffeine pages', 'caffeina' => 'Caffeine pages',
        'biblioteka' => 'Tea library', 'tea-library' => 'Tea library', 'libreria-te' => 'Tea library', 'markes' => 'Brands', 'brands' => 'Brands', 'marche' => 'Brands',
        'palyginimas' => 'Comparisons', 'compare' => 'Comparisons', 'confronto' => 'Comparisons', 'gidai' => 'Guides', 'guides' => 'Guides', 'guide' => 'Guides',
        'privatumas' => 'Privacy', 'privacy' => 'Privacy', 'privacy-policy' => 'Privacy', 'informativa-sulla-privacy' => 'Privacy'];
    if ($k === '') return 'Home';
    return $map[$k] ?? 'Other';
}
function source($r) {
    $h = $r['r'] ?? '';
    if ($h === '') return 'Direct / unknown';
    if (preg_match('/(^|\.)(google|bing|duckduckgo|ecosia|yahoo|yandex|brave|startpage)\./', $h)) return 'Search: ' . preg_replace('/^.*?(google|bing|duckduckgo|ecosia|yahoo|yandex|brave|startpage).*$/', '$1', $h);
    if (preg_match('/(facebook|instagram|t\.co|twitter|x\.com|linkedin|reddit|pinterest|tiktok|youtube|whatsapp|telegram)/', $h)) return 'Social: ' . $h;
    return 'Site: ' . $h;
}
$pv = $uv = [];
$byDay = $pages = $secs = $langs = $srcs = $devs = $events = $tools = $outs = $newsl = [];
$visitors = [];
$pvTotal = 0; $toolPv = 0;
foreach ($rows as $r) {
    $day = gmdate('Y-m-d', $r['t']);
    if (($r['e'] ?? '') === 'pv') {
        $pvTotal++;
        $byDay[$day]['pv'] = ($byDay[$day]['pv'] ?? 0) + 1;
        $visitors[$day . $r['v']] = 1;
        $byDay[$day]['v'][$r['v']] = 1;
        $pages[$r['p']] = ($pages[$r['p']] ?? 0) + 1;
        $s = section($r['p']); $secs[$s] = ($secs[$s] ?? 0) + 1;
        if ($s === 'Tools' && substr_count(trim($r['p'], '/'), '/') >= 2) { $toolPv++; }
        if ($r['l'] !== '') $langs[strtoupper($r['l'])] = ($langs[strtoupper($r['l'])] ?? 0) + 1;
        $sr = source($r); $srcs[$sr] = ($srcs[$sr] ?? 0) + 1;
        $dv = ['m' => 'Mobile', 't' => 'Tablet', 'd' => 'Desktop'][$r['d']] ?? 'Unknown'; $devs[$dv] = ($devs[$dv] ?? 0) + 1;
    } else {
        $k = $r['e']; $events[$k] = ($events[$k] ?? 0) + 1;
        if ($k === 'tool') $tools[$r['x']] = ($tools[$r['x']] ?? 0) + 1;
        if ($k === 'out') $outs[$r['x']] = ($outs[$r['x']] ?? 0) + 1;
        if ($k === 'newsletter') $newsl[$r['p']] = ($newsl[$r['p']] ?? 0) + 1;
    }
}
foreach ([&$pages, &$secs, &$langs, &$srcs, &$devs, &$events, &$tools, &$outs, &$newsl] as &$a) { arsort($a); }
unset($a);
ksort($byDay);

function table($title, $arr, $limit = 12, $note = '') {
    echo '<section><h2>' . h($title) . '</h2>';
    if ($note) echo '<p class="n">' . h($note) . '</p>';
    if (!$arr) { echo '<p class="n">No data yet.</p></section>'; return; }
    $max = max($arr);
    echo '<table>';
    foreach (array_slice($arr, 0, $limit, true) as $k => $v) {
        $w = $max ? round($v / $max * 100) : 0;
        echo '<tr><td class="k">' . h($k) . '</td><td class="v">' . (int)$v . '</td><td class="b"><i style="width:' . $w . '%"></i></td></tr>';
    }
    echo '</table></section>';
}
$visitorCount = count($visitors);
$tp = $toolPv ? round(array_sum($tools) / $toolPv * 100) : 0;
?><!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Arbata stats</title>
<style>
:root{--bg:#f4f6f1;--card:#fff;--ink:#16231c;--mut:#5a6b61;--line:#e3e8df;--acc:#1e4d36;--bar:#c5d9b5}
@media(prefers-color-scheme:dark){:root{--bg:#101712;--card:#17211b;--ink:#e7efe8;--mut:#9fb0a5;--line:#2b3a30;--acc:#8fd0a8;--bar:#2f5a43}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:1100px;margin:0 auto;padding:20px 16px 60px}
h1{font-size:24px;margin:0}h2{font-size:16px;margin:0 0 10px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:18px}
nav a{display:inline-block;padding:7px 13px;border-radius:999px;border:1px solid var(--line);color:var(--ink);text-decoration:none;margin-right:6px;background:var(--card)}
nav a.on{background:var(--acc);color:var(--bg);border-color:var(--acc)}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:16px}
.kpi div,section{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px}
.kpi b{display:block;font-size:28px}.kpi span{color:var(--mut);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}
table{width:100%;border-collapse:collapse}td{padding:5px 6px;border-top:1px solid var(--line);vertical-align:middle}
td.k{word-break:break-all}td.v{text-align:right;font-weight:700;width:48px}td.b{width:34%}td.b i{display:block;height:8px;border-radius:4px;background:var(--bar)}
.n{color:var(--mut);font-size:13px;margin:0 0 8px}svg{width:100%;height:150px;display:block}
a{color:var(--acc)}
</style></head><body><main>
<header><h1>Arbata stats</h1>
<nav><?php foreach ([1 => 'Today', 7 => '7 days', 30 => '30 days', 90 => '90 days', 365 => '1 year'] as $d => $lbl) echo '<a class="' . ($d === $days ? 'on' : '') . '" href="?d=' . $d . '">' . $lbl . '</a>'; ?><a href="?out=1">Log out</a></nav></header>
<div class="kpi">
<div><b><?= $pvTotal ?></b><span>Page views</span></div>
<div><b><?= $visitorCount ?></b><span>Visitors (counted per day)</span></div>
<div><b><?= (int)($events['tool'] ?? 0) ?></b><span>Tool uses (<?= $tp ?>% of tool page views)</span></div>
<div><b><?= (int)($events['newsletter'] ?? 0) ?></b><span>Newsletter sign-ups</span></div>
<div><b><?= (int)($events['out'] ?? 0) ?></b><span>Outbound clicks</span></div>
</div>
<section style="margin-bottom:12px"><h2>Page views per day</h2>
<?php
$labels = array_keys($byDay); $n = count($labels);
if ($n === 0) { echo '<p class="n">No data yet. Visits are recorded from now on, and visitors with Do Not Track / Global Privacy Control are not counted.</p>'; }
else {
    $max = 1; foreach ($byDay as $v) { $max = max($max, $v['pv'] ?? 0); }
    $w = 1000; $hh = 150; $bw = $w / max($n, 1);
    echo '<svg viewBox="0 0 ' . $w . ' ' . $hh . '" preserveAspectRatio="none" role="img" aria-label="Page views per day">';
    foreach ($labels as $i => $d) {
        $v = $byDay[$d]['pv'] ?? 0; $bh = round($v / $max * ($hh - 20));
        echo '<rect x="' . round($i * $bw + 1, 1) . '" y="' . ($hh - $bh) . '" width="' . max(round($bw - 2, 1), 1) . '" height="' . $bh . '" rx="2" fill="var(--bar)"><title>' . h($d) . ': ' . $v . ' views, ' . count($byDay[$d]['v'] ?? []) . ' visitors</title></rect>';
    }
    echo '</svg><p class="n">' . h($labels[0]) . ' to ' . h($labels[$n - 1]) . ', max ' . $max . ' per day (UTC dates).</p>';
}
?></section>
<div class="grid">
<?php
table('Top pages', $pages, 15);
table('Sections', $secs);
table('Traffic sources', $srcs, 12, 'Where visitors came from (referrer host).');
table('Languages', $langs);
table('Devices', $devs);
table('Tools used', $tools, 12, 'Counted once per page load, on the first click inside a tool.');
table('Pages with newsletter sign-ups', $newsl, 10);
table('Outbound clicks', $outs, 10, 'Clicks to other sites, by host.');
?></div>
<p class="n" style="margin-top:18px">No cookies, no IP addresses stored. A visitor is a one-day hash that cannot be linked across days. Raw data: <code>_data/analytics/*.jsonl</code> (blocked from the web, kept 14 months).</p>
</main></body></html>
