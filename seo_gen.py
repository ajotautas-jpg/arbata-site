"""Automatiniai SEO puslapiai iš caff.py duomenų: „kiek kofeino yra X“, „A vs B“, lentelė, dienos ribos gidas.
Visi skaičiai skaičiuojami iš duomenų bazės, tekstai LT/EN/IT. Generuoja build.py (žr. pages())."""
import json
import caff

DIR = {
    'drinks': {'lt': 'kofeinas', 'en': 'caffeine', 'it': 'caffeina'},
    'cmp': {'lt': 'palyginimas', 'en': 'compare', 'it': 'confronto'},
    'guides': {'lt': 'gidai', 'en': 'guides', 'it': 'guide'},
}
GUIDE_SLUG = {'lt': 'kofeino-riba-per-diena', 'en': 'daily-caffeine-limit', 'it': 'limite-giornaliero-caffeina'}

# id: (slug lt/en/it), nom (vardininkas), 'in' (kur: „kiek kofeino yra ...“)
N = {
 'black': {'slug': {'lt': 'juodoji-arbata', 'en': 'black-tea', 'it': 'te-nero'},
           'nom': {'lt': 'Juodoji arbata', 'en': 'Black tea', 'it': 'Tè nero'},
           'in': {'lt': 'juodojoje arbatoje', 'en': 'black tea', 'it': 'nel tè nero'}},
 'green': {'slug': {'lt': 'zalioji-arbata', 'en': 'green-tea', 'it': 'te-verde'},
           'nom': {'lt': 'Žalioji arbata', 'en': 'Green tea', 'it': 'Tè verde'},
           'in': {'lt': 'žaliojoje arbatoje', 'en': 'green tea', 'it': 'nel tè verde'}},
 'oolong': {'slug': {'lt': 'oolong', 'en': 'oolong-tea', 'it': 'oolong'},
            'nom': {'lt': 'Oolong arbata', 'en': 'Oolong tea', 'it': 'Oolong'},
            'in': {'lt': 'oolong arbatoje', 'en': 'oolong tea', 'it': "nell'oolong"}},
 'white': {'slug': {'lt': 'baltoji-arbata', 'en': 'white-tea', 'it': 'te-bianco'},
           'nom': {'lt': 'Baltoji arbata', 'en': 'White tea', 'it': 'Tè bianco'},
           'in': {'lt': 'baltojoje arbatoje', 'en': 'white tea', 'it': 'nel tè bianco'}},
 'puerh': {'slug': {'lt': 'pu-erh', 'en': 'pu-erh-tea', 'it': 'pu-erh'},
           'nom': {'lt': 'Pu-erh arbata', 'en': 'Pu-erh tea', 'it': 'Pu-erh'},
           'in': {'lt': 'pu-erh arbatoje', 'en': 'pu-erh tea', 'it': 'nel pu-erh'}},
 'mate': {'slug': {'lt': 'yerba-mate', 'en': 'yerba-mate', 'it': 'yerba-mate'},
          'nom': {'lt': 'Yerba mate', 'en': 'Yerba mate', 'it': 'Yerba mate'},
          'in': {'lt': 'yerba mate', 'en': 'yerba mate', 'it': 'nello yerba mate'}},
 'matcha': {'slug': {'lt': 'matcha', 'en': 'matcha', 'it': 'matcha'},
            'nom': {'lt': 'Matcha', 'en': 'Matcha', 'it': 'Matcha'},
            'in': {'lt': 'matcha arbatoje', 'en': 'matcha', 'it': 'nel matcha'}},
 'espresso': {'slug': {'lt': 'espresas', 'en': 'espresso', 'it': 'espresso'},
              'nom': {'lt': 'Espresas', 'en': 'Espresso', 'it': 'Espresso'},
              'in': {'lt': 'espresse', 'en': 'espresso', 'it': "nell'espresso"}},
 'filter': {'slug': {'lt': 'filtrine-kava', 'en': 'filter-coffee', 'it': 'caffe-filtro'},
            'nom': {'lt': 'Filtrinė kava', 'en': 'Filter coffee', 'it': 'Caffè filtro'},
            'in': {'lt': 'filtrinėje kavoje', 'en': 'filter coffee', 'it': 'nel caffè filtro'}},
 'decaf': {'slug': {'lt': 'kava-be-kofeino', 'en': 'decaf-coffee', 'it': 'caffe-decaffeinato'},
           'nom': {'lt': 'Kava be kofeino', 'en': 'Decaf coffee', 'it': 'Caffè decaffeinato'},
           'in': {'lt': 'kavoje be kofeino', 'en': 'decaf coffee', 'it': 'nel caffè decaffeinato'}},
 'cola': {'slug': {'lt': 'kola', 'en': 'cola', 'it': 'cola'},
          'nom': {'lt': 'Kola', 'en': 'Cola', 'it': 'Cola'},
          'in': {'lt': 'kolos gėrime', 'en': 'cola', 'it': 'nella cola'}},
 'energy': {'slug': {'lt': 'energinis-gerimas', 'en': 'energy-drink', 'it': 'energy-drink'},
            'nom': {'lt': 'Energinis gėrimas', 'en': 'Energy drink', 'it': 'Energy drink'},
            'in': {'lt': 'energiniame gėrime', 'en': 'an energy drink', 'it': "nell'energy drink"}},
 'shot': {'slug': {'lt': 'energinis-sotas', 'en': 'energy-shot', 'it': 'energy-shot'},
          'nom': {'lt': 'Energinis šotas', 'en': 'Energy shot', 'it': 'Energy shot'},
          'in': {'lt': 'energiniame šote', 'en': 'an energy shot', 'it': "nell'energy shot"}},
}

