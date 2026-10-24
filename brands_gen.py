"""Arbatų markių puslapiai (LT/EN/IT): hub + puslapis kiekvienai markei. Duomenys: brands_data.py.
Rodomi diapazonai su šaltiniu; neoficialūs (low) duomenys pažymimi „orientacinis“. Markės be oficialių mg → noindex ir ne sitemap."""
import json
import caff
import brands_data as BD
import seo_gen as SG

DIR = {'lt': 'markes', 'en': 'brands', 'it': 'marche'}

T = {
 'lt': dict(
  hub='Arbatų markės', hub_h1='Kofeinas arbatų markėse', hub_t='Kiek kofeino yra arbatų markėse? Lipton, Bigelow, Twinings, Yogi',
  hub_desc='Kofeino kiekis populiarių arbatų markių maišeliuose: gamintojų duomenys su šaltiniais, diapazonai ir palyginimas su kava.',
  hub_lead='Gamintojai konkrečių arbatų kofeino kiekį skelbia retai, todėl šiame skyriuje atskiriame oficialius duomenis nuo orientacinių. Kofeino kiekis keičiasi pagal partiją ir plikymą.',
  th_brand='Markė', th_mg='Oficialūs duomenys, mg', th_n='Produktai', none='nėra oficialių mg', qual_only='tik kokybinis lygis',
  h_official='Markės su oficialiais duomenimis', h_other='Markės be oficialių mg (tik orientaciniai duomenys)',
  h1='Kiek kofeino yra {b} arbatoje?', t='Kiek kofeino yra {b} arbatoje? {rg}', t_none='Kiek kofeino yra {b} arbatoje?',
  d='{b}: kofeino kiekis arbatoje pagal šaltinius, {rg}. Lentelė su porcija, mg / 100 ml ir šaltinio nuorodomis.', d_none='{b}: kofeino kiekis arbatoje. Oficialių gamintojo duomenų nėra, rodome orientacinius šaltinius.',
  ans_off='Pagal {b} duomenis arbatos porcijoje yra {rg} kofeino (priklauso nuo produkto).', ans_low='Oficialių {b} kofeino duomenų neradome. Neoficialūs šaltiniai nurodo {rg} porcijai; tai tik orientacinis skaičius.',
  ans_rtd='Pagal {b} duomenis litre paruošto gerti arbatos gėrimo yra {rg} kofeino (apie {c} mg stikline po 250 ml).',
  ans_qual='{b} nurodo tik kokybinį kofeino lygį: „{q}“. Skaičių mg gamintojas neskelbia.',
  vs='Tai {pct}% vidutinio filtruotos kavos puodelio ({fil} mg).',
  h_tbl='Produktai ir kofeinas', th_prod='Produktas', th_type='Rūšis', th_cup='Kofeinas porcijoje', th_serv='Porcija', th_p100='mg / 100 ml', th_rel='Šaltinis',
  rel_high='Gamintojo puslapis', rel_medium='Gamintojo etiketė', rel_low='Orientacinis, neoficialus', per_l='mg / litrui', qual_lbl='Kokybinis lygis',
  h_faq='Dažni klausimai', q1='Kiek kofeino yra {b} arbatoje?', q2='Ar {b} arbatoje daugiau kofeino nei kavoje?', a2='Dažniausiai ne: puodelis arbatos paprastai turi mažiau kofeino nei puodelis filtruotos kavos (apie {fil} mg), bet skirtumas priklauso nuo produkto, kiekio ir plikymo laiko.',
  q3='Ar kofeino kiekis visada toks pats?', a3='Ne. Jis priklauso nuo partijos, lapų kiekio ir plikymo laiko, todėl pateikiame diapazonus. Tikslų skaičių gali patvirtinti tik gamintojas.',
  h_more='Taip pat naudinga', all_brands='Visos markės', note='Duomenys surinkti {d}. Receptūros keičiasi, todėl skaičius patikrink ir ant pakuotės. Bendra informacija, ne medicininė konsultacija.',
  h_src='Šaltiniai', src_note='Šaltiniai nurodyti prie kiekvieno produkto lentelėje.', open_src='šaltinis',
  home='Pagrindinis', h_limit='Dienos riba',
 ),
 'en': dict(
  hub='Tea brands', hub_h1='Caffeine in tea brands', hub_t='How much caffeine is in tea brands? Lipton, Bigelow, Twinings, Yogi',
  hub_desc='Caffeine in popular tea brands: manufacturer data with sources, ranges and a comparison with coffee.',
  hub_lead='Manufacturers rarely publish caffeine for specific teas, so we separate official data from rough estimates. Caffeine varies by batch and brewing.',
  th_brand='Brand', th_mg='Official data, mg', th_n='Products', none='no official mg', qual_only='qualitative level only',
  h_official='Brands with official data', h_other='Brands without official mg (rough estimates only)',
  h1='How much caffeine is in {b} tea?', t='How much caffeine is in {b} tea? {rg}', t_none='How much caffeine is in {b} tea?',
  d='{b}: caffeine in tea by source, {rg}. Table with serving size, mg per 100 ml and source links.', d_none='{b}: caffeine in tea. No official manufacturer data, so we show rough sources.',
  ans_off='According to {b}, a serving of tea contains {rg} of caffeine (depends on the product).', ans_low='We found no official {b} caffeine data. Unofficial sources give {rg} per serving; treat it as a rough figure only.',
  ans_rtd='According to {b}, one litre of its ready-to-drink tea contains {rg} of caffeine (about {c} mg per 250 ml glass).',
  ans_qual='{b} gives only a qualitative caffeine level: "{q}". The manufacturer does not publish mg.',
  vs='That is {pct}% of an average cup of filter coffee ({fil} mg).',
  h_tbl='Products and caffeine', th_prod='Product', th_type='Type', th_cup='Caffeine per serving', th_serv='Serving', th_p100='mg / 100 ml', th_rel='Source',
  rel_high='Manufacturer page', rel_medium='Manufacturer label', rel_low='Rough, unofficial', per_l='mg per litre', qual_lbl='Qualitative level',
  h_faq='Frequently asked questions', q1='How much caffeine is in {b} tea?', q2='Does {b} tea have more caffeine than coffee?', a2='Usually not: a cup of tea typically has less caffeine than a cup of filter coffee (about {fil} mg), but it depends on the product, amount and steeping time.',
  q3='Is the caffeine amount always the same?', a3='No. It depends on the batch, the amount of leaf and steeping time, which is why we show ranges. Only the manufacturer can confirm an exact figure.',
  h_more='Also useful', all_brands='All brands', note='Data collected {d}. Recipes change, so check the figure on the pack as well. General information, not medical advice.',
  h_src='Sources', src_note='Sources are linked next to each product in the table.', open_src='source',
  home='Home', h_limit='Daily limit',
 ),
 'it': dict(
  hub='Marche di tè', hub_h1='Caffeina nelle marche di tè', hub_t='Quanta caffeina c\'è nelle marche di tè? Lipton, Bigelow, Twinings, Yogi',
  hub_desc='Caffeina nelle marche di tè più diffuse: dati dei produttori con fonti, intervalli e confronto con il caffè.',
  hub_lead='I produttori raramente pubblicano la caffeina dei singoli tè, quindi separiamo i dati ufficiali dalle stime indicative. La caffeina varia con il lotto e l\'infusione.',
  th_brand='Marca', th_mg='Dati ufficiali, mg', th_n='Prodotti', none='nessun mg ufficiale', qual_only='solo livello qualitativo',
  h_official='Marche con dati ufficiali', h_other='Marche senza mg ufficiali (solo stime indicative)',
  h1='Quanta caffeina c\'è nel tè {b}?', t='Quanta caffeina c\'è nel tè {b}? {rg}', t_none='Quanta caffeina c\'è nel tè {b}?',
  d='{b}: caffeina nel tè secondo le fonti, {rg}. Tabella con porzione, mg per 100 ml e link alle fonti.', d_none='{b}: caffeina nel tè. Nessun dato ufficiale del produttore, mostriamo fonti indicative.',
  ans_off='Secondo {b}, una porzione di tè contiene {rg} di caffeina (dipende dal prodotto).', ans_low='Non abbiamo trovato dati ufficiali di {b}. Fonti non ufficiali indicano {rg} a porzione: è solo un valore indicativo.',
  ans_rtd='Secondo {b}, un litro di tè pronto da bere contiene {rg} di caffeina (circa {c} mg per bicchiere da 250 ml).',
  ans_qual='{b} indica solo un livello qualitativo di caffeina: «{q}». Il produttore non pubblica i mg.',
  vs='È il {pct}% di una tazza media di caffè filtro ({fil} mg).',
  h_tbl='Prodotti e caffeina', th_prod='Prodotto', th_type='Tipo', th_cup='Caffeina per porzione', th_serv='Porzione', th_p100='mg / 100 ml', th_rel='Fonte',
  rel_high='Pagina del produttore', rel_medium='Etichetta del produttore', rel_low='Indicativo, non ufficiale', per_l='mg al litro', qual_lbl='Livello qualitativo',
  h_faq='Domande frequenti', q1='Quanta caffeina c\'è nel tè {b}?', q2='Il tè {b} ha più caffeina del caffè?', a2='Di solito no: una tazza di tè ha in genere meno caffeina di una tazza di caffè filtro (circa {fil} mg), ma dipende dal prodotto, dalla quantità e dal tempo di infusione.',
  q3='La quantità di caffeina è sempre la stessa?', a3='No. Dipende dal lotto, dalla quantità di foglie e dal tempo di infusione, per questo mostriamo intervalli. Solo il produttore può confermare un valore preciso.',
  h_more='Può servire anche', all_brands='Tutte le marche', note='Dati raccolti il {d}. Le ricette cambiano, controlla il valore anche sulla confezione. Informazioni generali, non parere medico.',
  h_src='Fonti', src_note='Le fonti sono collegate accanto a ogni prodotto nella tabella.', open_src='fonte',
  home='Home', h_limit='Limite giornaliero',
 ),
}

