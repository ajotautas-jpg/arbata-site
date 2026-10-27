<?php
// Paprasta el. pašto rinkimo forma: įrašo į _data/subscribers.csv (katalogas uždarytas per .htaccess).
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function out($ok, $code = 200) {
    http_response_code($code);
    echo json_encode(['ok' => $ok]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { out(false, 405); }

// anti-botų spąstai: žmonės šio lauko nemato
if (!empty($_POST['website'])) { out(true); }

$email = trim((string)($_POST['email'] ?? ''));
$lang = in_array($_POST['lang'] ?? '', ['lt', 'en', 'it'], true) ? $_POST['lang'] : 'lt';
$source = preg_replace('/[^a-z0-9_-]/i', '', (string)($_POST['source'] ?? 'newsletter'));
$source = substr($source, 0, 32);
$consent = !empty($_POST['consent']);

if (!$consent || strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) { out(false, 422); }

// paprasta apsauga nuo per dažno siuntimo iš to paties IP (iki 10 per valandą)
require_once __DIR__ . '/dataroot.php';
$dir = arbata_data_root();
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
$ipKey = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH'));
$rateFile = $dir . '/rate-' . substr($ipKey, 0, 16) . '.cnt';
$count = is_file($rateFile) ? (int)@file_get_contents($rateFile) : 0;
if ($count >= 10) { out(false, 429); }
// bendras ribojimas: iki 30 registracijų per valandą (apsauga nuo lentelės užpildymo)
$totFile = $dir . '/rate-total-' . date('YmdH') . '.cnt';
$tot = is_file($totFile) ? (int)@file_get_contents($totFile) : 0;
if ($tot >= 30) { out(false, 429); }
@file_put_contents($totFile, (string)($tot + 1), LOCK_EX);
@file_put_contents($rateFile, (string)($count + 1), LOCK_EX);
foreach (glob($dir . '/rate-*.cnt') ?: [] as $f) { if (filemtime($f) < time() - 7200) { @unlink($f); } }

// puslapis, iš kurio registruojamasi (tik kelias iš Referer, be užklausos parametrų)
$page = (string)parse_url((string)($_SERVER['HTTP_REFERER'] ?? ''), PHP_URL_PATH);
$page = substr(preg_replace('/[^a-zA-Z0-9\/_.-]/', '', $page), 0, 100);

// apsauga nuo CSV formulių
$safe = function ($v) { return preg_match('/^[=+\-@\t\r]/', $v) ? "'" . $v : $v; };

$file = $dir . '/subscribers.csv';
$new = !is_file($file);
$fh = @fopen($file, 'ab');
if (!$fh) { out(false, 500); }
if (flock($fh, LOCK_EX)) {
    if ($new) { fputcsv($fh, ['time', 'email', 'lang', 'source', 'consent', 'page']); }
    fputcsv($fh, [date('c'), $safe($email), $lang, $source, 'yes', $page]);
    fflush($fh);
    flock($fh, LOCK_UN);
}
fclose($fh);

// --- antroji kopija: Google Sheets per Apps Script (nepavykus registracija vis tiek sėkminga) ---
function sheet_post($conf, $row) {
    if (!function_exists('curl_init')) { return 'nocurl'; }
    $ch = curl_init($conf['url']);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($row + ['token' => $conf['token']]),
        CURLOPT_HTTPHEADER => ['Content-Type: text/plain;charset=utf-8'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_TIMEOUT => 5,
        CURLOPT_CONNECTTIMEOUT => 3,
    ]);
    $res = curl_exec($ch);
    $http = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_errno($ch);
    curl_close($ch);
    if ($res === false) { return 'curl' . $err; }
    $j = json_decode($res, true);
    if (is_array($j) && !empty($j['ok'])) { return ''; }
    return 'http' . $http . (is_array($j) && isset($j['error']) ? ':' . preg_replace('/[^a-z ]/', '', (string)$j['error']) : '');
}
function sheet_log($dir, $msg) {
    // be el. pašto: tik laikas ir klaidos kodas
    @file_put_contents($dir . '/sheet-errors.log', date('c') . ' ' . $msg . "\n", FILE_APPEND | LOCK_EX);
}

$confFile = $dir . '/sheet.conf.php';
$conf = is_file($confFile) ? @include $confFile : null;
if (is_array($conf) && !empty($conf['url']) && !empty($conf['token'])) {
    $queue = $dir . '/sheet-pending.jsonl';
    $row = ['email' => $email, 'lang' => $lang, 'form' => $source, 'consent' => true, 'page' => $page];
    $e = sheet_post($conf, $row);
    if ($e === '') {
        // pavyko: pabandyti iš naujo anksčiau nepavykusias (iki 5 per kartą)
        if (is_file($queue) && filesize($queue) > 0) {
            $lines = @file($queue, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [];
            $left = [];
            foreach ($lines as $i => $ln) {
                $r = json_decode($ln, true);
                if (!is_array($r) || $i >= 5) { $left[] = $ln; continue; }
                if (sheet_post($conf, $r) !== '') { $left[] = $ln; }
            }
            @file_put_contents($queue, $left ? implode("\n", $left) . "\n" : '', LOCK_EX);
        }
    } else {
        sheet_log($dir, $e);
        @file_put_contents($queue, json_encode($row) . "\n", FILE_APPEND | LOCK_EX);
    }
}
out(true);