PAIRS = (
    [('filter', x) for x in ('black', 'green', 'oolong', 'white', 'puerh', 'mate', 'matcha', 'espresso', 'decaf', 'cola', 'energy')]
    + [('espresso', x) for x in ('black', 'green', 'matcha', 'mate', 'energy')]
    + [('black', x) for x in ('green', 'oolong', 'puerh', 'mate', 'matcha', 'white', 'cola')]
    + [('green', x) for x in ('matcha', 'oolong', 'white')]
    + [('matcha', 'mate'), ('mate', 'puerh')]
)

# ---------- tekstai ----------
L = {
 'lt': dict(
  home='Pagrindinis', hub_d='Kofeino kiekis gėrimuose', hub_c='Gėrimų palyginimai', guides='Gidai',
  q_in='Kiek kofeino yra {inn}?', t_drink='Kiek kofeino yra {inn}? {lo}–{hi} mg puodelyje',
  d_desc='{nom}: {lo}–{hi} mg kofeino puodelyje ({ml} ml), apie {p100} mg / 100 ml. Palyginimas su kava, dienos riba ir šaltiniai.',
  ans='{nom} ({ml} ml) paprastai turi {lo}–{hi} mg kofeino, vidutiniškai apie {typ} mg.',
  ans_same='{nom} ({ml} ml) turi apie {typ} mg kofeino.',
  basis_tea='Skaičiuota {g} g sauso lapo, {ml} ml vandens, apie 5 min. plikymas.', basis_whole='Skaičiuota {g} g miltelių, {ml} ml vandens (suvartojamas visas lapas).', basis_other='Standartinė porcija: {ml} ml.',
  h_facts='Svarbiausi skaičiai', r_cup='Kofeinas puodelyje', r_vol='Tūris', r_p100='mg / 100 ml (vidutiniškai)', r_vsf='Palyginti su filtrine kava (puodelis)', r_c400='Puodelių iki 400 mg per dieną (suaugusiam)', r_c200='Puodelių vienu metu iki 200 mg',
  c_many='daugiau nei 20', h_brew='Kaip kofeinas kinta plikant', brew_note='Ilgesnis plikymas dažniausiai atneša daugiau kofeino. Skaičiai: {g} g arbatos.', b_time='Plikymo laikas', b_min='min.',
  h_gr='Kiek priklauso nuo gramų', gr_note='Matcha suvartojamas visas lapas, todėl svarbiausia – kiek gramų naudoji.', gr_g='Gramai',
  h_eve='O vakare?', eve='Po 6 valandų organizme lieka maždaug {lo}–{hi} mg kofeino (pusėjimo trukmė 3–7 val.). Jautrumas skiriasi, todėl tai orientyras, ne taisyklė.',
  h_faq='Dažni klausimai', h_more='Išbandyk', h_src='Šaltiniai ir metodika', src_note='Duomenys patikrinti {d}. Rodomi diapazonai, nes tyrimai pateikia skirtingus skaičius. Bendra informacija, ne medicininė konsultacija.', low_conf='Šio gėrimo duomenų šaltinių mažai, todėl diapazonas platesnis.',
  f1q='Ar {nom_l} turi daugiau kofeino nei filtrinė kava?', f1_more='Ne, vidutiniškai mažiau: apie {pct}% filtrinės kavos puodelio kofeino kiekio.', f1_less='Taip, vidutiniškai daugiau: apie {pct}% filtrinės kavos puodelio kofeino kiekio.', f1_same='Panašiai, apie {pct}% filtrinės kavos puodelio kofeino kiekio.',
  f2q='Kiek puodelių „{nom}“ galima išgerti per dieną?', f2a='Suaugusiam EFSA nurodo iki 400 mg kofeino per dieną iš visų šaltinių. Vien iš šio gėrimo tai maždaug {c} puodelių, jei jo nepildo kiti šaltiniai. Nėštumo metu riba – 200 mg per dieną.',
  f3q='Kaip „{nom}“ palyginti su kitomis arbatomis ir kava?', f3a='Žiūrėk lentelę „Kofeino kiekis gėrimuose“: ten visi gėrimai surikiuoti pagal kofeino kiekį puodelyje.',
  tools_calc='Kofeino skaičiuoklė', tools_cmp='Palyginti du gėrimus', tools_track='Dienos sekiklis', tools_conv='Kava → arbata keitiklis',
  # compare
  t_cmp='{a} ar {b}: kuriame daugiau kofeino?', c_desc='{a}: {alo}–{ahi} mg, {b}: {blo}–{bhi} mg puodelyje. Kuris turi daugiau kofeino, kiek puodelių atitinka ir kada tinka.',
  c_h1='{a} ar {b}: kuriame daugiau kofeino?', v_more='{x} puodelyje vidutiniškai turi apie {r}× daugiau kofeino nei {y}.', v_same='{a} ir {b} puodelyje turi panašų kofeino kiekį (skirtumas mažesnis nei 20%).',
  v_overlap='Diapazonai persidengia, todėl konkrečiame puodelyje skirtumas gali būti ir priešingas.',
  v_p100='Pagal 100 ml: {x} turi apie {r}× daugiau kofeino nei {y}.', v_p100_same='Pagal 100 ml kofeino kiekis panašus.',
  th_drink='Gėrimas', c_f1q='Kuris turi daugiau kofeino: {a} ar {b}?', c_f2q='Kiek puodelių „{b_g}“ atitinka vieną puodelį „{a_g}“?', c_f2a='Pagal vidutines vertes vieną puodelį „{a_n}“ ({atyp} mg) atitinka apie {n} puodelio „{b_n}“ ({btyp} mg). Tai orientyras, nes abu gėrimai kinta pagal partiją ir ruošimą.',
  c_f3q='Kuris geriau tinka vakare?', c_f3a='Mažiau kofeino puodelyje turi {x} (apie {xt} mg, o {y} – apie {yt} mg). Po 6 valandų organizme lieka apie pusė–trečdalis išgerto kiekio, bet jautrumas labai skiriasi.',
  c_open='Atidaryti interaktyvų palyginimą', c_page='Kofeinas: {n}',
  # hubs
  hub_d_h1='Kofeino kiekis gėrimuose', hub_d_t='Kofeino kiekis gėrimuose: arbata, kava, kola, energiniai (lentelė)', hub_d_desc='Lentelė: kiek kofeino yra arbatoje, kavoje, kolos ir energiniuose gėrimuose puodelyje ir 100 ml. Diapazonai su šaltiniais.', hub_d_lead='Visi gėrimai vienoje lentelėje, nuo daugiausia iki mažiausiai kofeino puodelyje.',
  hub_c_h1='Gėrimų palyginimai', hub_c_t='Kofeino palyginimai: arbata, kava ir kiti gėrimai', hub_c_desc='Kuris gėrimas turi daugiau kofeino? Palyginimai pagal puodelį ir 100 ml su diapazonais ir šaltiniais.', hub_c_lead='Pasirink porą ir pamatyk, kuris turi daugiau kofeino ir kiek puodelių atitinka vieną kitą.',
  th_cup='mg puodelyje', th_ml='ml', th_p100='mg / 100 ml',
  # guide
  g_t='Kiek kofeino per dieną saugu? EFSA ribos ir kiek tai puodelių', g_desc='EFSA ribos: 400 mg per dieną suaugusiam, 200 mg vienu metu ir nėštumo metu. Kiek tai puodelių arbatos, kavos ar kitų gėrimų.', g_h1='Kiek kofeino per dieną saugu?',
  g_lead='Europos maisto saugos tarnyba (EFSA) 2015 m. įvertino kofeino saugumą. Čia jos ribos ir kiek tai puodelių.',
  g_h_lim='EFSA ribos', g_lims=['Suaugusiems: iki 400 mg per dieną iš visų šaltinių.', 'Vienu metu: iki 200 mg.', 'Nėštumo ir žindymo metu: iki 200 mg per dieną.', 'Vaikams ir paaugliams: apie 3 mg kilogramui kūno svorio per dieną (pavyzdžiui, 40 kg vaikui apie 120 mg).'],
  g_h_cups='Kiek tai puodelių', g_cups_note='Lentelė rodo, kiek puodelių vidutiniškai pasiektų 400 mg ir 200 mg.', g_c400='Iki 400 mg', g_c200='Iki 200 mg',
  g_h_half='Kiek laiko kofeinas lieka organizme', g_half='Kofeino pusėjimo trukmė dažniausiai 3–7 valandos (skaičiuojame apie 5), todėl popietinis puodelis dar veikia vakare. Rūkymas, vaistai, nėštumas ir genetika šį laiką keičia.',
  g_note='Tai bendra informacija, ne medicininė konsultacija. Jei esi nėščia, vartoji vaistus ar turi sveikatos būklių, pasitark su gydytoju.',
 ),
 'en': dict(
  home='Home', hub_d='Caffeine in drinks', hub_c='Drink comparisons', guides='Guides',
  q_in='How much caffeine is in {inn}?', t_drink='How much caffeine is in {inn}? {lo}–{hi} mg per cup',
  d_desc='{nom}: {lo}–{hi} mg caffeine per cup ({ml} ml), about {p100} mg per 100 ml. Comparison with coffee, daily limit and sources.',
  ans='{nom} ({ml} ml) usually contains {lo}–{hi} mg of caffeine, about {typ} mg on average.',
  ans_same='{nom} ({ml} ml) contains about {typ} mg of caffeine.',
  basis_tea='Based on {g} g of dry leaf, {ml} ml of water, about 5 min of steeping.', basis_whole='Based on {g} g of powder, {ml} ml of water (the whole leaf is consumed).', basis_other='Standard serving: {ml} ml.',
  h_facts='Key numbers', r_cup='Caffeine per cup', r_vol='Volume', r_p100='mg / 100 ml (average)', r_vsf='Compared with filter coffee (per cup)', r_c400='Cups to reach 400 mg a day (adult)', r_c200='Cups to reach 200 mg at once',
  c_many='more than 20', h_brew='How caffeine changes with steeping', brew_note='Longer steeping usually brings more caffeine. Figures for {g} g of tea.', b_time='Steeping time', b_min='min',
  h_gr='How much depends on grams', gr_note='With matcha you consume the whole leaf, so the number of grams matters most.', gr_g='Grams',
  h_eve='What about the evening?', eve='After 6 hours roughly {lo}–{hi} mg of caffeine is still in the body (half-life 3–7 h). Sensitivity varies, so treat this as a guide, not a rule.',
  h_faq='Frequently asked questions', h_more='Try it', h_src='Sources and method', src_note='Data checked {d}. Ranges are shown because studies report different numbers. General information, not medical advice.', low_conf='Few sources exist for this drink, so the range is wider.',
  f1q='Does {nom_l} have more caffeine than filter coffee?', f1_more='No, on average less: about {pct}% of the caffeine in a cup of filter coffee.', f1_less='Yes, on average more: about {pct}% of the caffeine in a cup of filter coffee.', f1_same='About the same: around {pct}% of the caffeine in a cup of filter coffee.',
  f2q='How many cups of {nom_l} can I drink a day?', f2a='For adults EFSA gives up to 400 mg of caffeine a day from all sources. From this drink alone that is roughly {c} cups, if nothing else adds caffeine. In pregnancy the limit is 200 mg a day.',
  f3q='How does {nom_l} compare with other teas and coffee?', f3a='See the "Caffeine in drinks" table: every drink is listed by caffeine per cup.',
  tools_calc='Caffeine calculator', tools_cmp='Compare two drinks', tools_track='Daily tracker', tools_conv='Coffee → tea converter',
  t_cmp='{a} vs {b}: which has more caffeine?', c_desc='{a}: {alo}–{ahi} mg, {b}: {blo}–{bhi} mg per cup. Which has more caffeine, how many cups equal one, and when each fits.',
  c_h1='{a} vs {b}: which has more caffeine?', v_more='A cup of {x} has on average about {r}× more caffeine than {y}.', v_same='{a} and {b} have similar caffeine per cup (a difference of under 20%).',
  v_overlap='The ranges overlap, so in a particular cup the difference can go the other way.',
  v_p100='Per 100 ml: {x} has about {r}× more caffeine than {y}.', v_p100_same='Per 100 ml the caffeine is similar.',
  th_drink='Drink', c_f1q='Which has more caffeine: {a} or {b}?', c_f2q='How many cups of {b_g} equal one cup of {a_g}?', c_f2a='Using average values, one cup of {a_n} ({atyp} mg) equals about {n} cups of {b_n} ({btyp} mg). This is a guide, since both drinks vary by batch and preparation.',
  c_f3q='Which is better in the evening?', c_f3a='{x} has less caffeine per cup (about {xt} mg versus about {yt} mg for {y}). After 6 hours roughly half to a third of what you drank remains, but sensitivity varies a lot.',
  c_open='Open the interactive comparison', c_page='Caffeine: {n}',
  hub_d_h1='Caffeine in drinks', hub_d_t='Caffeine in drinks: tea, coffee, cola, energy drinks (table)', hub_d_desc='A table of caffeine in tea, coffee, cola and energy drinks per cup and per 100 ml. Ranges with sources.', hub_d_lead='Every drink in one table, from most to least caffeine per cup.',
  hub_c_h1='Drink comparisons', hub_c_t='Caffeine comparisons: tea, coffee and other drinks', hub_c_desc='Which drink has more caffeine? Comparisons per cup and per 100 ml, with ranges and sources.', hub_c_lead='Pick a pair to see which has more caffeine and how many cups equal one another.',
  th_cup='mg per cup', th_ml='ml', th_p100='mg / 100 ml',
  g_t='How much caffeine a day is safe? EFSA limits in cups', g_desc='EFSA limits: 400 mg a day for adults, 200 mg at once and in pregnancy. What that means in cups of tea, coffee and other drinks.', g_h1='How much caffeine a day is safe?',
  g_lead='The European Food Safety Authority (EFSA) assessed caffeine safety in 2015. Here are its limits and what they mean in cups.',
  g_h_lim='EFSA limits', g_lims=['Adults: up to 400 mg a day from all sources.', 'At one time: up to 200 mg.', 'Pregnancy and breastfeeding: up to 200 mg a day.', 'Children and teenagers: about 3 mg per kilogram of body weight a day (for example about 120 mg for a 40 kg child).'],
  g_h_cups='What that is in cups', g_cups_note='The table shows how many cups on average reach 400 mg and 200 mg.', g_c400='Up to 400 mg', g_c200='Up to 200 mg',
  g_h_half='How long caffeine stays in the body', g_half='The half-life of caffeine is usually 3–7 hours (we use about 5), so an afternoon cup can still act in the evening. Smoking, medication, pregnancy and genetics change this.',
  g_note='General information, not medical advice. If you are pregnant, take medication or have a health condition, talk to your doctor.',
 ),
 'it': dict(
  home='Home', hub_d='Caffeina nelle bevande', hub_c='Confronti tra bevande', guides='Guide',
  q_in='Quanta caffeina c\'è {inn}?', t_drink='Quanta caffeina c\'è {inn}? {lo}–{hi} mg a tazza',
  d_desc='{nom}: {lo}–{hi} mg di caffeina a tazza ({ml} ml), circa {p100} mg ogni 100 ml. Confronto con il caffè, limite giornaliero e fonti.',
  ans='{nom} ({ml} ml) contiene di solito {lo}–{hi} mg di caffeina, in media circa {typ} mg.',
  ans_same='{nom} ({ml} ml) contiene circa {typ} mg di caffeina.',
  basis_tea='Calcolato su {g} g di foglie secche, {ml} ml di acqua, circa 5 min di infusione.', basis_whole='Calcolato su {g} g di polvere, {ml} ml di acqua (si consuma tutta la foglia).', basis_other='Porzione standard: {ml} ml.',
  h_facts='I numeri principali', r_cup='Caffeina per tazza', r_vol='Volume', r_p100='mg / 100 ml (media)', r_vsf='Rispetto al caffè filtro (a tazza)', r_c400='Tazze per arrivare a 400 mg al giorno (adulto)', r_c200='Tazze per arrivare a 200 mg in una volta',
  c_many='più di 20', h_brew='Come cambia la caffeina con l\'infusione', brew_note='Un\'infusione più lunga di solito porta più caffeina. Valori per {g} g di tè.', b_time='Tempo di infusione', b_min='min',
  h_gr='Quanto dipende dai grammi', gr_note='Con il matcha si consuma tutta la foglia, quindi contano soprattutto i grammi.', gr_g='Grammi',
  h_eve='E la sera?', eve='Dopo 6 ore nel corpo restano circa {lo}–{hi} mg di caffeina (emivita 3–7 h). La sensibilità varia, quindi è un\'indicazione, non una regola.',
  h_faq='Domande frequenti', h_more='Provalo', h_src='Fonti e metodo', src_note='Dati verificati il {d}. Mostriamo intervalli perché gli studi riportano valori diversi. Informazioni generali, non parere medico.', low_conf='Per questa bevanda ci sono poche fonti, quindi l\'intervallo è più ampio.',
  f1q='{nom} ha più caffeina del caffè filtro?', f1_more='No, in media meno: circa il {pct}% della caffeina di una tazza di caffè filtro.', f1_less='Sì, in media di più: circa il {pct}% della caffeina di una tazza di caffè filtro.', f1_same='Più o meno uguale: circa il {pct}% della caffeina di una tazza di caffè filtro.',
  f2q='Quante tazze di {nom_l} si possono bere al giorno?', f2a='Per gli adulti l\'EFSA indica fino a 400 mg di caffeina al giorno da tutte le fonti. Solo da questa bevanda sono circa {c} tazze, se nient\'altro aggiunge caffeina. In gravidanza il limite è 200 mg al giorno.',
  f3q='Come si colloca {nom_l} rispetto ad altri tè e al caffè?', f3a='Guarda la tabella «Caffeina nelle bevande»: tutte le bevande sono ordinate per caffeina a tazza.',
  tools_calc='Calcolatore di caffeina', tools_cmp='Confronta due bevande', tools_track='Diario giornaliero', tools_conv='Convertitore caffè → tè',
  t_cmp='{a} o {b}: quale ha più caffeina?', c_desc='{a}: {alo}–{ahi} mg, {b}: {blo}–{bhi} mg a tazza. Quale ha più caffeina, quante tazze ne valgono una e quando scegliere ciascuna.',
  c_h1='{a} o {b}: quale ha più caffeina?', v_more='Una tazza di {x} ha in media circa {r}× più caffeina di {y}.', v_same='{a} e {b} hanno una caffeina simile a tazza (differenza inferiore al 20%).',
  v_overlap='Gli intervalli si sovrappongono, quindi in una tazza specifica la differenza può essere opposta.',
  v_p100='Ogni 100 ml: {x} ha circa {r}× più caffeina di {y}.', v_p100_same='Ogni 100 ml la caffeina è simile.',
  th_drink='Bevanda', c_f1q='Quale ha più caffeina: {a} o {b}?', c_f2q='Quante tazze di {b_g} valgono una tazza di {a_g}?', c_f2a='Con i valori medi, una tazza di {a_n} ({atyp} mg) vale circa {n} tazze di {b_n} ({btyp} mg). È un\'indicazione, perché entrambe variano per lotto e preparazione.',
  c_f3q='Quale è meglio la sera?', c_f3a='{x} ha meno caffeina a tazza (circa {xt} mg contro circa {yt} mg di {y}). Dopo 6 ore resta circa da metà a un terzo di quanto bevuto, ma la sensibilità varia molto.',
  c_open='Apri il confronto interattivo', c_page='Caffeina: {n}',
  hub_d_h1='Caffeina nelle bevande', hub_d_t='Caffeina nelle bevande: tè, caffè, cola, energy drink (tabella)', hub_d_desc='Tabella della caffeina in tè, caffè, cola ed energy drink a tazza e ogni 100 ml. Intervalli con fonti.', hub_d_lead='Tutte le bevande in una tabella, dalla più alla meno ricca di caffeina a tazza.',
  hub_c_h1='Confronti tra bevande', hub_c_t='Confronti sulla caffeina: tè, caffè e altre bevande', hub_c_desc='Quale bevanda ha più caffeina? Confronti a tazza e ogni 100 ml, con intervalli e fonti.', hub_c_lead='Scegli una coppia e vedi quale ha più caffeina e quante tazze ne valgono un\'altra.',
  th_cup='mg a tazza', th_ml='ml', th_p100='mg / 100 ml',
  g_t='Quanta caffeina al giorno è sicura? I limiti EFSA in tazze', g_desc='Limiti EFSA: 400 mg al giorno per gli adulti, 200 mg in una volta e in gravidanza. Cosa significano in tazze di tè, caffè e altre bevande.', g_h1='Quanta caffeina al giorno è sicura?',
  g_lead='L\'Autorità europea per la sicurezza alimentare (EFSA) ha valutato la sicurezza della caffeina nel 2015. Ecco i suoi limiti e cosa significano in tazze.',
  g_h_lim='I limiti EFSA', g_lims=['Adulti: fino a 400 mg al giorno da tutte le fonti.', 'In una volta: fino a 200 mg.', 'Gravidanza e allattamento: fino a 200 mg al giorno.', 'Bambini e adolescenti: circa 3 mg per chilo di peso al giorno (ad esempio circa 120 mg per un bambino di 40 kg).'],
  g_h_cups='Quante tazze sono', g_cups_note='La tabella mostra quante tazze in media arrivano a 400 mg e a 200 mg.', g_c400='Fino a 400 mg', g_c200='Fino a 200 mg',
  g_h_half='Quanto resta la caffeina nel corpo', g_half='L\'emivita della caffeina è di solito 3–7 ore (usiamo circa 5), quindi una tazza del pomeriggio può agire ancora la sera. Fumo, farmaci, gravidanza e genetica cambiano questo tempo.',
  g_note='Informazioni generali, non parere medico. In gravidanza, se prendi farmaci o hai problemi di salute, parla con il medico.',
 ),
}


