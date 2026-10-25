"""Blogas: straipsniai iš content/blog/<id>/<lang>.md (LT/EN/IT) -> /{lang}/blog/{slug}/.

Straipsnio failas: front matter (--- ... ---) + Markdown.
  slug, title, description, category, date (YYYY-MM-DD), [updated], [related: id, id], [sources: raktai]
Markdown: ## / ### antraštės, pastraipos, - sąrašai, 1. sąrašai, **paryškinta**, *kursyvas*, [tekstas](nuoroda).
  about: puslapių raktai, su kuriais straipsnis susijęs (įrankiai, d_black, g_limit, hub_b ...). Iš jų: „Įrankiai ir duomenys“ bloke
         straipsnyje IR „Skaityk daugiau“ blokas atvirkščiai tuose puslapiuose. Be to, tekste automatiškai nuorodomi gėrimų pavadinimai (AUTO).
Vidinės nuorodos: (@calc), (@quiz), (@convert) ... = įrankiai pagal PATH raktą; (@post:id) = kitas straipsnis
(jei jo nėra šioje kalboje, lieka tik tekstas). Pastraipa iš vienos nuorodos tampa „CTA“ bloku.
Straipsniai su data ateityje nepublikuojami (build'as juos praleidžia).
Nauja kalba / straipsnis = tiesiog naujas failas; hreflang poros sudaromos pagal tai, kokios kalbos yra.
"""
import datetime
import email.utils
import html
import json
import math
import os
import re
import unicodedata

import caff
import seo_gen
import tools_gen as TG

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content', 'blog')
LANGS = ['lt', 'en', 'it']
DIR = 'blog'

CATS = {
    'quit': {'lt': 'Kavos atsisakymas', 'en': 'Quitting coffee', 'it': 'Smettere il caffè'},
    'compare': {'lt': 'Kava ir arbata', 'en': 'Coffee and tea', 'it': 'Caffè e tè'},
}

UI = {
    'lt': dict(blog='Blogas', h1='Blogas', title='Blogas: kava, kofeinas ir arbata', desc='Straipsniai apie kavos atsisakymą, kofeiną ir perėjimą prie arbatos: su šaltiniais ir be spaudimo.',
               lead='Straipsniai apie kavos atsisakymą, kofeiną ir perėjimą prie arbatos.', empty='Straipsniai bus netrukus.', toc='Turinys', related='Skaityk toliau', min='min. skaitymo',
               updated='Atnaujinta', rss='Blogo RSS'),
    'en': dict(blog='Blog', h1='Blog', title='Blog: coffee, caffeine and tea', desc='Articles about quitting coffee, caffeine and switching to tea, with sources.',
               lead='Articles about quitting coffee, caffeine and switching to tea.', empty='Articles are coming soon.', toc='Contents', related='Keep reading', min='min read',
               updated='Updated', rss='Blog RSS'),
    'it': dict(blog='Blog', h1='Blog', title='Blog: caffè, caffeina e tè', desc='Articoli su come smettere di bere caffè, sulla caffeina e sul passaggio al tè, con le fonti.',
               lead='Articoli su come smettere di bere caffè, sulla caffeina e sul passaggio al tè.', empty='Gli articoli arrivano presto.', toc='Indice', related='Continua a leggere', min='min di lettura',
               updated='Aggiornato', rss='RSS del blog'),
}

