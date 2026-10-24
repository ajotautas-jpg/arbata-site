"""Arbatų markių kofeino duomenys (surinkta 2026-10-24, projekto failas claude/arbatu-kofeinas.json).
rel: high = gamintojo puslapis; medium = gamintojo etiketė / atstovo atsakymas; low = platintojas ar agregatorius (rodoma kaip „orientacinis“).
ml: porcijos tūris; 1000 = mg litrui (RTD gėrimai); None = nežinoma. qual = tik kokybinis lygis."""

U = {
    'bigelow': 'https://www.bigelowtea.com/blogs/tea-education/caffeine-in-tea',
    'pf': 'https://www.pfanner.com/en/fruit-facts/how-much-caffeine-do-pfanners-tea-beverages-contain/',
    'pfw': 'https://pfanner.com/en/products/world-of-teas',
    'lip_y': 'https://www.publix.com/pd/lipton-yellow-label-black-tea/RIO-PCI-103556',
    'lip_ci': 'https://www.caffeineinformer.com/caffeine-content/lipton-tea',
    'lip_ne': 'https://www.caffeineinformer.com/caffeine-content/lipton-natural-energy-tea',
    'yogi_g': 'https://well.ca/products/yogi-tea-green-tea-pure-green_15678.html',
    'yogi_v': 'https://www.vitacost.com/yogi-perfect-energy-herbal-tea-vanilla-spice',
    'yogi_m': 'https://merchant.freshop.com/shop/yogi_refreshing_mint_vital_energy_tea_bags_16_ct/p/2403964',
    'yogi_k': 'https://shop.pharmasave.com/store/yogi-herbal-tea-green-tea-kombucha-16s',
    'yogi_b': 'https://well.ca/products/yogi-tea-spiced-blackberrry-focus_304371.html',
    'tw1': 'https://www.target.com/p/twinings-pure-peppermint-tea-100ct/-/A-89862869',
    'tw2': 'https://www.target.com/p/twinings-green-tea-k-cup-24ct/-/A-85797474',
    'tee': 'https://www.rewe.de/shop/p/teekanne-bio-power-t-minze-75g/7753588',
    'tazo': 'https://www.caffeineinformer.com/caffeine-content/tazo-chai',
    'stash': 'https://www.nassaucandy.com/stash-decaf-earl-grey-18tb.html',
    'harney': 'https://uk.iherb.com/pr/harney-sons-oolong-tea-strawberry-milkshake-30-sachets-2-67-oz-75-g/154673',
    'ahmad': 'https://www.walmart.com/ip/seort/2040289686',
    'dilmah': 'https://shop.dilmah.sg/products/premium-ceylon-black-tea-100-tea-bags',
    'clipper': 'https://caffeineadvisor.com/caffeine-in-tea/clipper-tea/',
    'numi': 'https://caffeineadvisor.com/?p=1269',
    'york': 'https://howmuchblog.com/?p=29811',
    'pgtips': 'https://discover.texasrealfood.com/the-art-of-enough/how-many-cups-of-pg-tips-tea-per-day-is-too-much',
}

# slug, rodomas pavadinimas, tikroji šalis/pastaba nereikalinga
BRANDS = [
    ('lipton', 'Lipton'), ('bigelow', 'Bigelow'), ('pfanner', 'Pfanner'), ('yogi-tea', 'Yogi Tea'),
    ('twinings', 'Twinings'), ('teekanne', 'Teekanne'), ('dilmah', 'Dilmah'), ('tazo', 'Tazo'),
    ('stash', 'Stash'), ('harney-sons', 'Harney & Sons'), ('ahmad-tea', 'Ahmad Tea'), ('clipper', 'Clipper'),
    ('numi', 'Numi'), ('yorkshire-tea', 'Yorkshire Tea'), ('pg-tips', 'PG Tips'),
]