def num(x, lang, d=1):
    if abs(x - round(x)) < 1e-9 and d:
        s = str(int(round(x)))
    else:
        s = str(round(x, d))
    return s if lang == 'en' else s.replace('.', ',')


def key_d(i): return 'd_' + i
def key_c(a, b): return f'c_{a}_{b}'


def register(B):
    for lang in B.LANGS:
        pass
    for i in N:
        B.PATH[key_d(i)] = (lambda i: lambda l: f'/{l}/{DIR["drinks"][l]}/{N[i]["slug"][l]}/')(i)
    for a, b in PAIRS:
        B.PATH[key_c(a, b)] = (lambda a, b: lambda l: f'/{l}/{DIR["cmp"][l]}/{N[a]["slug"][l]}-vs-{N[b]["slug"][l]}/')(a, b)
    B.PATH['hub_d'] = lambda l: f'/{l}/{DIR["drinks"][l]}/'
    B.PATH['hub_c'] = lambda l: f'/{l}/{DIR["cmp"][l]}/'
    B.PATH['g_limit'] = lambda l: f'/{l}/{DIR["guides"][l]}/{GUIDE_SLUG[l]}/'


def all_keys():
    return ['hub_d', 'hub_c', 'g_limit'] + [key_d(i) for i in N] + [key_c(a, b) for a, b in PAIRS]


