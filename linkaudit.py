#!/usr/bin/env python3
"""Vidinių nuorodų auditas po `python3 build.py`: sugedusios nuorodos, puslapiai be įeinančių nuorodų (našlaičiai), blogo nuorodų skaičiai.
Naudojimas: python3 linkaudit.py"""
import glob, os, re, sys
from collections import defaultdict

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
pages = {}
for f in glob.glob(D + '/**/index.html', recursive=True):
    rel = os.path.relpath(os.path.dirname(f), D).replace(os.sep, '/')
    url = '/' if rel == '.' else '/' + rel + '/'
    pages[url] = open(f, encoding='utf-8').read()

inb, outb, broken = defaultdict(set), defaultdict(set), []
for url, s in pages.items():
    body = re.sub(r'<(header|footer|nav)\b.*?</\1>', '', s, flags=re.S)       # tik turinio nuorodos
    for h in set(re.findall(r'<a [^>]*href="(/[^"#?]*)"', body)):
        if '.' in os.path.basename(h.rstrip('/')) and not h.endswith('/'):
            if not os.path.exists(D + h):
                broken.append((url, h))
            continue
        h = h if h.endswith('/') else h + '/'
        if h not in pages:
            broken.append((url, h))
        elif h != url:
            outb[url].add(h); inb[h].add(url)

print(f'puslapių: {len(pages)}, sugedusių nuorodų: {len(broken)}')
for b in broken[:20]: print('  SUGEDĘ', b)
noindex = {u for u, s in pages.items() if 'noindex' in s or '/ideti/' in u or '/embed/' in u or '/incorpora/' in u}
orph = sorted(u for u in pages if u not in noindex and u != '/' and not inb[u])
print(f'našlaičių (be įeinančių turinio nuorodų): {len(orph)}')
for u in orph[:40]: print('  NAŠLAITIS', u)
print('\nBlogas (įeinančios / išeinančios turinio nuorodos):')
for u in sorted(pages):
    if '/blog/' in u and u.count('/') >= 4:
        print(f'  {u}  in={len(inb[u])}  out={len(outb[u])}')