# brand_slug, produktas, tipas, min, max, avg, ml, rel, url, tipo kodas
# tipas: black green white oolong herbal decaf blend rtd_black rtd_green rtd_white
R = [
    ('lipton', 'Yellow Label Black Tea (US)', 'black', 46, 70, 58, 237, 'medium', 'lip_y'),
    ('lipton', 'Black tea', 'black', 55, 55, 55, 237, 'low', 'lip_ci'),
    ('lipton', 'Decaf black tea', 'decaf', 5, 5, 5, 237, 'low', 'lip_ci'),
    ('lipton', 'Green tea', 'green', 35, 35, 35, 237, 'low', 'lip_ci'),
    ('lipton', 'Green tea with citrus', 'green', 25, 25, 25, 237, 'low', 'lip_ci'),
    ('lipton', 'Natural Energy Tea (K-cup)', 'black', 75, 75, 75, 237, 'low', 'lip_ne'),
    ('bigelow', 'Black teas (category)', 'black', 30, 60, 45, 237, 'high', 'bigelow'),
    ('bigelow', 'Green teas incl. matcha (category)', 'green', 25, 50, 37.5, 237, 'high', 'bigelow'),
    ('bigelow', 'Decaffeinated teas (category)', 'decaf', 1, 8, 4.5, 237, 'high', 'bigelow'),
    ('bigelow', 'Herbal teas (category)', 'herbal', 0, 0, 0, 237, 'high', 'bigelow'),
    ('bigelow', 'American Breakfast Black Tea', 'black', 60, 90, 75, 237, 'high', 'bigelow'),
    ('bigelow', 'Peak Energy (+ L-theanine)', 'black', 75, 75, 75, 237, 'high', 'bigelow'),
    ('pfanner', 'The Green One', 'rtd_green', 40, 70, 55, 1000, 'high', 'pf'),
    ('pfanner', 'Iced Tea Lemon-Lime', 'rtd_black', 40, 70, 55, 1000, 'high', 'pf'),
    ('pfanner', 'Iced Tea Peach', 'rtd_black', 40, 70, 55, 1000, 'high', 'pf'),
    ('pfanner', 'Pure Tea Green Tea', 'rtd_green', 40, 70, 55, 1000, 'high', 'pf'),
    ('pfanner', 'Pure Tea White Tea', 'rtd_white', 20, 30, 25, 1000, 'high', 'pfw'),
    ('pfanner', 'Iced Tea Mango-Passion Fruit', 'rtd_black', 40, 60, 50, 1000, 'high', 'pfw'),
    ('yogi-tea', 'Green Tea Pure Green', 'green', 58, 58, 58, 237, 'medium', 'yogi_g'),
    ('yogi-tea', 'Perfect Energy Vanilla Spice', 'blend', 75, 75, 75, 237, 'medium', 'yogi_v'),
    ('yogi-tea', 'Refreshing Mint Vital Energy', 'blend', 77, 77, 77, 237, 'medium', 'yogi_m'),
    ('yogi-tea', 'Green Tea Kombucha', 'green', 15, 15, 15, 237, 'medium', 'yogi_k'),
    ('yogi-tea', 'Spiced Blackberry Focus', 'black', 50, 50, 50, 237, 'medium', 'yogi_b'),
    ('twinings', 'Most teas (US)', 'blend', 19, 45, 32, 207, 'medium', 'tw1'),
    ('twinings', 'Unflavoured teas, e.g. English Breakfast (US)', 'black', 40, 76, 58, 207, 'medium', 'tw2'),
    ('teekanne', 'Bio Power-T Minze', 'blend', 40, 40, 40, 100, 'medium', 'tee'),
    ('tazo', 'Chai', 'black', 47, 47, 47, 237, 'low', 'tazo'),
    ('stash', 'Earl Grey', 'black', 40, 40, 40, None, 'low', 'stash'),
    ('stash', 'Decaf Earl Grey', 'decaf', 0, 6, 3, None, 'low', 'stash'),
    ('harney-sons', 'Oolong Strawberry Milkshake', 'oolong', 40, 60, 50, None, 'low', 'harney'),
    ('ahmad-tea', 'English Tea No. 1', 'black', 60, 60, 60, None, 'low', 'ahmad'),
    ('dilmah', 'Premium Ceylon Black Tea', 'black', None, None, None, None, 'medium', 'dilmah'),
    ('clipper', 'Black teas', 'black', 40, 70, 55, 237, 'low', 'clipper'),
    ('clipper', 'Green teas', 'green', 20, 45, 32.5, 237, 'low', 'clipper'),
    ('clipper', 'Decaffeinated teas', 'decaf', 0, 2, 1, 237, 'low', 'clipper'),
    ('numi', 'Breakfast Blend', 'black', 40, 70, 55, 237, 'low', 'numi'),
    ('numi', 'Gunpowder Green', 'green', 30, 50, 40, 237, 'low', 'numi'),
    ('numi', 'White Rose', 'white', 15, 30, 22.5, 237, 'low', 'numi'),
    ('yorkshire-tea', 'Standard black tea', 'black', 40, 60, 50, 237, 'low', 'york'),
    ('pg-tips', 'Black tea', 'black', 40, 50, 45, 200, 'low', 'pgtips'),
]

