"""Arbatų markių kofeino duomenys (surinkta 2026-10-24, projekto failas claude/arbatu-kofeinas.json, 77 eilutės).
rel: high = gamintojo puslapis; medium = gamintojo etiketė / atstovo atsakymas; low = platintojas ar agregatorius (rodoma kaip „orientacinis“).
ml: porcijos tūris; 1000 = mg litrui (RTD gėrimai); None = nežinoma. lo/hi gali būti None (tik riba: „75+“, „iki 150“).
qual = kokybinio lygio raktas (QUAL), kai gamintojas nurodo tik lygį."""

U = {
    'bigelow': 'https://www.bigelowtea.com/blogs/tea-education/caffeine-in-tea',
    'bigelow_cc': 'https://www.bigelowtea.com/blogs/tea-education/bigelow-constant-comment-tea',
    'pf': 'https://www.pfanner.com/en/fruit-facts/how-much-caffeine-do-pfanners-tea-beverages-contain/',
    'pfw': 'https://pfanner.com/en/products/world-of-teas',
    'lip_y': 'https://www.publix.com/pd/lipton-yellow-label-black-tea/RIO-PCI-103556',
    'lip_ci': 'https://www.caffeineinformer.com/caffeine-content/lipton-tea',
    'lip_ne': 'https://www.caffeineinformer.com/caffeine-content/lipton-natural-energy-tea',
    'lip_eb': 'https://www.lipton.com/us/en/our-teas/english-breakfast-black-tea-20-pyramid-tea-bags/',
    'lip_sg': 'https://www.lipton.com/us/en/our-teas/signature-blend-green-tea-40-tea-bags/',
    'lip_faq': 'https://www.lipton.com/us/en/faqs/',
    'yogi_g': 'https://yogi-life.com/en-US/product/green-tea-pure-green-076950450424',
    'yogi_v': 'https://www.vitacost.com/yogi-perfect-energy-herbal-tea-vanilla-spice',
    'yogi_m': 'https://merchant.freshop.com/shop/yogi_refreshing_mint_vital_energy_tea_bags_16_ct/p/2403964',
    'yogi_k': 'https://shop.pharmasave.com/store/yogi-herbal-tea-green-tea-kombucha-16s',
    'yogi_b': 'https://well.ca/products/yogi-tea-spiced-blackberrry-focus_304371.html',
    'tw1': 'https://www.target.com/p/twinings-pure-peppermint-tea-100ct/-/A-89862869',
    'tw2': 'https://www.target.com/p/twinings-green-tea-k-cup-24ct/-/A-85797474',
    'tw_uk': 'https://twinings.co.uk/pages/faqs',
    'tw_au': 'https://twinings.com.au/blogs/all-about-tea/tea-and-caffeine',
    'tee': 'https://www.rewe.de/shop/p/teekanne-bio-power-t-minze-75g/7753588',
    'tazo': 'https://www.caffeineinformer.com/caffeine-content/tazo-chai',
    'tazo_pu': 'https://www.tazo.com/us/en/product-benefits/tazo-teas-for-pick-me-up/',
    'stash': 'https://www.nassaucandy.com/stash-decaf-earl-grey-18tb.html',
    'stash_pol': 'https://www.stashtea.com/blogs/education/black-chai-green-tea-do-they-have-caffeine',
    'harney': 'https://uk.iherb.com/pr/harney-sons-oolong-tea-strawberry-milkshake-30-sachets-2-67-oz-75-g/154673',
    'harney_o': 'https://www.harney.com/blogs/news/clean-caffeine',
    'ahmad': 'https://www.walmart.com/ip/seort/2040289686',
    'dilmah': 'https://shop.dilmah.sg/products/premium-ceylon-black-tea-100-tea-bags',
    'clipper': 'https://caffeineadvisor.com/caffeine-in-tea/clipper-tea/',
    'numi': 'https://caffeineadvisor.com/?p=1269',
    'numi_faq': 'https://numitea.com/pages/faq',
    'york': 'https://howmuchblog.com/?p=29811',
    'pgtips': 'https://discover.texasrealfood.com/the-art-of-enough/how-many-cups-of-pg-tips-tea-per-day-is-too-much',
    'tet_us': 'https://www.tetleyusa.com/tetley-tea-faq',
    'tet_uk': 'https://www.tetley.co.uk/help/',
    'tata': 'https://www.tataconsumer.com/frequently-asked-questions',
    'cs_be': 'https://celestialseasonings.com/products/energy-black',
    'cs_eb': 'https://celestialseasonings.com/products/english-breakfast-black-tea',
    'cs_gr': 'https://celestialseasonings.com/products/authentic-green-tea-1',
    'cs_mt': 'https://celestialseasonings.com/products/morning-thunder',
    'cs_bl': 'https://celestialseasonings.com/blogs/teas/black-tea',
    'rot_c': 'https://www.republicoftea.com/products/caramel-black-hicaf-tea-bags',
    'rot_l': 'https://www.republicoftea.com/blogs/tea-library/which-tea-has-the-most-caffeine',
    'tpigs': 'https://www.teapigs.co.uk/pages/about-decaf',
    'rishi': 'https://rishi-tea.com/collections/high-caffeine',
    'dav': 'https://help.davidstea.com/how-much-caffeine-is-there-in-a-cup-of-tea-775228',
}