def drink_map():
    return {d['id']: d for d in caff.drinks()}


def jsonld(B, lang, key, name, faqs):
    crumbs = [(L[lang]['home'], B.BASE + B.PATH['home'](lang))]
    if key.startswith('d_') or key == 'hub_d':
        crumbs.append((L[lang]['hub_d'], B.BASE + B.PATH['hub_d'](lang)))
    elif key.startswith('c_') or key == 'hub_c':
        crumbs.append((L[lang]['hub_c'], B.BASE + B.PATH['hub_c'](lang)))
    crumbs.append((name, B.BASE + B.PATH[key](lang)))
    bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]}
    out = [bc]
    if faqs:
        out.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>' for o in out)


def crumbs_html(B, lang, key, name):
    E = B.E
    parts = [f'<a href="{B.PATH["home"](lang)}">{E(L[lang]["home"])}</a>']
    if key.startswith('d_'):
        parts.append(f'<a href="{B.PATH["hub_d"](lang)}">{E(L[lang]["hub_d"])}</a>')
    elif key.startswith('c_'):
        parts.append(f'<a href="{B.PATH["hub_c"](lang)}">{E(L[lang]["hub_c"])}</a>')
    parts.append(f'<span>{E(name)}</span>')
    return '<div class="crumbs">' + ' / '.join(parts) + '</div>'