# Šaltinio rūšis pagal patikimumą ir (Dilmah) kokybinis lygis
QUAL = {'dilmah': {'lt': 'Vidutinis', 'en': 'Medium', 'it': 'Medio'}}

TYPE = {
    'black': {'lt': 'Juodoji', 'en': 'Black', 'it': 'Nero'},
    'green': {'lt': 'Žalioji', 'en': 'Green', 'it': 'Verde'},
    'white': {'lt': 'Baltoji', 'en': 'White', 'it': 'Bianco'},
    'oolong': {'lt': 'Oolong', 'en': 'Oolong', 'it': 'Oolong'},
    'herbal': {'lt': 'Žolelių', 'en': 'Herbal', 'it': 'Erbe'},
    'decaf': {'lt': 'Be kofeino', 'en': 'Decaf', 'it': 'Decaffeinato'},
    'blend': {'lt': 'Mišinys', 'en': 'Blend', 'it': 'Miscela'},
    'rtd_black': {'lt': 'Juodoji (paruošta gerti)', 'en': 'Black (ready to drink)', 'it': 'Nero (pronto da bere)'},
    'rtd_green': {'lt': 'Žalioji (paruošta gerti)', 'en': 'Green (ready to drink)', 'it': 'Verde (pronto da bere)'},
    'rtd_white': {'lt': 'Baltoji (paruošta gerti)', 'en': 'White (ready to drink)', 'it': 'Bianco (pronto da bere)'},
}


def brand_name(slug):
    return dict(BRANDS)[slug]


def rows():
    out = []
    for n, (b, prod, typ, lo, hi, avg, ml, rel, url) in enumerate(R):
        r = {'n': n, 'brand': b, 'product': prod, 'type': typ, 'lo': lo, 'hi': hi, 'avg': avg, 'ml': ml,
             'rel': rel, 'url': U[url], 'rtd': ml == 1000, 'qual': b in QUAL and lo is None}
        if ml and lo is not None:
            r['p100'] = round(avg / ml * 100, 1)
        else:
            r['p100'] = None
        out.append(r)
    return out


def official(r):
    return r['rel'] in ('high', 'medium') and r['lo'] is not None


def for_brand(slug):
    return [r for r in rows() if r['brand'] == slug]


def tool_drinks():
    """Markių įrašai įrankių pasirinkimui (tik oficialūs): puodelio dydis ~237 ml, RTD ir mažos porcijos perskaičiuojamos."""
    out = []
    for r in rows():
        if not official(r) or not r['avg']:
            continue
        name = brand_name(r['brand']) + ' ' + r['product']
        ml, lo, hi, typ = r['ml'], r['lo'], r['hi'], r['avg']
        if ml and not (200 <= ml <= 240):
            k = 250 / ml if ml == 1000 else 237 / ml
            ml2 = 250 if ml == 1000 else 237
            lo, hi, typ = lo * k, hi * k, typ * k
            ml = ml2
        lo, hi, typ = int(lo + 0.5), int(hi + 0.5), int(typ + 0.5)
        nm = f'{name} ({ml} ml)'
        out.append({'id': f'b{r["n"]}', 'group': 'brand', 'lo': lo, 'hi': hi, 'typ': typ, 'ml': ml, 'g': 0,
                    'src': [], 'conf': 'high' if r['rel'] == 'high' else 'medium', 'url': r['url'],
                    'names': {'lt': nm, 'en': nm, 'it': nm}})
    return out