SERV = {'lt': '{ml} ml', 'en': '{ml} ml', 'it': '{ml} ml'}


def key_b(slug): return 'br_' + slug


def has_mg(slug):
    return any(BD.official(r) for r in BD.for_brand(slug))


def indexable():
    return [s for s, _ in BD.BRANDS if has_mg(s)]


def register(B):
    B.PATH['hub_b'] = lambda l: f'/{l}/{DIR[l]}/'
    for s, _ in BD.BRANDS:
        B.PATH[key_b(s)] = (lambda s: lambda l: f'/{l}/{DIR[l]}/{s}/')(s)


def all_keys():
    return ['hub_b'] + [key_b(s) for s in indexable()]


def rng(rows, lang):
    rs = [r for r in rows if r['lo'] is not None]
    if any(r['avg'] for r in rs):
        rs = [r for r in rs if r['avg']]
    if not rs:
        return None
    if any(r['rtd'] for r in rs) and not all(r['rtd'] for r in rs):
        rs = [r for r in rs if not r['rtd']]
    lo, hi = min(r['lo'] for r in rs), max(r['hi'] for r in rs)
    unit = ' mg/l' if all(r['rtd'] for r in rs) else ' mg'
    return (f'{SG.num(lo, lang)}–{SG.num(hi, lang)}' if lo != hi else SG.num(lo, lang)) + unit


