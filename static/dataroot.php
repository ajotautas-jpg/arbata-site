<?php
// Kur saugomi duomenys (statistika, prenumeratoriai). SVARBU: tai turi būti vieta, kurios diegimas (deploy) neperrašo.
// Pirmenybė: aplankas virš public_html (nepasiekiamas iš interneto); jei neleidžiama, – public_html šaknyje; paskutinė išeitis – senas aplankas.
function arbata_data_root() {
    static $root = null;
    if ($root !== null) { return $root; }
    $cands = [dirname(__DIR__, 2) . '/arbata-data', dirname(__DIR__) . '/_arbata_data', __DIR__ . '/_data'];
    foreach ($cands as $i => $c) {
        if (!@is_dir($c)) { @mkdir($c, 0750, true); }
        if (@is_dir($c) && @is_writable($c)) {
            if ($i > 0 && !is_file($c . '/.htaccess')) {
                @file_put_contents($c . '/.htaccess', "Require all denied\nOrder allow,deny\nDeny from all\n");
            }
            return $root = $c;
        }
    }
    return $root = __DIR__ . '/_data';
}
