"""Kofeino duomenų bazė su šaltiniais. Viskas, ką rodo įrankiai, ateina iš čia.
Skaičiai yra DIAPAZONAI; 'typ' yra orientacinis vidurkis (kai šaltiniai skiriasi, imamas vidurys).
Patikrinta: 2026-10-24."""

CHECKED = '2026-10-24'

SOURCES = {
    'mayo': ('Mayo Clinic: Caffeine content for coffee, tea, soda and more',
             'https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/caffeine/art-20049372'),
    'efsa': ('EUFIC: EFSA opinion on the safety of caffeine (2015)',
             'https://eufic.org/en/whats-in-food/article/efsa-opinion-on-the-safety-of-caffeine'),
    'fsanz': ('FSANZ P1056: caffeine safety assessment (half-life, EFSA values)',
              'https://mta-sts.foodstandards.govt.nz/sites/default/files/2025-03/P1056%20SD1%202nd%20CFS%20Safety%20Assessment.pdf'),
    'foods': ('Ayakdaş & Ağagündüz, Foods 2025;14(13):2313 (68 tea samples)',
              'https://pmc.ncbi.nlm.nih.gov/articles/PMC12248710'),
    'matcha': ('Medical News Today: matcha caffeine (19–44 mg/g, citing Kochman et al. 2020)',
               'https://www.medicalnewstoday.com/articles/does-matcha-have-caffeine'),
    'mate': ('Markowicz Bastos et al., Acta Farm. Bonaerense 2005;24(1):91–95 (yerba mate)',
             'https://www.e-lactancia.org/media/papers/MateCafeina-ActFarmBona2005.pdf'),
    'ci': ('Caffeine Informer: brewed tea (lab averages and brew-time tests)',
           'https://www.caffeineinformer.com/caffeine-content/tea-brewed'),
    'ci_mate': ('Caffeine Informer: yerba mate (producer data)',
                'https://www.caffeineinformer.com/caffeine-content/ymateina-yerba-mate'),
}

# Limitai ir farmakokinetika
LIMITS = {
    'adult_day': 400,      # mg / d., EFSA 2015
    'single': 200,         # mg viena doze, EFSA 2015
    'pregnancy_day': 200,  # mg / d., EFSA 2015
    'child_per_kg': 3,     # mg / kg / d., per BfR/EFSA (FSANZ)
    'sleep_note': 100,     # mg: EUFIC: apie 100 mg prieš miegą gali veikti miegą
    'half_life': [3, 5, 7],  # val.: diapazonas 3–7, centras ~5 (FSANZ)
}

# Laiko veiksnys (santykis su 5 min. plikymu), pagal Caffeine Informer bandymus (1/3/5 min.)
TIME_F = {2: 0.65, 3: 0.85, 4: 0.93, 5: 1.0}

# Arbatos: mg kofeino 1 g sausos arbatos ties 5 min. plikymu. [min, max], aptarnavimas g.
# Juodoji/žalioji/oolong/baltoji/pu-erh: puodelio diapazonas (2 g / 200–237 ml) iš Foods 2025 (apačia)
# ir Mayo/Caffeine Informer (viršus), padalinta iš 2 g.
TEAS = [
    # id, mg/g lo, mg/g hi, porcija g, visa lapo suvartojimas (matcha), šaltiniai, patikimumas
    ('black', 7.0, 24.0, 2, False, ['foods', 'mayo', 'ci'], 'medium'),
    ('green', 5.5, 14.5, 2, False, ['foods', 'mayo'], 'medium'),
    ('oolong', 2.0, 14.5, 2, False, ['foods'], 'medium'),
    ('white', 3.0, 15.5, 2, False, ['foods'], 'medium'),
    ('puerh', 6.5, 20.0, 2, False, ['foods'], 'medium'),
    ('mate', 10.8, 16.0, 5, False, ['mate', 'ci_mate'], 'low'),
    ('matcha', 18.9, 44.4, 2, True, ['matcha'], 'medium'),
]