def faq_html(B, lang, faqs):
    E = B.E
    return f'<section class="seo-sec"><h2>{E(L[lang]["h_faq"])}</h2>' + ''.join(
        f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs) + '</section>'


def src_html(B, lang, srcs):
    E = B.E
    t = L[lang]
    items = ''.join(f'<li><a href="{caff.SOURCES[k][1]}" target="_blank" rel="noopener nofollow">{E(caff.SOURCES[k][0])}</a></li>' for k in srcs)
    return f'<section class="seo-sec"><h2>{E(t["h_src"])}</h2><ul class="small srclist">{items}</ul><p class="small">{E(t["src_note"].format(d=caff.CHECKED))}</p></section>'


def tools_links(B, lang, a=None, b=None):
    E = B.E
    t = L[lang]
    cmp_url = B.PATH['compare'](lang) + (f'?a={a}&b={b}' if a and b else '')
    links = [(B.PATH['calc'](lang), t['tools_calc']), (cmp_url, t['tools_cmp']), (B.PATH['tracker'](lang), t['tools_track']), (B.PATH['convert'](lang), t['tools_conv'])]
    links.append((B.PATH['hub_t'](lang), __import__('tealib_gen').T[lang]['hub']))
    return f'<section class="seo-sec"><h2>{E(t["h_more"])}</h2><div class="quiet-links">' + ''.join(f'<a href="{u}">{E(n)}</a>' for u, n in links) + '</div></section>'