BRANDS = [
    ('lipton', 'Lipton'), ('bigelow', 'Bigelow'), ('pfanner', 'Pfanner'), ('yogi-tea', 'Yogi Tea'),
    ('twinings', 'Twinings'), ('tetley', 'Tetley'), ('celestial-seasonings', 'Celestial Seasonings'),
    ('republic-of-tea', 'The Republic of Tea'), ('teapigs', 'teapigs'), ('rishi-tea', 'Rishi Tea'),
    ('davidstea', 'DAVIDsTEA'), ('teekanne', 'Teekanne'), ('harney-sons', 'Harney & Sons'), ('numi', 'Numi'),
    ('tazo', 'Tazo'), ('dilmah', 'Dilmah'), ('stash', 'Stash'), ('ahmad-tea', 'Ahmad Tea'),
    ('clipper', 'Clipper'), ('yorkshire-tea', 'Yorkshire Tea'), ('pg-tips', 'PG Tips'),
]

# brand_slug, produktas, tipas, min, max, avg, ml, rel, url, qual
R = [
    ('lipton', 'Yellow Label Black Tea (US)', 'black', 46, 70, 58, 237, 'medium', 'lip_y', None),
    ('lipton', 'Black tea', 'black', 55, 55, 55, 237, 'low', 'lip_ci', None),
    ('lipton', 'Decaf black tea', 'decaf', 5, 5, 5, 237, 'low', 'lip_ci', None),
    ('lipton', 'Green tea', 'green', 35, 35, 35, 237, 'low', 'lip_ci', None),
    ('lipton', 'Green tea with citrus', 'green', 25, 25, 25, 237, 'low', 'lip_ci', None),
    ('lipton', 'Natural Energy Tea (K-cup)', 'black', 75, 75, 75, 237, 'low', 'lip_ne', None),
    ('bigelow', 'Black teas (category)', 'black', 30, 60, 45, 237, 'high', 'bigelow', None),
    ('bigelow', 'Green teas incl. matcha (category)', 'green', 25, 50, 37.5, 237, 'high', 'bigelow', None),
    ('bigelow', 'Decaffeinated teas (category)', 'decaf', 1, 8, 4.5, 237, 'high', 'bigelow', None),
    ('bigelow', 'Herbal teas (category)', 'herbal', 0, 0, 0, 237, 'high', 'bigelow', None),
    ('bigelow', 'American Breakfast Black Tea', 'black', 60, 90, 75, 237, 'high', 'bigelow', None),
    ('bigelow', 'Peak Energy (+ L-theanine)', 'black', 75, 75, 75, 237, 'high', 'bigelow', None),
    ('pfanner', 'The Green One', 'rtd_green', 40, 70, 55, 1000, 'high', 'pf', None),
    ('pfanner', 'Iced Tea Lemon-Lime', 'rtd_black', 40, 70, 55, 1000, 'high', 'pf', None),
    ('pfanner', 'Iced Tea Peach', 'rtd_black', 40, 70, 55, 1000, 'high', 'pf', None),
    ('pfanner', 'Pure Tea Green Tea', 'rtd_green', 40, 70, 55, 1000, 'high', 'pf', None),
    ('pfanner', 'Pure Tea White Tea', 'rtd_white', 20, 30, 25, 1000, 'high', 'pfw', None),
    ('pfanner', 'Iced Tea Mango-Passion Fruit', 'rtd_black', 40, 60, 50, 1000, 'high', 'pfw', None),
    ('yogi-tea', 'Green Tea Pure Green', 'green', 58, 58, 58, 237, 'high', 'yogi_g', None),
    ('yogi-tea', 'Perfect Energy Vanilla Spice', 'blend', 75, 75, 75, 237, 'medium', 'yogi_v', None),
    ('yogi-tea', 'Refreshing Mint Vital Energy', 'blend', 77, 77, 77, 237, 'medium', 'yogi_m', None),
    ('yogi-tea', 'Green Tea Kombucha', 'green', 15, 15, 15, 237, 'medium', 'yogi_k', None),
    ('yogi-tea', 'Spiced Blackberry Focus', 'black', 50, 50, 50, 237, 'medium', 'yogi_b', None),
    ('twinings', 'Most teas (US)', 'blend', 19, 45, 32, 207, 'medium', 'tw1', None),
    ('twinings', 'Unflavoured teas, e.g. English Breakfast (US)', 'black', 40, 76, 58, 207, 'medium', 'tw2', None),
    ('teekanne', 'Bio Power-T Minze', 'blend', 40, 40, 40, 100, 'medium', 'tee', None),
    ('tazo', 'Chai', 'black', 47, 47, 47, 237, 'low', 'tazo', None),
    ('stash', 'Earl Grey', 'black', 40, 40, 40, None, 'low', 'stash', None),
    ('stash', 'Decaf Earl Grey', 'decaf', 0, 6, 3, None, 'low', 'stash', None),
    ('harney-sons', 'Oolong Strawberry Milkshake', 'oolong', 40, 60, 50, None, 'low', 'harney', None),
    ('ahmad-tea', 'English Tea No. 1', 'black', 60, 60, 60, None, 'low', 'ahmad', None),
    ('dilmah', 'Premium Ceylon Black Tea', 'black', None, None, None, None, 'medium', 'dilmah', 'medium'),
    ('tetley', 'Black and green tea (US)', 'black_green', 40, 50, 45, 237, 'high', 'tet_us', None),
    ('tetley', 'Decaf tea (US)', 'decaf', 4, 6, 5, 237, 'high', 'tet_us', None),
    ('tetley', 'Black tea (UK, 250 ml cup)', 'black', 30, 50, 40, 250, 'high', 'tet_uk', None),
    ('tetley', 'Black tea (UK, 190 ml cup, Tata FAQ)', 'black_green', 30, 50, 40, 190, 'high', 'tata', None),
    ('tetley', 'Decaf tea (UK)', 'decaf', 2.5, 2.5, 2.5, None, 'high', 'tet_uk', None),
    ('twinings', 'Black, green, white, oolong (UK)', 'blend', 30, 50, 40, 200, 'high', 'tw_uk', None),
    ('twinings', 'Standard black tea, average (UK)', 'black', 50, 50, 50, None, 'high', 'tw_uk', None),
    ('twinings', 'Decaf bag (UK)', 'decaf', 3, 3, 3, None, 'high', 'tw_uk', None),
    ('twinings', 'Strong black teas (Australia)', 'black', 0, 60, 30, None, 'high', 'tw_au', None),
    ('lipton', 'English Breakfast Pyramid (US)', 'black', 46, 70, 58, None, 'high', 'lip_eb', None),
    ('lipton', 'Signature Blend Green Tea (US)', 'green', 6, 30, 18, None, 'high', 'lip_sg', None),
    ('lipton', 'Black tea (US FAQ)', 'black', 55, 55, 55, None, 'high', 'lip_faq', None),
    ('lipton', 'Green tea (US FAQ)', 'green', 45, 45, 45, None, 'high', 'lip_faq', None),
    ('celestial-seasonings', 'Black Energy (vanilla)', 'blend', 95, 95, 95, None, 'high', 'cs_be', None),
    ('celestial-seasonings', 'English Breakfast', 'black', 60, 60, 60, None, 'high', 'cs_eb', None),
    ('celestial-seasonings', 'Authentic Green Tea', 'green', 35, 35, 35, None, 'high', 'cs_gr', None),
    ('celestial-seasonings', 'Morning Thunder', 'blend', 35, 35, 35, None, 'high', 'cs_mt', None),
    ('celestial-seasonings', 'Black teas (category)', 'black', 50, 70, 60, None, 'high', 'cs_bl', None),
    ('republic-of-tea', 'HiCAF Caramel Black Tea', 'black', 123, 123, 123, 177, 'high', 'rot_c', None),
    ('republic-of-tea', 'HiCAF blends (up to)', 'black', None, 150, None, 177, 'high', 'rot_l', None),
    ('republic-of-tea', 'Black tea (average)', 'black', 50, 50, 50, 177, 'high', 'rot_l', None),
    ('republic-of-tea', 'Green tea (average)', 'green', 25, 25, 25, 177, 'high', 'rot_l', None),
    ('republic-of-tea', 'White tea (average)', 'white', 10, 10, 10, 177, 'high', 'rot_l', None),
    ('republic-of-tea', 'Decaf tea', 'decaf', 2, 4, 3, 177, 'high', 'rot_l', None),
    ('harney-sons', 'Teas in general (no herbals)', 'blend', 40, 60, 50, None, 'high', 'harney_o', None),
    ('teapigs', 'Black tea (general)', 'black', 75, 75, 75, None, 'high', 'tpigs', None),
    ('teapigs', 'Green tea (general)', 'green', 30, 30, 30, None, 'high', 'tpigs', None),
    ('teapigs', 'Decaf', 'decaf', 2, 2, 2, None, 'high', 'tpigs', None),
    ('numi', 'All teas (general)', 'blend', 15, 70, 42.5, None, 'high', 'numi_faq', None),
    ('bigelow', 'Constant Comment (black)', 'black', 30, 60, 45, None, 'high', 'bigelow_cc', None),
    ('tazo', 'Pick-me-up teas (at least)', 'black', 75, None, None, None, 'high', 'tazo_pu', None),
    ('rishi-tea', 'High caffeine collection (up to)', 'blend', None, 100, None, None, 'high', 'rishi', 'high'),
    ('davidstea', 'Caffeine level: none', 'herbal', 0, 0, 0, None, 'high', 'dav', 'none'),
    ('davidstea', 'Caffeine level: low', 'blend', 1, 19, 10, None, 'high', 'dav', 'low'),
    ('davidstea', 'Caffeine level: medium', 'blend', 20, 39, 29.5, None, 'high', 'dav', 'medium'),
    ('davidstea', 'Caffeine level: high (at least)', 'blend', 40, None, None, None, 'high', 'dav', 'high'),
    ('stash', 'Teas (company policy)', 'blend', None, None, None, None, 'high', 'stash_pol', 'nomg'),
    ('clipper', 'Black teas', 'black', 40, 70, 55, 237, 'low', 'clipper', None),
    ('clipper', 'Green teas', 'green', 20, 45, 32.5, 237, 'low', 'clipper', None),
    ('clipper', 'Decaffeinated teas', 'decaf', 0, 2, 1, 237, 'low', 'clipper', None),
    ('numi', 'Breakfast Blend', 'black', 40, 70, 55, 237, 'low', 'numi', None),
    ('numi', 'Gunpowder Green', 'green', 30, 50, 40, 237, 'low', 'numi', None),
    ('numi', 'White Rose', 'white', 15, 30, 22.5, 237, 'low', 'numi', None),
    ('yorkshire-tea', 'Standard black tea', 'black', 40, 60, 50, 237, 'low', 'york', None),
    ('pg-tips', 'Black tea', 'black', 40, 50, 45, 200, 'low', 'pgtips', None),
]