MONTHS = {
    'lt': ['sausio', 'vasario', 'kovo', 'balandžio', 'gegužės', 'birželio', 'liepos', 'rugpjūčio', 'rugsėjo', 'spalio', 'lapkričio', 'gruodžio'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'],
}

UI2 = {
    'lt': dict(more='Skaityk daugiau', about='Įrankiai ir duomenys', home_t='Iš bloga', home_sub='Straipsniai apie kavos atsisakymą ir perėjimą prie arbatos.', all='Visi straipsniai'),
    'en': dict(more='Read more', about='Tools and data', home_t='From the blog', home_sub='Articles about quitting coffee and switching to tea.', all='All articles'),
    'it': dict(more='Approfondisci', about='Strumenti e dati', home_t='Dal blog', home_sub='Articoli su come smettere di bere caffè e passare al tè.', all='Tutti gli articoli'),
}
for _l, _d in UI2.items():
    UI[_l].update(_d)

DRINK_LBL = {'lt': 'Kiek kofeino {n}?', 'en': 'Caffeine in {n}', 'it': 'Caffeina {n}'}   # {n} = seo_gen.N[id]["in"][lang]

# Automatinės nuorodos tekste: puslapio raktas -> {kalba: regex}. Nuorodomas tik PIRMAS pavadinimo paminėjimas straipsnyje,
# ne antraštėse, ne CTA, ir tik jei straipsnis dar nenurodo į tą puslapį. Daugiausiai AUTO_MAX nuorodų straipsnyje.
AUTO_MAX = 6
AUTO = {
    'd_black': {'lt': r'\bjuod(?:oji|osios|ąją|ojoje|ąja)\b(?:\s+arbat\w+)?', 'en': r'\bblack tea\b', 'it': r'\btè nero\b'},
    'd_green': {'lt': r'\bžal(?:ioji|iosios|iąją|iojoje|iąja)\b(?:\s+arbat\w+)?', 'en': r'\bgreen tea\b', 'it': r'\btè verde\b'},
    'd_white': {'lt': r'\bbalt(?:oji|osios|ąją|ojoje|ąja)\s+arbat\w+', 'en': r'\bwhite tea\b', 'it': r'\btè bianco\b'},
    'd_oolong': {'lt': r'\boolong\w*', 'en': r'\boolong\b', 'it': r'\boolong\b'},
    'd_puerh': {'lt': r'\bpu-erh\w*', 'en': r'\bpu-erh\b', 'it': r'\bpu-erh\b'},
    'd_matcha': {'lt': r'\bmatcha\w*', 'en': r'\bmatcha\b', 'it': r'\bmatcha\b'},
    'd_mate': {'lt': r'\byerba mate\w*', 'en': r'\byerba mate\b', 'it': r'\byerba mate\b'},
    'd_espresso': {'lt': r'\bespres\w+', 'en': r'\bespresso\b', 'it': r'\bespresso\b'},
    'd_filter': {'lt': r'\bfiltruot\w+\s+kav\w+', 'en': r'\b(?:brewed|filter) coffee\b', 'it': r'\bcaffè (?:filtrato|filtro)\b'},
    'd_decaf': {'lt': r'\bkav\w+ be kofeino\b', 'en': r'\bdecaf(?:feinated)? coffee\b', 'it': r'\bcaffè decaffeinato\b'},
    'd_cola': {'lt': r'\bkol(?:a|os|ą)\b', 'en': r'\bcola\b', 'it': r'\bcola\b'},
    'd_energy': {'lt': r'\benergin\w+\s+gėrim\w+', 'en': r'\benergy drinks?\b', 'it': r'\bbevande energetiche\b|\benergy drink\b'},
    'g_limit': {'lt': r'\bEFSA\b|\bdienos kofeino rib\w+', 'en': r'\bEFSA\b|\bdaily caffeine limit\b', 'it': r'\bEFSA\b|\blimite giornaliero\b'},
    'hub_t': {'lt': r'\barbatų bibliotek\w+', 'en': r'\btea library\b', 'it': r'\blibreria dei tè\b'},
    'hub_r': {'lt': r'\bkavos ritual\w+|\bryto ritual\w+', 'en': r'\bcoffee rituals?\b|\bmorning ritual\b', 'it': r'\brituali? (?:del caffè|del mattino)\b'},
    'hub_b': {'lt': r'\barbatų markių?\b|\barbatų markėms\b|\barbatų gamintoj\w+', 'en': r'\btea brands\b', 'it': r'\bmarche di tè\b'},
    'calc': {'lt': r'\bkofeino skaičiuokl\w+', 'en': r'\bcaffeine calculator\b', 'it': r'\bcalcolatore (?:della )?caffeina\b'},
    'tracker': {'lt': r'\bkofeino sekikl\w+', 'en': r'\bcaffeine tracker\b', 'it': r'\bdiario della caffeina\b'},
}
GENERIC = {'tools', 'hub_d', 'hub_c', 'hub_b', 'hub_t', 'hub_r'}   # puslapiai be konkretaus „about“ atitikmens rodo naujausius straipsnius

# papildomi šaltiniai (caff.SOURCES lieka tik kofeino duomenų bazei)
EXTRA_SOURCES = {
    'juliano': ('Juliano & Griffiths, Psychopharmacology 2004;176(1):1–29 (caffeine withdrawal: onset 12–24 h, peak 20–51 h, 2–9 days)',
                'https://doi.org/10.1007/s00213-004-2000-x'),
    'nutr': ('Nutrition Reviews 2008;66(2):82–90: Psychological effects of dietary components of tea: caffeine and L-theanine',
             'https://pubmed.ncbi.nlm.nih.gov/18254874/'),
}

POSTS = {}      # id -> {lang: post}
INDEX = {}      # puslapio raktas -> [straipsnių id] (iš about)
_FM = re.compile(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z', re.S)


def today():
    return os.environ.get('BLOG_TODAY') or datetime.date.today().isoformat()


def source(key):
    if key in EXTRA_SOURCES:
        return EXTRA_SOURCES[key]
    if key in caff.SOURCES:
        return caff.SOURCES[key]
    raise ValueError(f'Nežinomas šaltinio raktas: {key}')


def _parse(path):
    raw = open(path, encoding='utf-8').read()
    m = _FM.match(raw)
    if not m:
        raise ValueError(f'{path}: nerastas front matter')
    meta = {}
    for line in m.group(1).split('\n'):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        k, _, v = line.partition(':')
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1]
        meta[k.strip()] = v
    for req in ('slug', 'title', 'description', 'category', 'date'):
        if not meta.get(req):
            raise ValueError(f'{path}: trūksta „{req}“')
    if meta['category'] not in CATS:
        raise ValueError(f'{path}: nežinoma kategorija {meta["category"]}')
    datetime.date.fromisoformat(meta['date'])
    meta['related'] = [x.strip() for x in meta.get('related', '').split(',') if x.strip()]
    meta['sources'] = [x.strip() for x in meta.get('sources', '').split(',') if x.strip()]
    meta['about'] = [x.strip() for x in meta.get('about', '').split(',') if x.strip()]
    for s in meta['sources']:
        source(s)
    meta['body'] = m.group(2).strip() + '\n'
    return meta


def load():
    POSTS.clear()
    if not os.path.isdir(CONTENT):
        return
    t = today()
    for pid in sorted(os.listdir(CONTENT)):
        d = os.path.join(CONTENT, pid)
        if not os.path.isdir(d):
            continue
        for lang in LANGS:
            p = os.path.join(d, lang + '.md')
            if not os.path.exists(p):
                continue
            meta = _parse(p)
            if meta['date'] > t:
                continue
            meta['id'] = pid
            POSTS.setdefault(pid, {})[lang] = meta
    seen = {}
    for pid, by in POSTS.items():
        for lang, m in by.items():
            k = (lang, m['slug'])
            if k in seen:
                raise ValueError(f'Pasikartoja slug {k}: {seen[k]} ir {pid}')
            seen[k] = pid
    INDEX.clear()
    for pid, by in POSTS.items():
        for m in by.values():
            for k in m['about']:
                if pid not in INDEX.setdefault(k, []):
                    INDEX[k].append(pid)


def langs_of_post(pid):
    return [l for l in LANGS if l in POSTS[pid]]


def key_p(pid):
    return 'b_' + pid


def register(B):
    load()
    B.PATH['blog'] = lambda l: f'/{l}/{DIR}/'
    for pid in POSTS:
        B.PATH[key_p(pid)] = (lambda pid: lambda l: f'/{l}/{DIR}/{POSTS[pid][l]["slug"]}/')(pid)
        B.LANGS_OF[key_p(pid)] = langs_of_post(pid)


def all_keys():
    return ['blog'] + [key_p(p) for p in sorted(POSTS)]


def lastmod(key, lang):
    if key.startswith('b_') and key[2:] in POSTS and lang in POSTS[key[2:]]:
        m = POSTS[key[2:]][lang]
        return m.get('updated') or m['date']
    if key == 'blog':
        ds = [(m.get('updated') or m['date']) for by in POSTS.values() for l, m in by.items() if l == lang]
        return max(ds) if ds else None
    return None


# ---------- Markdown ----------
def slugify(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'sec'


def _link(B, lang, text, url):
    if url.startswith('@post:'):
        pid = url[6:]
        if pid in POSTS and lang in POSTS[pid]:
            return f'<a href="{B.PATH[key_p(pid)](lang)}">{text}</a>'
        if pid not in {p for p in os.listdir(CONTENT)}:
            raise ValueError(f'Nežinomas straipsnis: {url}')
        return text
    if url.startswith('@'):
        k = url[1:]
        if k not in B.PATH:
            raise ValueError(f'Nežinomas puslapio raktas: {url}')
        return f'<a href="{B.PATH[k](lang)}" target="_blank" rel="noopener">{text}</a>'
    ext = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
    return f'<a href="{html.escape(url, quote=True)}"{ext}>{text}</a>'


def inline(B, lang, s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: _link(B, lang, m.group(1), html.unescape(m.group(2))), s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])', r'<em>\1</em>', s)
    return s


_TOKEN = re.compile(r'(<a\b.*?</a>|<[^>]+>)', re.S)


def autolink(B, lang, htm, st):
    """Nuorodina pirmą AUTO frazės paminėjimą (tik tekste ne <a> viduje). st: {'used': set(raktų), 'n': int, 'skip': set(raktų)}."""
    if st['n'] >= AUTO_MAX:
        return htm
    parts = _TOKEN.split(htm)
    for i, tok in enumerate(parts):
        if i % 2 or not tok.strip() or st['n'] >= AUTO_MAX:
            continue
        for key, pats in AUTO.items():
            if key in st['used'] or key in st['skip'] or key not in B.PATH or st['n'] >= AUTO_MAX:
                continue
            m = re.search(pats[lang], tok, re.I)
            if m:
                a, b = m.span()
                tok = tok[:a] + f'<a href="{B.PATH[key](lang)}">{tok[a:b]}</a>' + tok[b:]
                # nauja nuoroda gali turėti <a>; kitų raktų ieškome tik už jos ribų
                st['used'].add(key)
                st['n'] += 1
                head, link, tail = tok[:a], tok[a:a + len(f'<a href="{B.PATH[key](lang)}">{m.group(0)}</a>')], tok[a + len(f'<a href="{B.PATH[key](lang)}">{m.group(0)}</a>'):]
                tail = autolink(B, lang, tail, st)
                head = autolink(B, lang, head, st) if head.strip() else head
                tok = head + link + tail
                break
        parts[i] = tok
    return ''.join(parts)


def render(B, lang, md):
    out, heads = [], []
    existing = set(re.findall(r'\]\(@([a-z0-9_]+)\)', md))
    st = {'used': set(), 'n': 0, 'skip': existing}
    para, items, kind = [], [], None

    def flush_p():
        nonlocal para
        if para:
            text = ' '.join(para)
            if re.fullmatch(r'\[[^\]]+\]\([^)\s]+\)', text):
                out.append(f'<p class="post-cta">{inline(B, lang, text)}</p>')
            else:
                out.append(f'<p>{autolink(B, lang, inline(B, lang, text), st)}</p>')
            para = []

    def flush_l():
        nonlocal items, kind
        if items:
            out.append(f'<{kind}>' + ''.join(f'<li>{autolink(B, lang, inline(B, lang, i), st)}</li>' for i in items) + f'</{kind}>')
            items, kind = [], None

    for line in md.split('\n'):
        s = line.rstrip()
        if not s.strip():
            flush_p(); flush_l()
            continue
        m = re.match(r'(#{2,3})\s+(.*)', s)
        if m:
            flush_p(); flush_l()
            lvl, txt = len(m.group(1)), m.group(2).strip()
            hid = slugify(re.sub(r'[*_]', '', txt))
            if lvl == 2:
                heads.append((hid, re.sub(r'[*_]', '', txt)))
            out.append(f'<h{lvl} id="{hid}">{inline(B, lang, txt)}</h{lvl}>')
            continue
        m = re.match(r'\s*[-*]\s+(.*)', s) or None
        n = re.match(r'\s*\d+\.\s+(.*)', s)
        if m or n:
            flush_p()
            k = 'ul' if m else 'ol'
            if kind and kind != k:
                flush_l()
            kind = k
            items.append((m or n).group(1))
            continue
        flush_l()
        para.append(s.strip())
    flush_p(); flush_l()
    return '\n'.join(out), heads


def read_min(md):
    return max(1, math.ceil(len(re.findall(r'\w+', md)) / 200))


def fmt_date(iso, lang):
    d = datetime.date.fromisoformat(iso)
    if lang == 'lt':
        return f'{d.year} m. {MONTHS["lt"][d.month - 1]} {d.day} d.'
    return f'{d.day} {MONTHS[lang][d.month - 1]} {d.year}'


def _sorted_ids(lang):
    ids = [p for p in POSTS if lang in POSTS[p]]
    return sorted(ids, key=lambda p: (POSTS[p][lang]['date'], p), reverse=True)


# ---------- puslapiai ----------
def _ld(B, lang, objs):
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>' for o in objs)


def _crumb_ld(B, lang, items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def _rss_link(B, lang):
    return f'<link rel="alternate" type="application/rss+xml" title="{B.E(UI[lang]["rss"])}" href="/{lang}/{DIR}/feed.xml">'


def _card(B, lang, pid):
    E = B.E
    m = POSTS[pid][lang]
    return (f'<a class="card" href="{B.PATH[key_p(pid)](lang)}"><span class="chip">{E(CATS[m["category"]][lang])}</span>'
            f'<h2 class="card-title">{E(m["title"])}</h2><p class="card-text">{E(m["description"])}</p>'
            f'<span class="card-foot"><span class="small">{E(fmt_date(m["date"], lang))}</span>'
            f'<span class="small">{read_min(m["body"])} {E(UI[lang]["min"])}</span></span></a>')


def index_page(B, lang):
    E = B.E
    u = UI[lang]
    t = seo_gen.L[lang]
    ids = _sorted_ids(lang)
    cards = ''.join(_card(B, lang, p) for p in ids) or f'<p>{E(u["empty"])}</p>'
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <span>{E(u['blog'])}</span></div>
<h1 class="page-title">{E(u['h1'])}</h1><p class="lead">{E(u['lead'])}</p>
<div class="grid">{cards}</div>
{seo_gen.tools_links(B, lang)}
</main>
{_ld(B, lang, [_crumb_ld(B, lang, [(t['home'], B.BASE + B.PATH['home'](lang)), (u['blog'], B.BASE + B.PATH['blog'](lang))])])}'''
    out = B.shell(lang, 'blog', u['title'], u['desc'], main)
    return out.replace('</head>', _rss_link(B, lang) + '</head>', 1)


def related_ids(pid, lang, n=3):
    """Pirma nurodyti related, tada tos pačios kategorijos / bendro about naujausi (iki n)."""
    m = POSTS[pid][lang]
    ids = [r for r in m['related'] if r in POSTS and lang in POSTS[r] and r != pid]
    rest = [p for p in _sorted_ids(lang) if p != pid and p not in ids]
    rest.sort(key=lambda p: (-(POSTS[p][lang]['category'] == m['category']) - len(set(POSTS[p][lang]['about']) & set(m['about'])) * 0.1,))
    return (ids + rest)[:n]


def page_label(B, key, lang):
    """Rodomas pavadinimas puslapio rakto nuorodai."""
    t = seo_gen.L[lang]
    if key in TG.TXT:
        return TG.TXT[key][lang]['menu']
    if key == 'calc':
        return t['tools_calc']
    if key.startswith('d_') and key[2:] in seo_gen.N:
        return DRINK_LBL[lang].format(n=seo_gen.N[key[2:]]['in'][lang])
    if key == 'g_limit':
        return t['g_h1']
    if key == 'hub_d':
        return t['hub_d']
    if key == 'hub_c':
        return t['hub_c']
    if key == 'hub_b':
        import brands_gen
        return brands_gen.T[lang]['hub']
    if key == 'tools':
        return B.C[lang]['nav_tools']
    if key == 'hub_t' or key.startswith('tl_'):
        import tealib_gen
        if key == 'hub_t':
            return tealib_gen.T[lang]['hub']
        import tealib_gen
        return tealib_gen.name_of(key[3:], lang)
    if key == 'hub_r' or key.startswith('r_'):
        import rituals_gen
        return rituals_gen.label(B, key, lang)
    if key.startswith('br_'):
        import brands_data
        return brands_data.brand_name(key[3:])
    raise ValueError(f'Nėra pavadinimo puslapio raktui {key}')


def about_block(B, lang, m, limit=8):
    keys = [k for k in m['about'] if k in B.PATH and lang in B.langs_of(k)][:limit]
    if not keys:
        return seo_gen.tools_links(B, lang)
    E = B.E
    links = ''.join(f'<a href="{B.PATH[k](lang)}">{E(page_label(B, k, lang))}</a>' for k in keys)
    return f'<section class="seo-sec"><h2>{E(UI[lang]["about"])}</h2><div class="quiet-links">{links}</div></section>'


def posts_for(key, lang, limit=3):
    """Straipsniai, rodomi puslapyje `key` (atvirkštinės nuorodos)."""
    if key == 'blog' or key.startswith(('b_', 'e_')) or key in ('embed', 'privacy'):
        return []
    ids = list(INDEX.get(key, []))
    if key.startswith('c_'):                      # c_<a>_<b>: palyginimas -> abiejų gėrimų straipsniai
        a, b = key.split('_')[1:3]
        ids = INDEX.get('d_' + a, []) + INDEX.get('d_' + b, [])
    elif key.startswith('br_'):
        ids = INDEX.get('hub_b', [])
    elif key.startswith('tl_'):
        ids = INDEX.get(key, []) + INDEX.get('d_' + key[3:], []) + INDEX.get('hub_t', [])
    if not ids and (key in GENERIC or key == 'home' or key.startswith('tl_')):
        ids = list(POSTS)
    ids = [p for p in dict.fromkeys(ids) if lang in POSTS[p]]
    ids.sort(key=lambda p: (POSTS[p][lang]['date'], p), reverse=True)
    return ids[:limit]


def augment(B, key, lang, main):
    """Į kitus puslapius (B.shell) įdeda „Skaityk daugiau“ su susijusiais straipsniais."""
    ids = posts_for(key, lang, 3 if key != 'home' else 3)
    if not ids:
        return main
    E = B.E
    u = UI[lang]
    cards = ''.join(_card(B, lang, p) for p in ids)
    if key == 'home':
        sec = (f'<section class="wrap sec" id="blog"><div class="sec-head"><h2 class="sec-title">{E(u["home_t"])}</h2>'
               f'<p class="sec-sub">{E(u["home_sub"])}</p></div><div class="grid">{cards}</div>'
               f'<p style="margin-top:24px"><a class="btn btn-outline btn-sm" href="{B.PATH["blog"](lang)}">{E(u["all"])} →</a></p></section>\n')
        anchor = '<section class="wrap sec" id="shop">'
        return main.replace(anchor, sec + anchor, 1) if anchor in main else main
    sec = f'<section class="seo-sec post-more"><h2>{E(u["more"])}</h2><div class="grid">{cards}</div></section>\n'
    i = main.rfind('</main>')
    return main[:i] + sec + main[i:] if i >= 0 else main


def validate(B):
    for k in INDEX:
        if k not in B.PATH:
            raise ValueError(f'about: nežinomas puslapio raktas {k} (straipsniai: {INDEX[k]})')
        page_label(B, k, 'lt')


def post_page(B, lang, pid):
    E = B.E
    m = POSTS[pid][lang]
    u = UI[lang]
    t = seo_gen.L[lang]
    key = key_p(pid)
    body, heads = render(B, lang, m['body'])
    toc = ''
    if len(heads) >= 3:
        toc = (f'<nav class="toc" aria-label="{E(u["toc"])}"><strong>{E(u["toc"])}</strong><ol>'
               + ''.join(f'<li><a href="#{i}">{E(h)}</a></li>' for i, h in heads) + '</ol></nav>')
    upd = f' · {E(u["updated"])} <time datetime="{m["updated"]}">{E(fmt_date(m["updated"], lang))}</time>' if m.get('updated') else ''
    rel = related_ids(pid, lang)
    related = ''
    if rel:
        related = f'<section class="seo-sec"><h2>{E(u["related"])}</h2><div class="grid">' + ''.join(_card(B, lang, r) for r in rel) + '</div></section>'
    srcs = ''
    if m['sources']:
        items = ''.join(f'<li><a href="{source(k)[1]}" target="_blank" rel="noopener nofollow">{E(source(k)[0])}</a></li>' for k in m['sources'])
        srcs = (f'<section class="seo-sec"><h2>{E(t["h_src"])}</h2><ul class="small srclist">{items}</ul>'
                f'<p class="small">{E(t["src_note"].format(d=m.get("updated") or m["date"]))}</p></section>')
    url = B.BASE + B.PATH[key](lang)
    org = {'@type': 'Organization', 'name': 'Arbata', 'url': B.BASE + '/'}
    ld = [
        _crumb_ld(B, lang, [(t['home'], B.BASE + B.PATH['home'](lang)), (u['blog'], B.BASE + B.PATH['blog'](lang)), (m['title'], url)]),
        {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': m['title'], 'description': m['description'],
         'datePublished': m['date'], 'dateModified': m.get('updated') or m['date'], 'inLanguage': lang,
         'mainEntityOfPage': url, 'url': url, 'author': org, 'publisher': org, 'articleSection': CATS[m['category']][lang]},
    ]
    main = f'''<main id="main" class="wrap wrap-narrow seo post">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <a href="{B.PATH['blog'](lang)}">{E(u['blog'])}</a> / <span>{E(m['title'])}</span></div>
<article class="post-art">
<header class="post-head">
<p class="post-meta"><span class="chip">{E(CATS[m['category']][lang])}</span><time datetime="{m['date']}">{E(fmt_date(m['date'], lang))}</time><span>· {read_min(m['body'])} {E(u['min'])}</span>{upd}</p>
<h1 class="page-title">{E(m['title'])}</h1>
</header>
{toc}
<div class="post-body">
{body}
</div>
</article>
<p class="answer small">{E(t['g_note'])}</p>
{related}
{about_block(B, lang, m)}
{srcs}
</main>
{_ld(B, lang, ld)}'''
    out = B.shell(lang, key, m['title'], m['description'], main)
    out = out.replace('<meta property="og:type" content="website">',
                      f'<meta property="og:type" content="article"><meta property="article:published_time" content="{m["date"]}">', 1)
    return out.replace('</head>', _rss_link(B, lang) + '</head>', 1)


def feed(B, lang):
    E = lambda s: html.escape(s, quote=False)
    u = UI[lang]
    items = ''
    for pid in _sorted_ids(lang):
        m = POSTS[pid][lang]
        url = B.BASE + B.PATH[key_p(pid)](lang)
        dt = datetime.datetime.fromisoformat(m['date']).replace(tzinfo=datetime.timezone.utc)
        items += (f'<item><title>{E(m["title"])}</title><link>{url}</link><guid isPermaLink="true">{url}</guid>'
                  f'<pubDate>{email.utils.format_datetime(dt)}</pubDate><description>{E(m["description"])}</description></item>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f'<title>Arbata: {E(u["blog"])}</title><link>{B.BASE}{B.PATH["blog"](lang)}</link>'
            f'<description>{E(u["desc"])}</description><language>{lang}</language>\n{items}</channel></rss>\n')


def _newtab(html, lang):
    """Straipsnyje visos nuorodos į įrankius ir kitus svetainės puslapius (ne blogas, ne pagrindinis) atsidaro naujame lange."""
    import re
    a, b = html.find('<main'), html.find('</main>')
    if a < 0 or b < 0:
        return html
    def f(m):
        tag = m.group(0)
        h = m.group(1)
        if 'target=' in tag or h == f'/{lang}/' or h.startswith(f'/{lang}/blog/') or not h.startswith('/'):
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return html[:a] + re.sub(r'<a href="([^"]*)"[^>]*>', f, html[a:b]) + html[b:]


def pages(B):
    validate(B)
    out = []
    for lang in B.LANGS:
        out.append((B.PATH['blog'](lang) + 'index.html', index_page(B, lang)))
        out.append((B.PATH['blog'](lang) + 'feed.xml', feed(B, lang)))
        for pid in sorted(POSTS):
            if lang in POSTS[pid]:
                out.append((B.PATH[key_p(pid)](lang) + 'index.html', _newtab(post_page(B, lang, pid), lang)))
    return out
