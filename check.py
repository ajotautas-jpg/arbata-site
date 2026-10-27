#!/usr/bin/env python3
"""Patikra prieš diegimą: python3 check.py  (deploy.sh paleidžia automatiškai; apeiti: SKIP_CHECK=1 ./deploy.sh).
Tikrina jau sugeneruotą dist/: būtini failai, PHP sintaksė, duomenų vieta, HTML (likę {vietos}, None, NaN), sitemap, robots, noindex, nuorodos į failus,
JSON-LD, draudžiamos frazės, paslaptys repo. Grąžina kodą 1, jei yra KLAIDŲ; ĮSPĖJIMAI tik parodomi."""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(ROOT, 'dist')
errors, warns = [], []
def err(m): errors.append(m)
def warn(m): warns.append(m)

if not os.path.isdir(D):
    print('KLAIDA: nėra dist/, pirma paleisk python3 build.py'); sys.exit(1)

# 1. būtini failai
for f in ('.htaccess', 'robots.txt', 'sitemap.xml', 'index.html', 'a.php', 'dataroot.php', 'subscribe.php', 'stats/index.php', 'stats/.htaccess', 'assets/a.js', 'assets/style.css', 'assets/tools.js', 'lt/index.html', 'en/index.html', 'it/index.html'):
    if not os.path.exists(os.path.join(D, f)): err(f'trūksta failo dist/{f}')

# 2. PHP: sintaksė ir duomenų vieta
for f in glob.glob(D + '/**/*.php', recursive=True):
    r = subprocess.run(['php', '-l', f], capture_output=True, text=True)
    if r.returncode != 0 and 'not found' not in (r.stderr or ''): err(f'PHP sintaksės klaida {os.path.relpath(f, D)}: {r.stdout.strip() or r.stderr.strip()}')
    base = os.path.basename(f)
    src = open(f, encoding='utf-8').read()
    if base != 'dataroot.php' and re.search(r"__DIR__\s*\.\s*'/_data", src):
        err(f'{os.path.relpath(f, D)} rašo į __DIR__/_data: diegimas tai ištrins (naudok arbata_data_root())')
    if base in ('a.php', 'subscribe.php') or base == 'index.php' and 'stats' in f:
        if 'arbata_data_root' not in src: err(f'{os.path.relpath(f, D)} nenaudoja arbata_data_root()')
if not os.path.exists(os.path.join(ROOT, 'static', 'stats', 'index.php')) or 'KEY_HASH' not in open(os.path.join(ROOT, 'static', 'stats', 'index.php'), encoding='utf-8').read():
    err('static/stats/index.php be KEY_HASH')

# 3. HTML
pages = {}
for f in glob.glob(D + '/**/*.html', recursive=True):
    rel = os.path.relpath(f, D).replace(os.sep, '/')
    pages[rel] = open(f, encoding='utf-8').read()
noindex = set()
PH = re.compile(r'\{[a-z_]{1,24}\}')
for rel, s in pages.items():
    is_embed = rel.split('/')[1:2] in (['embed'], ['ideti'], ['incorpora'])
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s): noindex.add(rel)
    vis = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', vis)
    for pat, name in ((PH, 'likusi {vieta}'), (re.compile(r'\bNone\b'), 'None'), (re.compile(r'\bundefined\b'), 'undefined'), (re.compile(r'\bNaN\b'), 'NaN'), (re.compile(r'\[object '), '[object')):
        m = pat.search(text)
        if m: err(f'{rel}: {name} ({m.group(0)!r}) tekste')
    if rel != 'index.html':
        if '<title>' not in s or re.search(r'<title>\s*</title>', s): err(f'{rel}: nėra title')
        if 'name="description"' not in s and not is_embed: warn(f'{rel}: nėra meta description')
        if 'rel="canonical"' not in s and not is_embed: warn(f'{rel}: nėra canonical')
        if len(re.findall(r'<h1\b', s)) != 1 and not is_embed: warn(f'{rel}: h1 kiekis {len(re.findall(r"<h1", s))}')
    # JSON-LD
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S):
        try: json.loads(blk.replace('<\\/', '</'))
        except Exception as e: err(f'{rel}: sugedęs JSON-LD ({e})')
    # vietiniai ištekliai
    for h in set(re.findall(r'(?:href|src)="(/[^"#?]+\.(?:css|js|svg|png|jpg|jpeg|webp|ico|xml|txt))', s)):
        if not os.path.exists(D + h): err(f'{rel}: nėra failo {h}')
    # draudžiamos frazės
    low = text.lower()
    for bad in ('no pressure to buy', 'no pressure'):
        if bad in low: err(f'{rel}: draudžiama frazė „{bad}“')
    if rel.startswith('lt/') and re.search(r'\bmark(?:ė|ės|ių|ėse|es)\b', text, flags=re.I): warn(f'{rel}: LT tekste „markė“ (vartok „gamintojai“)')

# 4. šaknis ir robots
root = pages.get('index.html', '')
if 'noindex' in root: err('šakninis puslapis turi noindex (sprendimas 2026-10-25: be noindex)')
rb = open(os.path.join(D, 'robots.txt'), encoding='utf-8').read() if os.path.exists(D + '/robots.txt') else ''
if re.search(r'^Disallow:\s*/\s*$', rb, flags=re.M): err('robots.txt blokuoja visą svetainę')
for need in ('Disallow: /_data/', 'Disallow: /stats/', 'Sitemap:'):
    if need not in rb: err(f'robots.txt be „{need}“')

# 5. sitemap
sm = open(os.path.join(D, 'sitemap.xml'), encoding='utf-8').read() if os.path.exists(D + '/sitemap.xml') else ''
urls = re.findall(r'<loc>https://arbata\.pajusk\.lt(/[^<]*)</loc>', sm)
if len(urls) < 250: err(f'sitemap per mažas: {len(urls)} URL')
if len(set(urls)) != len(urls): err('sitemap turi pasikartojančių URL')
for u in urls:
    rel = u.strip('/') + '/index.html' if u != '/' else 'index.html'
    if rel not in pages: err(f'sitemap URL be failo: {u}')
    elif rel in noindex: err(f'sitemap URL su noindex: {u}')

# 6. paslaptys repo
tracked = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True).stdout.split()
SECRET = re.compile(r'(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY)')
for f in tracked:
    if f.endswith(('.png', '.jpg', '.webp', '.ico', '.svg', '.woff2')): continue
    try: t = open(os.path.join(ROOT, f), encoding='utf-8').read()
    except Exception: continue
    if SECRET.search(t): err(f'galima paslaptis faile {f}')

# 7. nuorodų auditas
r = subprocess.run([sys.executable, os.path.join(ROOT, 'linkaudit.py')], capture_output=True, text=True)
head = r.stdout.split('\n')[:2]
m1 = re.search(r'sugedusių nuorodų: (\d+)', head[0]); m2 = re.search(r': (\d+)', head[1]) if len(head) > 1 else None
if not m1 or int(m1.group(1)): err('sugedusių vidinių nuorodų: ' + (m1.group(1) if m1 else '?'))
if m2 and int(m2.group(1)): warn(f'puslapių be įeinančių nuorodų: {m2.group(1)}')

for w in warns[:40]: print('ĮSPĖJIMAS:', w)
for e in errors[:60]: print('KLAIDA:', e)
print(f'Patikra: {len(pages)} HTML, {len(urls)} sitemap URL, klaidų {len(errors)}, įspėjimų {len(warns)}')
sys.exit(1 if errors else 0)
