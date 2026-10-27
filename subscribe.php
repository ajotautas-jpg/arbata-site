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
@file_put_contents($rateFile, (string)($count + 1), LOCK_EX);
foreach (glob($dir . '/rate-*.cnt') ?: [] as $f) { if (filemtime($f) < time() - 7200) { @unlink($f); } }

// apsauga nuo CSV formulių
$safe = function ($v) { return preg_match('/^[=+\-@\t\r]/', $v) ? "'" . $v : $v; };

$file = $dir . '/subscribers.csv';
$new = !is_file($file);
$fh = @fopen($file, 'ab');
if (!$fh) { out(false, 500); }
if (flock($fh, LOCK_EX)) {
    if ($new) { fputcsv($fh, ['time', 'email', 'lang', 'source', 'consent']); }
    fputcsv($fh, [date('c'), $safe($email), $lang, $source, 'yes']);
    fflush($fh);
    flock($fh, LOCK_UN);
}
fclose($fh);
out(true);