def cups_to(limit, d):
    c = limit / max(d['typ'], 1)
    return c


def cups_txt(limit, d, lang):
    c = int(limit // max(d['typ'], 1))
    return L[lang]['c_many'] if c > 20 else str(max(c, 0))


def drink_page(B, i, lang):
    E = B.E
    t = L[lang]
    D = drink_map()
    d = D[i]
    fil = D['filter']['typ']
    nom = N[i]['nom'][lang]
    inn = N[i]['in'][lang]
    nom_l = nom[0].lower() + nom[1:]
    p100 = num(round(d['typ'] / d['ml'] * 100, 1), lang)
    pct = round(d['typ'] / fil * 100)
    same = d['lo'] == d['hi']
    ans = (t['ans_same'] if same else t['ans']).format(nom=nom, ml=d['ml'], lo=d['lo'], hi=d['hi'], typ=d['typ'])
    if d['group'] == 'tea':
        basis = (t['basis_whole'] if d.get('whole') else t['basis_tea']).format(g=d['g'], ml=d['ml'])
    else:
        basis = t['basis_other'].format(ml=d['ml'])
    title = t['t_drink'].format(inn=inn, lo=d['lo'], hi=d['hi']) if not same else t['q_in'].format(inn=inn)
    desc = t['d_desc'].format(nom=nom, lo=d['lo'], hi=d['hi'], ml=d['ml'], p100=p100) if not same else f'{nom}: ~{d["typ"]} mg / {d["ml"]} ml.'
    c400, c200 = cups_txt(400, d, lang), cups_txt(200, d, lang)
    rg = f'{d["lo"]}–{d["hi"]} mg' if not same else f'{d["typ"]} mg'
    rows = [(t['r_cup'], rg), (t['r_vol'], f'{d["ml"]} ml'), (t['r_p100'], p100), (t['r_vsf'], f'{pct}%'), (t['r_c400'], c400), (t['r_c200'], c200)]
    table = '<table class="cmp"><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in rows) + '</tbody></table>'
    extra = ''
    if d['group'] == 'tea' and not d.get('whole'):
        pg = d['perg']
        trs = ''.join(f'<tr><th scope="row">{m} {E(t["b_min"])}</th><td>{round(pg[0] * d["g"] * caff.TIME_F[m])}–{round(pg[1] * d["g"] * caff.TIME_F[m])} mg</td></tr>' for m in (2, 3, 4, 5))
        extra = f'<section class="seo-sec"><h2>{E(t["h_brew"])}</h2><p>{E(t["brew_note"].format(g=d["g"]))}</p><table class="cmp"><thead><tr><th>{E(t["b_time"])}</th><th>{E(t["r_cup"])}</th></tr></thead><tbody>{trs}</tbody></table></section>'
    elif d.get('whole'):
        pg = d['perg']
        trs = ''.join(f'<tr><th scope="row">{g} g</th><td>{round(pg[0] * g)}–{round(pg[1] * g)} mg</td></tr>' for g in (1, 2, 3))
        extra = f'<section class="seo-sec"><h2>{E(t["h_gr"])}</h2><p>{E(t["gr_note"])}</p><table class="cmp"><thead><tr><th>{E(t["gr_g"])}</th><th>{E(t["r_cup"])}</th></tr></thead><tbody>{trs}</tbody></table></section>'
    eve = ''
    if d['typ'] >= 10:
        eve = f'<section class="seo-sec"><h2>{E(t["h_eve"])}</h2><p>{E(t["eve"].format(lo=round(d["lo"] * 0.25), hi=round(d["hi"] * 0.55)))}</p></section>'
    f1 = t['f1_more'] if pct < 85 else (t['f1_less'] if pct > 118 else t['f1_same'])
    faqs = [
        (t['q_in'].format(inn=inn), ans + ' ' + basis),
        (t['f1q'].format(nom=nom, nom_l=nom_l), f1.format(pct=pct)),
        (t['f2q'].format(nom_l=nom_l, nom=nom), t['f2a'].format(c=c400)),
        (t['f3q'].format(nom_l=nom_l, nom=nom), t['f3a']),
    ]
    low = f'<p class="small">{E(t["low_conf"])}</p>' if d['conf'] == 'low' else ''
    related = [(a, b) for a, b in PAIRS if i in (a, b)][:6]
    rl = ''.join(f'<a href="{B.PATH[key_c(a, b)](lang)}">{E(N[a]["nom"][lang])} vs {E(N[b]["nom"][lang])}</a>' for a, b in related)
    rel = f'<section class="seo-sec"><div class="quiet-links">{rl}</div></section>' if rl else ''
    key = key_d(i)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
{crumbs_html(B, lang, key, nom)}
<h1 class="page-title">{E(t['q_in'].format(inn=inn))}</h1>
<div class="answer"><p class="answer-main">{E(ans)}</p><p class="small">{E(basis)}</p>{low}</div>
<section class="seo-sec"><h2>{E(t['h_facts'])}</h2>{table}</section>
{extra}{eve}
{faq_html(B, lang, faqs)}
{rel}
{tools_links(B, lang, i, 'filter' if i != 'filter' else 'espresso')}
{src_html(B, lang, d['src'] + ['efsa'])}
</main>
{jsonld(B, lang, key, nom, faqs)}'''
    return B.shell(lang, key, title, desc, main)


def pair_page(B, a, b, lang):
    E = B.E
    t = L[lang]
    D = drink_map()
    A, Bd = D[a], D[b]
    an, bn = N[a]['nom'][lang], N[b]['nom'][lang]
    ratio = A['typ'] / Bd['typ']
    overlap = A['lo'] <= Bd['hi'] and Bd['lo'] <= A['hi']
    hi_d, lo_d = (a, b) if ratio >= 1 else (b, a)
    hn, ln = N[hi_d]['nom'][lang], N[lo_d]['nom'][lang]
    r = max(ratio, 1 / ratio)
    similar = r < 1.2
    low = lambda n: n[0].lower() + n[1:]
    hx = hn if lang == 'lt' else low(hn)
    verdict = t['v_same'].format(a=an, b=low(bn)) if similar else t['v_more'].format(x=hx, y=low(ln), r=num(round(r, 1), lang))
    p_a, p_b = A['typ'] / A['ml'], Bd['typ'] / Bd['ml']
    pr = max(p_a / p_b, p_b / p_a)
    if pr < 1.2:
        v100 = t['v_p100_same']
    else:
        x, y = (low(an), low(bn)) if p_a > p_b else (low(bn), low(an))
        v100 = t['v_p100'].format(x=x, y=y, r=num(round(pr, 1), lang))
    ov = t['v_overlap'] if overlap and not similar else ''
    rg = lambda d: f'{d["lo"]}–{d["hi"]} mg' if d['lo'] != d['hi'] else f'{d["typ"]} mg'
    table = (f'<table class="cmp"><thead><tr><th></th><th><a href="{B.PATH[key_d(a)](lang)}">{E(an)}</a></th><th><a href="{B.PATH[key_d(b)](lang)}">{E(bn)}</a></th></tr></thead><tbody>'
             f'<tr><th scope="row">{E(t["r_cup"])}</th><td>{rg(A)}</td><td>{rg(Bd)}</td></tr>'
             f'<tr><th scope="row">{E(t["r_vol"])}</th><td>{A["ml"]} ml</td><td>{Bd["ml"]} ml</td></tr>'
             f'<tr><th scope="row">{E(t["r_p100"])}</th><td>{num(round(p_a * 100, 1), lang)}</td><td>{num(round(p_b * 100, 1), lang)}</td></tr>'
             f'<tr><th scope="row">{E(t["r_c400"])}</th><td>{cups_txt(400, A, lang)}</td><td>{cups_txt(400, Bd, lang)}</td></tr></tbody></table>')
    n_eq = num(round(A['typ'] / Bd['typ'], 1), lang)
    lower, higher = (a, b) if A['typ'] < Bd['typ'] else (b, a)
    xn, yn = N[lower]['nom'][lang], N[higher]['nom'][lang]
    faqs = [
        (t['c_f1q'].format(a=an, b=bn), verdict + (' ' + ov if ov else '')),
        (t['c_f2q'].format(a_g=an.lower(), b_g=bn.lower()), t['c_f2a'].format(a_n=an.lower(), b_n=bn.lower(), atyp=A['typ'], btyp=Bd['typ'], n=n_eq)),
        (t['c_f3q'], t['c_f3a'].format(x=(low(xn) if lang == 'lt' else xn), y=low(yn), xt=D[lower]['typ'], yt=D[higher]['typ'])),
    ]
    key = key_c(a, b)
    title = t['t_cmp'].format(a=an, b=bn)
    desc = t['c_desc'].format(a=an, b=bn, alo=A['lo'], ahi=A['hi'], blo=Bd['lo'], bhi=Bd['hi'])
    srcs = []
    for k in A['src'] + Bd['src'] + ['efsa']:
        if k not in srcs:
            srcs.append(k)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
{crumbs_html(B, lang, key, f'{an} vs {bn}')}
<h1 class="page-title">{E(t['c_h1'].format(a=an, b=bn))}</h1>
<div class="answer"><p class="answer-main">{E(verdict)}</p><p>{E(v100)}</p>{f'<p class="small">{E(ov)}</p>' if ov else ''}</div>
<section class="seo-sec">{table}<p style="margin-top:16px"><a class="btn btn-forest btn-sm" href="{B.PATH['compare'](lang)}?a={a}&amp;b={b}">{E(t['c_open'])} →</a></p></section>
{faq_html(B, lang, faqs)}
<section class="seo-sec"><div class="quiet-links"><a href="{B.PATH[key_d(a)](lang)}">{E(t['c_page'].format(n=an))}</a><a href="{B.PATH[key_d(b)](lang)}">{E(t['c_page'].format(n=bn))}</a></div></section>
{tools_links(B, lang, a, b)}
{src_html(B, lang, srcs)}
</main>
{jsonld(B, lang, key, f'{an} vs {bn}', faqs)}'''
    return B.shell(lang, key, title, desc, main)


def hub_d_page(B, lang):
    E = B.E
    t = L[lang]
    D = sorted(caff.drinks(), key=lambda d: -d['typ'])
    trs = ''
    for d in D:
        rg = f'{d["lo"]}–{d["hi"]}' if d['lo'] != d['hi'] else str(d['typ'])
        trs += f'<tr><th scope="row"><a href="{B.PATH[key_d(d["id"])](lang)}">{E(N[d["id"]]["nom"][lang])}</a></th><td>{rg}</td><td>{d["ml"]}</td><td>{num(round(d["typ"] / d["ml"] * 100, 1), lang)}</td></tr>'
    table = f'<table class="cmp"><thead><tr><th>{E(t["th_drink"])}</th><th>{E(t["th_cup"])}</th><th>{E(t["th_ml"])}</th><th>{E(t["th_p100"])}</th></tr></thead><tbody>{trs}</tbody></table>'
    main = f'''<main id="main" class="wrap wrap-narrow seo">
{crumbs_html(B, lang, 'hub_d', t['hub_d'])}
<h1 class="page-title">{E(t['hub_d_h1'])}</h1><p class="lead">{E(t['hub_d_lead'])}</p>
<section class="seo-sec chart-card" style="margin-top:0">{table}</section>
{tools_links(B, lang)}
<section class="seo-sec"><div class="quiet-links"><a href="{B.PATH['hub_c'](lang)}">{E(t['hub_c'])}</a><a href="{B.PATH['g_limit'](lang)}">{E(t['g_h1'])}</a><a href="{B.PATH['hub_b'](lang)}">{E(__import__('brands_gen').T[lang]['hub'])}</a><a href="{B.PATH['hub_t'](lang)}">{E(__import__('tealib_gen').T[lang]['hub'])}</a></div></section>
{src_html(B, lang, ['mayo', 'foods', 'matcha', 'mate', 'efsa'])}
</main>
{jsonld(B, lang, 'hub_d', t['hub_d'], [])}'''
    return B.shell(lang, 'hub_d', t['hub_d_t'], t['hub_d_desc'], main)


def hub_c_page(B, lang):
    E = B.E
    t = L[lang]
    links = ''.join(f'<li><a href="{B.PATH[key_c(a, b)](lang)}">{E(N[a]["nom"][lang])} vs {E(N[b]["nom"][lang])}</a></li>' for a, b in PAIRS)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
{crumbs_html(B, lang, 'hub_c', t['hub_c'])}
<h1 class="page-title">{E(t['hub_c_h1'])}</h1><p class="lead">{E(t['hub_c_lead'])}</p>
<ul class="pairs">{links}</ul>
{tools_links(B, lang)}
</main>
{jsonld(B, lang, 'hub_c', t['hub_c'], [])}'''
    return B.shell(lang, 'hub_c', t['hub_c_t'], t['hub_c_desc'], main)


def guide_page(B, lang):
    E = B.E
    t = L[lang]
    D = sorted([d for d in caff.drinks() if d['id'] != 'decaf'], key=lambda d: d['typ'])
    trs = ''.join(f'<tr><th scope="row"><a href="{B.PATH[key_d(d["id"])](lang)}">{E(N[d["id"]]["nom"][lang])}</a></th><td>{cups_txt(400, d, lang)}</td><td>{cups_txt(200, d, lang)}</td></tr>' for d in D)
    table = f'<table class="cmp"><thead><tr><th>{E(t["th_drink"])}</th><th>{E(t["g_c400"])}</th><th>{E(t["g_c200"])}</th></tr></thead><tbody>{trs}</tbody></table>'
    lims = ''.join(f'<li>{E(x)}</li>' for x in t['g_lims'])
    key = 'g_limit'
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <span>{E(t['guides'])}</span></div>
<h1 class="page-title">{E(t['g_h1'])}</h1><p class="lead">{E(t['g_lead'])}</p>
<section class="seo-sec"><h2>{E(t['g_h_lim'])}</h2><ul class="limits">{lims}</ul></section>
<section class="seo-sec"><h2>{E(t['g_h_cups'])}</h2><p>{E(t['g_cups_note'])}</p><div class="chart-card" style="margin-top:0">{table}</div></section>
<section class="seo-sec"><h2>{E(t['g_h_half'])}</h2><p>{E(t['g_half'])}</p></section>
<p class="answer small">{E(t['g_note'])}</p>
{tools_links(B, lang)}
{src_html(B, lang, ['efsa', 'fsanz', 'mayo'])}
</main>
{jsonld(B, lang, key, t['g_h1'], [])}'''
    return B.shell(lang, key, t['g_t'], t['g_desc'], main)


def pages(B):
    register(B)
    out = []
    for lang in B.LANGS:
        out.append((B.PATH['hub_d'](lang) + 'index.html', hub_d_page(B, lang)))
        out.append((B.PATH['hub_c'](lang) + 'index.html', hub_c_page(B, lang)))
        out.append((B.PATH['g_limit'](lang) + 'index.html', guide_page(B, lang)))
        for i in N:
            out.append((B.PATH[key_d(i)](lang) + 'index.html', drink_page(B, i, lang)))
        for a, b in PAIRS:
            out.append((B.PATH[key_c(a, b)](lang) + 'index.html', pair_page(B, a, b, lang)))
    return out