def cell_cup(r, lang, t):
    if r['lo'] is None:
        return f'{t["qual_lbl"]}: {BD.QUAL[r["brand"]][lang]}'
    base = f'{SG.num(r["lo"], lang)}–{SG.num(r["hi"], lang)}' if r['lo'] != r['hi'] else SG.num(r['lo'], lang)
    return base + (' mg/l' if r['rtd'] else ' mg')


def row_html(B, r, lang, t):
    E = B.E
    serv = '–' if not r['ml'] else (f'1 l' if r['rtd'] else f'{r["ml"]} ml')
    p100 = '–' if r['p100'] is None else SG.num(r['p100'], lang)
    return (f'<tr><th scope="row">{E(r["product"])}</th><td>{E(BD.TYPE[r["type"]][lang])}</td><td>{E(cell_cup(r, lang, t))}</td>'
            f'<td>{E(serv)}</td><td>{p100}</td>'
            f'<td><a href="{E(r["url"])}" target="_blank" rel="noopener nofollow">{E(t["rel_" + r["rel"]])}</a></td></tr>')


def brand_page(B, slug, lang):
    E = B.E
    t = T[lang]
    name = BD.brand_name(slug)
    rows = BD.for_brand(slug)
    off = [r for r in rows if BD.official(r)]
    low = [r for r in rows if r['rel'] == 'low']
    fil = [d for d in caff.drinks() if d['id'] == 'filter'][0]['typ']
    cupish = [r for r in off if not r['rtd'] and r['avg']]
    if off:
        rg = rng(off, lang)
        ans = t['ans_off'].format(b=name, rg=rg)
        if all(r['rtd'] for r in off):
            ans = t['ans_rtd'].format(b=name, rg=rg, c=SG.num(round(sum(r['avg'] for r in off) / len(off) / 4), lang))
        title = t['t'].format(b=name, rg=rg)
        desc = t['d'].format(b=name, rg=rg)
    elif low:
        rg = rng(low, lang)
        ans = t['ans_low'].format(b=name, rg=rg)
        title, desc = t['t_none'].format(b=name), t['d_none'].format(b=name)
    else:
        rg = ''
        ans = t['ans_qual'].format(b=name, q=BD.QUAL[slug][lang])
        title, desc = t['t_none'].format(b=name), t['d_none'].format(b=name)
    vs = ''
    if cupish:
        avg = sum(r['avg'] * (237 / r['ml']) for r in cupish) / len(cupish)
        vs = t['vs'].format(pct=round(avg / fil * 100), fil=fil)
    head = f'<tr><th>{E(t["th_prod"])}</th><th>{E(t["th_type"])}</th><th>{E(t["th_cup"])}</th><th>{E(t["th_serv"])}</th><th>{E(t["th_p100"])}</th><th>{E(t["th_rel"])}</th></tr>'
    body = ''.join(row_html(B, r, lang, t) for r in sorted(rows, key=lambda r: (r['rel'] == 'low', r['n'])))
    table = f'<div class="chart-card" style="margin-top:0"><table class="cmp"><thead>{head}</thead><tbody>{body}</tbody></table></div>'
    faqs = [(t['q1'].format(b=name), ans), (t['q2'].format(b=name), t['a2'].format(fil=fil)), (t['q3'], t['a3'])]
    key = key_b(slug)
    others = [s for s in indexable() if s != slug][:6]
    ol = ''.join(f'<a href="{B.PATH[key_b(s)](lang)}">{E(BD.brand_name(s))}</a>' for s in others)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <a href="{B.PATH['hub_b'](lang)}">{E(t['hub'])}</a> / <span>{E(name)}</span></div>