QUAL = {
    'medium': {'lt': 'Vidutinis', 'en': 'Medium', 'it': 'Medio'},
    'none': {'lt': 'Be kofeino', 'en': 'Caffeine-free', 'it': 'Senza caffeina'},
    'low': {'lt': 'Žemas', 'en': 'Low', 'it': 'Basso'},
    'high': {'lt': 'Aukštas', 'en': 'High', 'it': 'Alto'},
    'nomg': {'lt': 'Gamintojas mg nenurodo', 'en': 'Manufacturer does not state mg', 'it': 'Il produttore non indica i mg'},
}

TYPE = {
    'black': {'lt': 'Juodoji', 'en': 'Black', 'it': 'Nero'},
    'green': {'lt': 'Žalioji', 'en': 'Green', 'it': 'Verde'},
    'black_green': {'lt': 'Juodoji / žalioji', 'en': 'Black / green', 'it': 'Nero / verde'},
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
    for n, (b, prod, typ, lo, hi, avg, ml, rel, url, qual) in enumerate(R):
        r = {'n': n, 'brand': b, 'product': prod, 'type': typ, 'lo': lo, 'hi': hi, 'avg': avg, 'ml': ml,
             'rel': rel, 'url': U[url], 'rtd': ml == 1000, 'qual': qual}
        r['p100'] = round(avg / ml * 100, 1) if (ml and avg is not None) else None
        out.append(r)
    return out


def has_num(r):
    return r['lo'] is not None or r['hi'] is not None


def official(r):
    return r['rel'] in ('high', 'medium') and has_num(r)


def for_brand(slug):
    return [r for r in rows() if r['brand'] == slug]


def tool_drinks():
    """Markių įrašai įrankių pasirinkimui (tik oficialūs, pilni skaičiai, žinomas tūris): RTD ir mažos porcijos perskaičiuojamos."""
    out = []
    for r in rows():
        if not official(r) or r['lo'] is None or r['hi'] is None or not r['avg'] or not r['ml']:
            continue
        name = brand_name(r['brand']) + ' ' + r['product']
        ml, lo, hi, typ = r['ml'], r['lo'], r['hi'], r['avg']
        if not (170 <= ml <= 260):
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