TEA_NAMES = {
    'black': {'lt': 'Juodoji arbata', 'en': 'Black tea', 'it': 'Tè nero'},
    'green': {'lt': 'Žalioji arbata', 'en': 'Green tea', 'it': 'Tè verde'},
    'oolong': {'lt': 'Oolong', 'en': 'Oolong', 'it': 'Oolong'},
    'white': {'lt': 'Baltoji arbata', 'en': 'White tea', 'it': 'Tè bianco'},
    'puerh': {'lt': 'Pu-erh', 'en': 'Pu-erh', 'it': 'Pu-erh'},
    'mate': {'lt': 'Yerba mate', 'en': 'Yerba mate', 'it': 'Yerba mate'},
    'matcha': {'lt': 'Matcha', 'en': 'Matcha', 'it': 'Matcha'},
}

# Kiti gėrimai: id, grupė, lo, hi, typ, tūris ml, šaltiniai, patikimumas
OTHER = [
    ('espresso', 'coffee', 40, 63, 63, 30, ['mayo', 'efsa'], 'high'),
    ('filter', 'coffee', 80, 107, 96, 237, ['mayo', 'efsa'], 'high'),
    ('decaf', 'coffee', 1, 1, 1, 237, ['mayo'], 'high'),
    ('cola', 'other', 33, 33, 33, 237, ['mayo'], 'medium'),
    ('energy', 'other', 79, 79, 79, 237, ['mayo'], 'medium'),
    ('shot', 'other', 200, 200, 200, 60, ['mayo'], 'medium'),
]

OTHER_NAMES = {
    'espresso': {'lt': 'Espresas (30 ml)', 'en': 'Espresso (30 ml)', 'it': 'Espresso (30 ml)'},
    'filter': {'lt': 'Filtrinė kava (237 ml)', 'en': 'Filter coffee (237 ml)', 'it': 'Caffè filtro (237 ml)'},
    'decaf': {'lt': 'Kava be kofeino (237 ml)', 'en': 'Decaf coffee (237 ml)', 'it': 'Caffè decaffeinato (237 ml)'},
    'cola': {'lt': 'Kola (237 ml)', 'en': 'Cola (237 ml)', 'it': 'Cola (237 ml)'},
    'energy': {'lt': 'Energinis gėrimas (237 ml)', 'en': 'Energy drink (237 ml)', 'it': 'Energy drink (237 ml)'},
    'shot': {'lt': 'Energinis šotas (60 ml)', 'en': 'Energy shot (60 ml)', 'it': 'Energy shot (60 ml)'},
}


def r(x):
    return int(x + 0.5)


def tea_cup(tea_id):
    """Puodelio diapazonas (mg) ties numatyta porcija ir 5 min. plikymu."""
    for tid, lo, hi, g, whole, src, conf in TEAS:
        if tid == tea_id:
            return r(lo * g), r(hi * g), r((lo + hi) / 2 * g)
    raise KeyError(tea_id)


def drinks():
    """Vieningas gėrimų sąrašas įrankiams: id, grupė, lo, hi, typ, tūris, šaltiniai, patikimumas, vardai."""
    out = []
    for tid, lo, hi, g, whole, src, conf in TEAS:
        clo, chi, ctyp = tea_cup(tid)
        out.append({'id': tid, 'group': 'tea', 'lo': clo, 'hi': chi, 'typ': ctyp, 'ml': 237 if tid != 'matcha' else 200,
                    'g': g, 'perg': [lo, hi], 'whole': whole, 'src': src, 'conf': conf, 'names': TEA_NAMES[tid]})
    for did, grp, lo, hi, typ, ml, src, conf in OTHER:
        out.append({'id': did, 'group': grp, 'lo': lo, 'hi': hi, 'typ': typ, 'ml': ml, 'g': 0,
                    'src': src, 'conf': conf, 'names': OTHER_NAMES[did]})
    return out


def data_js():
    import json
    payload = {
        'checked': CHECKED,
        'limits': LIMITS,
        'timeF': {str(k): v for k, v in TIME_F.items()},
        'drinks': drinks() + __import__('brands_data').tool_drinks(),
        'sources': {k: {'title': v[0], 'url': v[1]} for k, v in SOURCES.items()},
    }
    return 'window.ARBATA_DATA=' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + ';\n'