<h1 class="page-title">{E(t['h1'].format(b=name))}</h1>
<div class="answer"><p class="answer-main">{E(ans)}</p>{f'<p>{E(vs)}</p>' if vs else ''}</div>
<section class="seo-sec"><h2>{E(t['h_tbl'])}</h2>{table}</section>
{SG.faq_html(B, lang, faqs)}
<section class="seo-sec"><h2>{E(t['h_more'])}</h2><div class="quiet-links"><a href="{B.PATH['hub_b'](lang)}">{E(t['all_brands'])}</a>{ol}<a href="{B.PATH['g_limit'](lang)}">{E(t['h_limit'])}</a></div></section>
{SG.tools_links(B, lang)}
<section class="seo-sec"><h2>{E(t['h_src'])}</h2><p class="small">{E(t['src_note'])}</p><ul class="small srclist"><li><a href="{caff.SOURCES['efsa'][1]}" target="_blank" rel="noopener nofollow">{E(caff.SOURCES['efsa'][0])}</a></li></ul><p class="small">{E(t['note'].format(d=caff.CHECKED))}</p></section>
</main>
{jsonld(B, lang, key, name, faqs, t)}'''
    return B.shell(lang, key, title, desc, main, noindex=not off)


def jsonld(B, lang, key, name, faqs, t):
    crumbs = [(t['home'], B.BASE + B.PATH['home'](lang)), (t['hub'], B.BASE + B.PATH['hub_b'](lang))]
    if key != 'hub_b':
        crumbs.append((name, B.BASE + B.PATH[key](lang)))
    out = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]}]
    if faqs:
        out.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>' for o in out)


def hub_page(B, lang):
    E = B.E
    t = T[lang]
    trs_o, trs_x = '', ''
    for s, name in BD.BRANDS:
        rows = BD.for_brand(s)
        off = [r for r in rows if BD.official(r)]
        link = f'<a href="{B.PATH[key_b(s)](lang)}">{E(name)}</a>'
        if off:
            trs_o += f'<tr><th scope="row">{link}</th><td>{E(rng(off, lang))}</td><td>{len(rows)}</td></tr>'
        else:
            rg = rng(rows, lang) if any(r['lo'] is not None for r in rows) else t['qual_only']
            trs_x += f'<tr><th scope="row">{link}</th><td>{E(rg)}</td><td>{len(rows)}</td></tr>'
    th = f'<thead><tr><th>{E(t["th_brand"])}</th><th>{E(t["th_mg"])}</th><th>{E(t["th_n"])}</th></tr></thead>'
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <span>{E(t['hub'])}</span></div>
<h1 class="page-title">{E(t['hub_h1'])}</h1><p class="lead">{E(t['hub_lead'])}</p>
<section class="seo-sec"><h2>{E(t['h_official'])}</h2><div class="chart-card" style="margin-top:0"><table class="cmp">{th}<tbody>{trs_o}</tbody></table></div></section>
<section class="seo-sec"><h2>{E(t['h_other'])}</h2><div class="chart-card" style="margin-top:0"><table class="cmp">{th.replace(t['th_mg'], t['th_mg'].replace(t['th_mg'], {'lt': 'Orientaciniai duomenys, mg', 'en': 'Rough data, mg', 'it': 'Dati indicativi, mg'}[lang]))}<tbody>{trs_x}</tbody></table></div></section>
<section class="seo-sec"><div class="quiet-links"><a href="{B.PATH['hub_d'](lang)}">{E(SG.L[lang]['hub_d'])}</a><a href="{B.PATH['g_limit'](lang)}">{E(t['h_limit'])}</a></div></section>
{SG.tools_links(B, lang)}
<section class="seo-sec"><p class="small">{E(t['note'].format(d=caff.CHECKED))}</p></section>
</main>
{jsonld(B, lang, 'hub_b', t['hub'], [], t)}'''
    return B.shell(lang, 'hub_b', t['hub_t'], t['hub_desc'], main)


def pages(B):
    register(B)
    out = []
    for lang in B.LANGS:
        out.append((B.PATH['hub_b'](lang) + 'index.html', hub_page(B, lang)))
        for s, _ in BD.BRANDS:
            out.append((B.PATH[key_b(s)](lang) + 'index.html', brand_page(B, s, lang)))
    return out
