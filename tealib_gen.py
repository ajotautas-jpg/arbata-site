"""Arbatų biblioteka (LT/EN/IT): hub + puslapis kiekvienai arbatos rūšiai (juodoji, žalioji, oolong, baltoji, pu-erh, yerba mate, matcha).
Skaičiai (kofeinas) imami iš caff.py, markės iš brands_data.py; apdorojimo, skonio ir plikymo faktai turi šaltinius (SRC).
Generuoja build.py (register / pages / all_keys)."""
import json
import caff
import brands_data as BD
import seo_gen as SG

DIR = {'lt': 'biblioteka', 'en': 'tea-library', 'it': 'libreria-te'}
IDS = ['black', 'green', 'oolong', 'white', 'puerh', 'mate', 'matcha']

# papildomi šaltiniai (be caff.SOURCES)
SRC = {
    'ift': ('IFT Food Technology: Processing, how tea is processed', 'https://www.ift.org/food-technology-magazine/processing-how-tea-is-processed'),
    'ka': ('KitchenAid: Tea temperatures, a guide to brewing tea', 'https://www.kitchenaid.com/countertop-appliances/pinch-of-help/tea-temperatures'),
    'nutr': ('Nutrition Reviews 2008;66(2):82–90: Psychological effects of dietary components of tea: caffeine and L-theanine', 'https://pubmed.ncbi.nlm.nih.gov/18254874/'),
    'wp_puerh': ('Wikipedia: Pu-erh tea', 'https://en.wikipedia.org/wiki/Pu-erh_tea'),
    'wp_mate': ('Wikipedia: Yerba mate', 'https://en.wikipedia.org/wiki/Yerba_mate'),
    'wp_matcha': ('Wikipedia: Matcha', 'https://en.wikipedia.org/wiki/Matcha'),
    'wp_white': ('Wikipedia: White tea', 'https://en.wikipedia.org/wiki/White_tea'),
    'wp_rooibos': ('Wikipedia: Rooibos', 'https://en.wikipedia.org/wiki/Rooibos'),
    'wp_herbal': ('Wikipedia: Herbal tea', 'https://en.wikipedia.org/wiki/Herbal_tea'),
    'wp_sencha': ('Wikipedia: Sencha', 'https://en.wikipedia.org/wiki/Sencha'),
    'wp_yellow': ('Wikipedia: Yellow tea', 'https://en.wikipedia.org/wiki/Yellow_tea'),
    'wp_earlgrey': ('Wikipedia: Earl Grey tea', 'https://en.wikipedia.org/wiki/Earl_Grey_tea'),
    'yama_hojicha': ('Yamamotoyama: Does Hojicha have less caffeine?', 'https://ec.yamamotoyama.co.jp/en/blogs/column/reading204'),
    'ci_herbal': ('Caffeine Informer: Herbal tea caffeine content', 'https://www.caffeineinformer.com/caffeine-content/herbal-tea'),
}


def source(k):
    return SRC[k] if k in SRC else caff.SOURCES[k]


# tipiniai plikymo duomenys: (temperatūra °C, laikas min. arba tekstas), šaltiniai
BREW = {
    'black': ('95–100', '3–5', ['ka']),
    'green': ('70–82', '1–3', ['ka']),
    'oolong': ('85–95', '2–3', ['ka']),
    'white': ('75–85', '1–2', ['ka', 'wp_white']),
    'puerh': ('95–100', '2–3', ['ka', 'wp_puerh']),
    'mate': ('70–80', None, ['wp_mate']),
    'matcha': ('80–90', None, ['wp_matcha']),
}
FIXSRC = {'black': ['ift'], 'green': ['ift'], 'oolong': ['ift'], 'white': ['ift', 'wp_white'], 'puerh': ['wp_puerh'], 'mate': ['wp_mate'], 'matcha': ['wp_matcha']}

# turinys: made (kaip gaminama), taste (skonis), brew (plikymo pastaba), best (kada tinka, pagal kofeiną)
X = {
 'lt': {
  'black': dict(
    kind='Visiškai oksiduota arbata',
    made='Lapai vytinami, sutraiškomi ar sugnybti (ortodoksiškas būdas laiko lapus sveikus, CTC būdas supjausto juos į smulkius gabalėlius), oksiduojami iki galo (100 %) ir išdžiovinami.',
    taste='Dažniausiai pilnesnio skonio ir tamsesnės spalvos nei žalioji; tai labiausiai paplitusi arbata maišeliuose.',
    brew='Verdantis vanduo; maždaug 3–5 minutės.'),
  'green': dict(
    kind='Neoksiduota arbata',
    made='Lapai nėra oksiduojami: trumpas kaitinimas (kinų keptuvėje arba japoniškas garinimas) išjungia oksidaciją sukeliančius fermentus, tada lapai formuojami ir džiovinami.',
    taste='Dažniausiai šviesesnis, gaivesnis, žolinis skonis; per karštas vanduo ar per ilgas plikymas daro ją kartesnę.',
    brew='Vėsesnis nei verdantis vanduo, maždaug 70–82 °C; trumpai, apie 1–3 minutes.'),
  'oolong': dict(
    kind='Dalinai oksiduota arbata',
    made='Oksidacija sustabdoma per vidurį: oolong būna oksiduotas nuo maždaug 5 % iki 70 %, todėl skonis gali būti arčiau žaliosios arba arčiau juodosios.',
    taste='Plati skonių gama: nuo lengvų, gėlių iki sodresnių, skrudintų; priklauso nuo oksidacijos ir skrudinimo.',
    brew='Maždaug 85–95 °C; apie 2–3 minutes, lapus dažnai galima plikyti kelis kartus.'),
  'white': dict(
    kind='Minimaliai apdorota arbata',
    made='Daugiausia pumpurai ir jauni lapai; jie tik vytinami ir švelniai džiovinami, nesukti ir neoksiduojami. Dažniausiai gaminama Kinijoje, Fudzianio provincijoje.',
    taste='Lengvesnis už daugumą žaliųjų ir juodųjų arbatų, šviesiai geltonas užpilas.',
    brew='Maždaug 75–85 °C; apie 1–2 minutes.'),
  'puerh': dict(
    kind='Mikrobiologiškai fermentuota arbata',
    made='Kilusi iš Junano (Kinija). Pu-erh fermentuoja pelėsiai, bakterijos ir mielės (tai ne fermentinė oksidacija, kaip juodojoje). Žalias (šeng) brandinamas metais; tamsus (šou) gaminamas „šlapiu krovimu“, kuris trunka maždaug 45–60 dienų.',
    taste='Jauna žalia pu-erh dažnai stipri, kartoka ir sutraukianti; ilgai brandinta švelnesnė, su žemiškais atspalviais. Tamsi pu-erh turi fermentuotą, žemišką skonį.',
    brew='Maždaug 95–100 °C; tradiciniame gongfu plikyme (85–99 °C) pirma infuzija trunka vos 12–30 sekundžių, o toliau laikas pamažu ilgėja.'),
  'mate': dict(
    kind='Ne arbata, o Ilex paraguariensis lapai',
    made='Gaminama iš pietų Amerikos holio rūšies Ilex paraguariensis lapų, ne iš arbatmedžio (Camellia sinensis). Tradiciškai geriama iš moliūgo indo per bombillą (metalinį ar medinį šiaudelį); šaltas variantas vadinamas tereré.',
    taste='Primena daržovių, žolelių ir žolės užpilą, šiek tiek kaip kai kurios žaliosios arbatos; karštame vandenyje dažnai kartoka.',
    brew='Karštas, bet ne verdantis vanduo, maždaug 70–80 °C; indas pripildomas maždaug trimis ketvirtadaliais lapų, o užpilas pildomas iš naujo.'),
  'matcha': dict(
    kind='Šešėlyje auginta, sumalta visa lapo arbata',
    made='Lapai kelias savaites (pagal japonų standartą 2–3) prieš derlių pridengiami, garinami ir džiovinami nesukti (tai vadinama tencha), tada sumalami akmeniniais girnapusiais į smulkius miltelius. Geriama viso lapo milteliai, ne tik užpilas.',
    taste='Stipraus umami skonio, kurį dažniausiai siejama su aminorūgštimis, tokiomis kaip teaninas.',
    brew='Plakama bambukiniu šluotele (chasen): įprastam plonam variantui (usucha) naudojamas apie 90 °C vanduo, tirštam (koicha) apie 80 °C. Kadangi geriamas visas lapas, kofeino viename puodelyje daugiau.'),
 },
 'en': {
  'black': dict(
    kind='Fully oxidised tea',
    made='Leaves are withered, bruised or rolled (the orthodox method keeps leaves whole, CTC cuts them into small pieces), fully oxidised (100%) and dried.',
    taste='Usually fuller in flavour and darker than green tea; it is the most common tea in teabags.',
    brew='Boiling water, about 3–5 minutes.'),
  'green': dict(
    kind='Unoxidised tea',
    made='Leaves are not oxidised: brief heating (pan-firing in China or steaming in Japan) stops the enzymes that cause oxidation, then the leaves are shaped and dried.',
    taste='Usually lighter, fresher and grassier; water that is too hot or steeping that is too long makes it more bitter.',
    brew='Cooler than boiling water, about 70–82 °C, and short: roughly 1–3 minutes.'),
  'oolong': dict(
    kind='Partly oxidised tea',
    made='Oxidation is stopped part-way: oolong is oxidised from about 5% up to 70%, so it can taste closer to green or closer to black.',
    taste='A wide range, from light and floral to richer and roasted, depending on oxidation and roasting.',
    brew='About 85–95 °C for roughly 2–3 minutes; the leaves can often be infused several times.'),
  'white': dict(
    kind='Minimally processed tea',
    made='Mostly buds and young leaves that are only withered and gently dried, neither rolled nor oxidised. It is mainly produced in China, especially Fujian.',
    taste='Lighter than most green or black teas, with a pale yellow cup.',
    brew='About 75–85 °C for roughly 1–2 minutes.'),
  'puerh': dict(
    kind='Microbially fermented tea',
    made='From Yunnan, China. Pu-erh is fermented by moulds, bacteria and yeasts (not the enzymatic oxidation of black tea). Raw (sheng) pu-erh is aged for years; ripe (shou) pu-erh is made by "wet piling", which takes about 45–60 days.',
    taste='Young raw pu-erh is often strong, bitter and astringent; well-aged it turns smoother and earthy. Ripe pu-erh has a fermented, earthy taste.',
    brew='About 95–100 °C; in traditional gongfu brewing (85–99 °C) the first infusion lasts just 12–30 seconds and later ones get slightly longer.'),
  'mate': dict(
    kind='Not tea: leaves of Ilex paraguariensis',
    made='Made from the leaves of a South American holly, Ilex paraguariensis, not from the tea plant (Camellia sinensis). Traditionally drunk from a gourd through a bombilla (a metal or wooden straw); the cold version is called tereré.',
    taste='Like an infusion of vegetables, herbs and grass, somewhat like some green teas; often bitter when steeped in hot water.',
    brew='Hot but not boiling water, about 70–80 °C; the gourd is filled about three-quarters with leaves and topped up repeatedly.'),
  'matcha': dict(
    kind='Shade-grown, whole-leaf powdered tea',
    made='Leaves are shaded for a few weeks before harvest (2–3 weeks under the Japanese standard), steamed and dried without rolling (this is tencha), then ground to a fine powder in stone mills. You drink the whole leaf, not just an infusion.',
    taste='A strong umami flavour, which is mostly attributed to amino acids such as theanine.',
    brew='Whisked with a bamboo chasen: thin matcha (usucha) uses about 90 °C water, thick matcha (koicha) about 80 °C. Because you drink the whole leaf, a cup usually carries more caffeine.'),
 },
 'it': {
  'black': dict(
    kind='Tè completamente ossidato',
    made='Le foglie vengono appassite, arrotolate o contuse (il metodo ortodosso mantiene le foglie intere, il CTC le taglia in piccoli pezzi), ossidate del tutto (100%) ed essiccate.',
    taste='Di solito più pieno e scuro del tè verde; è il tè più comune nelle bustine.',
    brew='Acqua bollente, circa 3–5 minuti.'),
  'green': dict(
    kind='Tè non ossidato',
    made='Le foglie non vengono ossidate: un breve riscaldamento (in padella in Cina o a vapore in Giappone) ferma gli enzimi dell\'ossidazione, poi le foglie vengono modellate ed essiccate.',
    taste='Di solito più leggero, fresco ed erbaceo; acqua troppo calda o infusione troppo lunga lo rendono più amaro.',
    brew='Acqua meno calda del bollore, circa 70–82 °C, e breve: circa 1–3 minuti.'),
  'oolong': dict(
    kind='Tè parzialmente ossidato',
    made='L\'ossidazione si ferma a metà: l\'oolong è ossidato da circa il 5% fino al 70%, quindi può somigliare di più al verde o al nero.',
    taste='Una gamma ampia, da leggero e floreale a più ricco e tostato, secondo ossidazione e tostatura.',
    brew='Circa 85–95 °C per 2–3 minuti; le foglie si possono spesso infondere più volte.'),
  'white': dict(
    kind='Tè poco lavorato',
    made='Soprattutto gemme e foglie giovani, solo appassite ed essiccate con delicatezza, né arrotolate né ossidate. Si produce soprattutto in Cina, in particolare nel Fujian.',
    taste='Più leggero della maggior parte dei tè verdi o neri, con una tazza giallo pallido.',
    brew='Circa 75–85 °C per 1–2 minuti.'),
  'puerh': dict(
    kind='Tè fermentato da microrganismi',
    made='Viene dallo Yunnan, in Cina. Il pu-erh è fermentato da muffe, batteri e lieviti (non è l\'ossidazione enzimatica del tè nero). Il crudo (sheng) invecchia per anni; il maturo (shou) si ottiene con l\'ammasso a umido, che dura circa 45–60 giorni.',
    taste='Il pu-erh crudo giovane è spesso forte, amaro e astringente; invecchiato bene diventa più morbido e terroso. Il maturo ha un gusto fermentato e terroso.',
    brew='Circa 95–100 °C; nell\'infusione gongfu tradizionale (85–99 °C) la prima infusione dura solo 12–30 secondi e le successive si allungano un poco.'),
  'mate': dict(
    kind='Non è tè: foglie di Ilex paraguariensis',
    made='Si ricava dalle foglie di un agrifoglio sudamericano, l\'Ilex paraguariensis, non dalla pianta del tè (Camellia sinensis). Si beve tradizionalmente da una zucca con la bombilla (cannuccia di metallo o legno); la versione fredda si chiama tereré.',
    taste='Ricorda un infuso di verdure, erbe e erba, un po\' come certi tè verdi; spesso amaro se infuso in acqua calda.',
    brew='Acqua calda ma non bollente, circa 70–80 °C; la zucca si riempie per tre quarti di foglie e si rabbocca più volte.'),
  'matcha': dict(
    kind='Tè in polvere coltivato all\'ombra, a foglia intera',
    made='Le foglie vengono ombreggiate per alcune settimane prima del raccolto (2–3 secondo lo standard giapponese), cotte al vapore ed essiccate senza arrotolare (si chiama tencha), poi macinate a pietra in polvere fine. Si beve tutta la foglia, non solo l\'infuso.',
    taste='Un forte sapore umami, attribuito soprattutto agli amminoacidi come la teanina.',
    brew='Si sbatte con il chasen di bambù: il matcha leggero (usucha) usa acqua a circa 90 °C, quello denso (koicha) a circa 80 °C. Poiché si beve tutta la foglia, una tazza contiene di solito più caffeina.'),
 },
}

T = {
 'lt': dict(
  hub='Arbatų biblioteka', hub_h1='Arbatų biblioteka: rūšys, kofeinas ir plikymas',
  hub_t='Arbatų biblioteka: juodoji, žalioji, rooibos, sencha, matcha ir kitos',
  hub_desc='Kiekviena arbatos rūšis: kaip gaminama, kiek kofeino, kaip plikyti ir kada gerti. Skaičiai su šaltiniais ir diapazonais.',
  hub_lead='Arbatos rūšis lemia ne tik skonį: nuo jos priklauso ir kofeino kiekis. Čia surinkome septynias dažniausias rūšis su diapazonais, plikymu ir šaltiniais, o toliau dar šešis užpilus ir variantus, tarp jų ir tokius be kofeino.',
  th_tea='Rūšis', th_kind='Gaminimas', th_cup='Kofeino puodelyje', th_temp='Vanduo, °C',
  h_order='Nuo mažiau iki daugiau kofeino', order_note='Rūšys išrikiuotos pagal vidutinį kofeino kiekį puodelyje. Diapazonai persidengia, todėl konkretus puodelis gali būti kitoks.',
  h_theanine='Kofeinas arbatoje ir teaninas', theanine='Arbata turi ir L-teanino. Apžvalga Nutrition Reviews (2008) nurodo, kad arbata, gerta reguliariais intervalais, gali padėti išlaikyti budrumą ir dėmesį, o teaninas kartu su kofeinu gali pagerinti dėmesio perjungimą. Tai bendra informacija, ne medicininė konsultacija.',
  h1='{nom}: kofeinas, plikymas ir skonis', t='{nom}: kofeinas, plikymas ir skonis ({rg})',
  d='{nom}: {rg} kofeino puodelyje, kaip gaminama, kaip plikyti ir kada gerti. Skaičiai su šaltiniais.',
  ans='{nom} puodelyje ({ml} ml) paprastai yra {rg} kofeino, vidutiniškai apie {typ} mg ({pct} % filtruotos kavos puodelio).',
  h_glance='Trumpai', r_kind='Rūšis', r_cup='Kofeino puodelyje', r_p100='mg / 100 ml', r_c400='Puodeliai iki 400 mg per dieną', r_temp='Vandens temperatūra', r_time='Plikymo laikas',
  min_word='min.', na='pagal skonį ir receptą', h_made='Kaip gaminama', h_taste='Skonis', h_brew='Kaip plikyti', brew_amount='Kofeino skaičiavimams naudojame {g} g sausos arbatos puodeliui ({ml} ml).',
  brew_tools='Pasirink plikymo laiką ir pamatyk apytikslį kofeiną:', h_time='Plikymo laikas ir kofeinas', time_note='Ilgiau plikoma arbata išskiria daugiau kofeino. Apskaičiuota {g} g arbatos puodeliui.',
  b_time='Laikas', h_day='Kada gerti', day='Kofeino pusinės eliminacijos laikas dažniausiai 3–7 val. (naudojame apie 5), todėl po {h} val. organizme gali likti maždaug pusė puodelio kofeino. Apie 100 mg prieš miegą gali veikti miegą (EUFIC).',
  day_tool='Paskutinio puodelio įrankis', h_brands='Gamintojai ir produktai', brands_note='Gamintojų nurodytas kofeinas šios rūšies produktuose (tik oficialūs duomenys):',
  h_faq='Dažni klausimai', q1='Kiek kofeino yra {inn}?', q2='Kaip plikyti {gen}?', a2='{brew} {amount}', q3='Ar {nom_l} tinka gerti vakare?', a3='Puodelyje yra apie {typ} mg kofeino. Po {h} val. gali likti maždaug pusė, todėl jautresniems žmonėms geriau rinktis anksčiau. Kai kurie žmonės kofeinui jautresni nei kiti.',
  h_more='Taip pat naudinga', all_lib='Visos rūšys', page_caf='Kofeino kiekis: {nom}', hub_c='Gėrimų palyginimai', hub_b='Arbatų gamintojai', calc='Kofeino skaičiuoklė', timer='Plikymo laikmatis', compare='Palyginti du gėrimus',
  h_src='Šaltiniai', src_note='Plikymo temperatūra ir laikas orientacinis: gamintojų nurodymai gali skirtis.', note='Duomenys patikrinti {d}. Bendra informacija, ne medicininė konsultacija.', home='Pagrindinis',
  gen={'black': 'juodąją arbatą', 'green': 'žaliąją arbatą', 'oolong': 'oolong', 'white': 'baltąją arbatą', 'puerh': 'pu-erh', 'mate': 'yerba mate', 'matcha': 'matcha'},
 ),
 'en': dict(
  hub='Tea library', hub_h1='Tea library: types, caffeine and brewing',
  hub_t='Tea library: black, green, rooibos, sencha, matcha and more',
  hub_desc='Every tea type: how it is made, how much caffeine, how to brew and when to drink it. Figures with sources and ranges.',
  hub_lead='The type of tea decides more than flavour: it also shapes the caffeine. Here are the seven most common types with ranges, brewing and sources, followed by six more infusions and variants, including caffeine-free ones.',
  th_tea='Type', th_kind='How it is made', th_cup='Caffeine per cup', th_temp='Water, °C',
  h_order='From less to more caffeine', order_note='Types are ordered by average caffeine per cup. Ranges overlap, so a particular cup can differ.',
  h_theanine='Caffeine in tea and theanine', theanine='Tea also contains L-theanine. A review in Nutrition Reviews (2008) says tea taken at regular intervals may help maintain alertness and focused attention, and that theanine together with caffeine may improve attention switching. General information, not medical advice.',
  h1='{nom}: caffeine, brewing and taste', t='{nom}: caffeine, brewing and taste ({rg})',
  d='{nom}: {rg} of caffeine per cup, how it is made, how to brew it and when to drink it. Figures with sources.',
  ans='A cup of {nom_l} ({ml} ml) usually has {rg} of caffeine, about {typ} mg on average ({pct}% of a cup of filter coffee).',
  h_glance='At a glance', r_kind='Type', r_cup='Caffeine per cup', r_p100='mg / 100 ml', r_c400='Cups to reach 400 mg a day', r_temp='Water temperature', r_time='Steeping time',
  min_word='min', na='to taste and recipe', h_made='How it is made', h_taste='Taste', h_brew='How to brew', brew_amount='For caffeine figures we assume {g} g of dry tea per cup ({ml} ml).',
  brew_tools='Pick a steeping time and see approximate caffeine:', h_time='Steeping time and caffeine', time_note='Longer steeping releases more caffeine. Calculated for {g} g of tea per cup.',
  b_time='Time', h_day='When to drink it', day='Caffeine\'s half-life is usually 3–7 hours (we use about 5), so after {h} hours roughly half a cup\'s caffeine can still be in the body. About 100 mg before bed may affect sleep (EUFIC).',
  day_tool='Last cup tool', h_brands='Brands and products', brands_note='Caffeine stated by manufacturers for products of this type (official data only):',
  h_faq='Frequently asked questions', q1='How much caffeine is in {inn}?', q2='How do you brew {gen}?', a2='{brew} {amount}', q3='Is {nom_l} good in the evening?', a3='A cup has about {typ} mg of caffeine. After {h} hours roughly half can remain, so sensitive people may prefer earlier in the day. Some people are more sensitive to caffeine than others.',
  h_more='Also useful', all_lib='All types', page_caf='Caffeine content: {nom}', hub_c='Drink comparisons', hub_b='Tea brands', calc='Caffeine calculator', timer='Brewing timer', compare='Compare two drinks',
  h_src='Sources', src_note='Brewing temperature and time are typical: manufacturers\' instructions may differ.', note='Data checked {d}. General information, not medical advice.', home='Home',
  gen={'black': 'black tea', 'green': 'green tea', 'oolong': 'oolong', 'white': 'white tea', 'puerh': 'pu-erh', 'mate': 'yerba mate', 'matcha': 'matcha'},
 ),
 'it': dict(
  hub='Libreria del tè', hub_h1='Libreria del tè: tipi, caffeina e infusione',
  hub_t='Libreria del tè: nero, verde, rooibos, sencha, matcha e altri',
  hub_desc='Ogni tipo di tè: come si fa, quanta caffeina, come prepararlo e quando berlo. Valori con fonti e intervalli.',
  hub_lead='Il tipo di tè decide più del gusto: influisce anche sulla caffeina. Ecco i sette tipi più comuni con intervalli, infusione e fonti, e poi altri sei infusi e varianti, anche senza caffeina.',
  th_tea='Tipo', th_kind='Lavorazione', th_cup='Caffeina per tazza', th_temp='Acqua, °C',
  h_order='Da meno a più caffeina', order_note='I tipi sono in ordine di caffeina media per tazza. Gli intervalli si sovrappongono, quindi una tazza può essere diversa.',
  h_theanine='Caffeina nel tè e teanina', theanine='Il tè contiene anche L-teanina. Una rassegna su Nutrition Reviews (2008) indica che il tè assunto a intervalli regolari può aiutare a mantenere vigilanza e attenzione, e che la teanina insieme alla caffeina può migliorare il cambio di attenzione. Informazioni generali, non parere medico.',
  h1='{nom}: caffeina, infusione e gusto', t='{nom}: caffeina, infusione e gusto ({rg})',
  d='{nom}: {rg} di caffeina per tazza, come si fa, come prepararlo e quando berlo. Valori con fonti.',
  ans='Una tazza di {nom_l} ({ml} ml) contiene di solito {rg} di caffeina, in media circa {typ} mg ({pct}% di una tazza di caffè filtro).',
  h_glance='In breve', r_kind='Tipo', r_cup='Caffeina per tazza', r_p100='mg / 100 ml', r_c400='Tazze per arrivare a 400 mg al giorno', r_temp='Temperatura dell\'acqua', r_time='Tempo di infusione',
  min_word='min', na='a gusto e secondo la ricetta', h_made='Come si fa', h_taste='Gusto', h_brew='Come prepararlo', brew_amount='Per i calcoli della caffeina usiamo {g} g di tè secco per tazza ({ml} ml).',
  brew_tools='Scegli il tempo di infusione e vedi la caffeina approssimativa:', h_time='Tempo di infusione e caffeina', time_note='Un\'infusione più lunga libera più caffeina. Calcolato per {g} g di tè per tazza.',
  b_time='Tempo', h_day='Quando berlo', day='L\'emivita della caffeina è di solito 3–7 ore (usiamo circa 5), quindi dopo {h} ore può restare circa metà della caffeina di una tazza. Circa 100 mg prima di dormire possono influire sul sonno (EUFIC).',
  day_tool='Strumento ultima tazza', h_brands='Marche e prodotti', brands_note='Caffeina indicata dai produttori per prodotti di questo tipo (solo dati ufficiali):',
  h_faq='Domande frequenti', q1='Quanta caffeina c\'è {inn}?', q2='Come si prepara {gen}?', a2='{brew} {amount}', q3='{nom} va bene la sera?', a3='Una tazza contiene circa {typ} mg di caffeina. Dopo {h} ore può restarne circa metà, quindi chi è più sensibile può preferire la mattina o il pomeriggio. Alcune persone sono più sensibili alla caffeina di altre.',
  h_more='Può servire anche', all_lib='Tutti i tipi', page_caf='Caffeina: {nom}', hub_c='Confronti di bevande', hub_b='Marche di tè', calc='Calcolatore di caffeina', timer='Timer di infusione', compare='Confronta due bevande',
  h_src='Fonti', src_note='Temperatura e tempo di infusione sono indicativi: le istruzioni dei produttori possono variare.', note='Dati controllati il {d}. Informazioni generali, non parere medico.', home='Home',
  gen={'black': 'il tè nero', 'green': 'il tè verde', 'oolong': 'l\'oolong', 'white': 'il tè bianco', 'puerh': 'il pu-erh', 'mate': 'lo yerba mate', 'matcha': 'il matcha'},
 ),
}

import tealib_extra as XT

BRAND_TYPES = {'herbal': ('herbal',), 'black': ('black', 'rtd_black'), 'green': ('green', 'rtd_green'), 'oolong': ('oolong',), 'white': ('white', 'rtd_white')}


def key_t(i): return 'tl_' + i


def register(B):
    B.PATH['hub_t'] = lambda l: f'/{l}/{DIR[l]}/'
    for i in IDS:
        B.PATH[key_t(i)] = (lambda i: lambda l: f'/{l}/{DIR[l]}/{SG.N[i]["slug"][l]}/')(i)
    for i in XT.IDS:
        B.PATH[key_t(i)] = (lambda i: lambda l: f'/{l}/{DIR[l]}/{XT.NAMES[i]["slug"][l]}/')(i)


def all_keys():
    return ['hub_t'] + [key_t(i) for i in IDS + XT.IDS]


def D(i):
    return [d for d in caff.drinks() if d['id'] == i][0]


def jsonld(B, lang, key, name, faqs):
    t = T[lang]
    crumbs = [(t['home'], B.BASE + B.PATH['home'](lang)), (t['hub'], B.BASE + B.PATH['hub_t'](lang))]
    if key != 'hub_t':
        crumbs.append((name, B.BASE + B.PATH[key](lang)))
    out = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'name': a, 'item': u} for n, (a, u) in enumerate(crumbs)]}]
    if faqs:
        out.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>' for o in out)


def src_block(B, lang, keys):
    E = B.E
    t = T[lang]
    seen = []
    for k in keys:
        if k not in seen:
            seen.append(k)
    items = ''.join(f'<li><a href="{source(k)[1]}" target="_blank" rel="noopener nofollow">{E(source(k)[0])}</a></li>' for k in seen)
    return f'<section class="seo-sec"><h2>{E(t["h_src"])}</h2><ul class="small srclist">{items}</ul><p class="small">{E(t["src_note"])} {E(t["note"].format(d=caff.CHECKED))}</p></section>'


def brand_block(B, lang, i):
    import brands_gen as BG
    E = B.E
    t = T[lang]
    types = BRAND_TYPES.get(i)
    if not types:
        return ''
    lines = ''
    for r in BD.rows():
        if r['type'] in types and BD.official(r) and r['lo'] is not None and r['hi'] is not None and (r['avg'] or i == 'herbal') and r['brand'] in BG.indexable():
            rg = BG.cell_cup(r, lang, BG.T[lang])
            lines += f'<a class="lib-card" href="{B.PATH[BG.key_b(r["brand"])](lang)}"><span class="lib-name">{E(BD.brand_name(r["brand"]))}</span><span class="lib-kind">{E(rg)}</span><span class="lib-taste">{E(r["product"])}</span></a>'
    if not lines:
        return ''
    return f'<section class="seo-sec"><h2>{E(t["h_brands"])}</h2><p>{E(t["brands_note"])}</p><div class="lib-grid">{lines}</div><p class="small"><a href="{B.PATH["hub_b"](lang)}">{E(t["hub_b"])} →</a></p></section>'


def name_of(i, lang):
    return XT.NAMES[i]['nom'][lang] if i in XT.NAMES else SG.N[i]['nom'][lang]


T['lt'].update(
    x_title='Daugiau rūšių ir užpilų', x_note='Čia rūšys ir užpilai, kurių kofeino negalime pateikti vienu skaičiumi iš savo matavimų: nuo gėrimų be kofeino iki japoniškų žaliųjų ir aromatizuotų arbatų. Kur šaltinis skaičiaus nenurodo, jo nerodome.',
    xt='{nom}: ar turi kofeino? Plikymas ir skonis', xd='{nom}: {cs} Kaip gaminama, kaip plikyti, šaltiniai.',
    x_na='pagal pakuotę', x_min='min.', c_zero='0 mg', c_zero_herbal='dauguma 0 mg, bet ne visos', c_range='{lo}–{hi} mg puodelyje (įvertis)', c_per100='apie {v} mg / 100 ml (gamintojo duomenys)',
    c_none='patikimo skaičiaus nerasta', c_base='kaip pagrindo arbata: {lo}–{hi} mg', h_caf='Kofeinas', plan_cta='Keiti kavą kitu gėrimu? Pabandyk mažinimo planą', conv_cta='Kava → arbata keitiklis', cmp_cta='Palygink su filtrine kava',
    h_flavour='Variantai ir skonis')
T['en'].update(
    x_title='More types and infusions', x_note='Types and infusions where we cannot give one number from our own measurements: from caffeine-free drinks to Japanese green teas and flavoured teas. Where a source gives no number, we show none.',
    xt='{nom}: does it have caffeine? Brewing and taste', xd='{nom}: {cs} How it is made, how to brew it, sources.',
    x_na='see packaging', x_min='min', c_zero='0 mg', c_zero_herbal='most 0 mg, but not all', c_range='{lo}–{hi} mg per cup (estimate)', c_per100='about {v} mg / 100 ml (producer data)',
    c_none='no reliable figure found', c_base='as the base tea: {lo}–{hi} mg', h_caf='Caffeine', plan_cta='Replacing coffee with something else? Try the switch plan', conv_cta='Coffee → tea converter', cmp_cta='Compare with filter coffee',
    h_flavour='Variants and taste')
T['it'].update(
    x_title='Altri tipi e infusi', x_note='Tipi e infusi per cui non possiamo dare un solo numero dalle nostre misure: dalle bevande senza caffeina ai tè verdi giapponesi e ai tè aromatizzati. Dove la fonte non dà un numero, non lo mostriamo.',
    xt='{nom}: contiene caffeina? Infusione e gusto', xd='{nom}: {cs} Come si fa, come prepararlo, fonti.',
    x_na='vedi la confezione', x_min='min', c_zero='0 mg', c_zero_herbal='per lo più 0 mg, ma non tutte', c_range='{lo}–{hi} mg per tazza (stima)', c_per100='circa {v} mg / 100 ml (dati del produttore)',
    c_none='nessun valore affidabile trovato', c_base='come il tè di base: {lo}–{hi} mg', h_caf='Caffeina', plan_cta='Sostituisci il caffè con altro? Prova il piano di passaggio', conv_cta='Convertitore caffè → tè', cmp_cta='Confronta con il caffè filtro',
    h_flavour='Varianti e gusto')


def caf_cell(i, lang):
    t = T[lang]
    c = XT.CAF[i]
    k = c['kind']
    if k == 'zero':
        return t['c_zero_herbal'] if i == 'herbal' else t['c_zero']
    if k == 'range':
        return t['c_range'].format(lo=c['lo'], hi=c['hi'])
    if k == 'per100':
        return t['c_per100'].format(v=c['v'])
    if k == 'base':
        b = D('black')
        return t['c_base'].format(lo=b['lo'], hi=b['hi'])
    return t['c_none']


def extra_page(B, i, lang):
    E = B.E
    t = T[lang]
    x = dict(XT.X[lang][i])
    b = D('black')
    x['caf'] = x['caf'].replace('{lo}', str(b['lo'])).replace('{hi}', str(b['hi']))
    nom = XT.NAMES[i]['nom'][lang]
    temp, mins = XT.BREW[i]
    temp_txt = f'{temp} °C' if temp else t['x_na']
    time_txt = f'{mins} {t["x_min"]}' if mins else t['x_na']
    cell = caf_cell(i, lang)
    ans = x['caf'].split('. ')[0].rstrip('.') + '.'
    rows = [(t['r_kind'], x['kind']), (t['h_caf'], cell), (t['r_temp'], temp_txt), (t['r_time'], time_txt)]
    table = '<table class="cmp"><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(v)}</td></tr>' for a, v in rows) + '</tbody></table>'
    faqs = [
        (t['q1'].format(inn=XT.NAMES[i]['inn'][lang]), ans),
        (t['q2'].format(gen=XT.NAMES[i]['gen'][lang]), x['brew']),
        (x['f3q'], x['f3a']),
    ]
    key = key_t(i)
    others = [j for j in IDS + XT.IDS if j != i]
    ol = ''.join(f'<a href="{B.PATH[key_t(j)](lang)}">{E(name_of(j, lang))}</a>' for j in others)
    cta = ''
    if XT.CAF[i]['kind'] == 'zero':
        q = f'?tea={i}' if i in ('rooibos', 'herbal') else ''
        qc = f'?a=filter&amp;b={i}' if i in ('rooibos', 'herbal') else ''
        cta = (f'<p><a class="btn btn-forest btn-sm" href="{B.PATH["plan"](lang)}{q}">{E(t["plan_cta"])} →</a> '
               f'<a class="btn btn-outline btn-sm" href="{B.PATH["convert"](lang)}{q}">{E(t["conv_cta"])}</a>'
               + (f' <a class="btn btn-outline btn-sm" href="{B.PATH["compare"](lang)}{qc}">{E(t["cmp_cta"])}</a>' if qc else '') + '</p>')
    srcs = list(XT.SRC[i])
    rest = x['caf'][len(x['caf'].split('. ')[0]) + 1:].strip()
    cafsec = ''
    if rest or cta:
        cafsec = f'<section class="seo-sec"><h2>{E(t["h_caf"])}</h2>' + (f'<p>{E(rest)}</p>' if rest else '') + cta + '</section>'
    taste_h = t['h_flavour'] if i == 'earlgrey' else t['h_taste']
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <a href="{B.PATH['hub_t'](lang)}">{E(t['hub'])}</a> / <span>{E(nom)}</span></div>
<h1 class="page-title">{E(t['h1'].format(nom=nom))}</h1>
<div class="answer"><p class="answer-main">{E(ans)}</p></div>
<section class="seo-sec"><h2>{E(t['h_glance'])}</h2>{table}</section>
{cafsec}
<section class="seo-sec"><h2>{E(t['h_made'])}</h2><p>{E(x['made'])}</p></section>
<section class="seo-sec"><h2>{E(taste_h)}</h2><p>{E(x['taste'])}</p></section>
<section class="seo-sec"><h2>{E(t['h_brew'])}</h2><p>{E(x['brew'])}</p><p><a class="btn btn-outline btn-sm" href="{B.PATH['timer'](lang)}">{E(t['timer'])} →</a></p></section>
{brand_block(B, lang, i)}
{SG.faq_html(B, lang, faqs)}
<section class="seo-sec"><h2>{E(t['h_more'])}</h2><div class="quiet-links"><a href="{B.PATH['hub_t'](lang)}">{E(t['all_lib'])}</a>{ol}<a href="{B.PATH['calc'](lang)}">{E(t['calc'])}</a><a href="{B.PATH['hub_r'](lang)}">{E(__import__('rituals_gen').UI[lang]['hub'])}</a><a href="{B.PATH['g_limit'](lang)}">{E(SG.L[lang]['g_h1'])}</a></div></section>
{src_block(B, lang, srcs)}
</main>
{jsonld(B, lang, key, nom, faqs)}'''
    return B.shell(lang, key, t['xt'].format(nom=nom), t['xd'].format(nom=nom, cs=ans), main)


def tea_page(B, i, lang):
    E = B.E
    t = T[lang]
    x = X[lang][i]
    d = D(i)
    nom = SG.N[i]['nom'][lang]
    nom_l = nom if lang == 'lt' and i in ('puerh',) else nom[0].lower() + nom[1:]
    if lang == 'lt':
        nom_l = nom[0].lower() + nom[1:]
    fil = D('filter')['typ']
    pct = round(d['typ'] / fil * 100)
    rg = f'{d["lo"]}–{d["hi"]} mg'
    inn = SG.N[i]['in'][lang]
    temp, mins, bsrc = BREW[i]
    time_txt = f'{mins} {t["min_word"]}' if mins else t['na']
    p100 = SG.num(round(d['typ'] / d['ml'] * 100, 1), lang)
    ans = t['ans'].format(nom=nom, nom_l=nom_l, ml=d['ml'], rg=rg, typ=d['typ'], pct=pct)
    rows = [(t['r_kind'], x['kind']), (t['r_cup'], rg), (t['r_p100'], p100), (t['r_c400'], SG.cups_txt(400, d, lang)), (t['r_temp'], f'{temp} °C'), (t['r_time'], time_txt)]
    table = '<table class="cmp"><tbody>' + ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td></tr>' for a, b in rows) + '</tbody></table>'
    amount = t['brew_amount'].format(g=d['g'], ml=d['ml'])
    timetbl = ''
    if not d.get('whole') and i != 'mate':
        pg = d['perg']
        trs = ''.join(f'<tr><th scope="row">{m} {E(t["min_word"])}</th><td>{round(pg[0] * d["g"] * caff.TIME_F[m])}–{round(pg[1] * d["g"] * caff.TIME_F[m])} mg</td></tr>' for m in (2, 3, 4, 5))
        timetbl = f'<section class="seo-sec"><h2>{E(t["h_time"])}</h2><p>{E(t["time_note"].format(g=d["g"]))}</p><table class="cmp"><thead><tr><th>{E(t["b_time"])}</th><th>{E(t["r_cup"])}</th></tr></thead><tbody>{trs}</tbody></table></section>'
    half = 5
    faqs = [
        (t['q1'].format(inn=inn), ans),
        (t['q2'].format(gen=t['gen'][i]), t['a2'].format(brew=x['brew'], amount=amount)),
        (t['q3'].format(nom_l=nom_l, nom=nom), t['a3'].format(typ=d['typ'], h=half)),
    ]
    key = key_t(i)
    others = [j for j in IDS + XT.IDS if j != i]
    ol = ''.join(f'<a href="{B.PATH[key_t(j)](lang)}">{E(name_of(j, lang))}</a>' for j in others)
    srcs = FIXSRC[i] + bsrc + d['src'] + ['nutr', 'efsa']
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <a href="{B.PATH['hub_t'](lang)}">{E(t['hub'])}</a> / <span>{E(nom)}</span></div>
<h1 class="page-title">{E(t['h1'].format(nom=nom))}</h1>
<div class="answer"><p class="answer-main">{E(ans)}</p></div>
<section class="seo-sec"><h2>{E(t['h_glance'])}</h2>{table}</section>
<section class="seo-sec"><h2>{E(t['h_made'])}</h2><p>{E(x['made'])}</p></section>
<section class="seo-sec"><h2>{E(t['h_taste'])}</h2><p>{E(x['taste'])}</p></section>
<section class="seo-sec"><h2>{E(t['h_brew'])}</h2><p>{E(x['brew'])}</p><p class="small">{E(amount)}</p><p><a class="btn btn-forest btn-sm" href="{B.PATH['timer'](lang)}">{E(t['timer'])} →</a></p></section>
{timetbl}
<section class="seo-sec"><h2>{E(t['h_day'])}</h2><p>{E(t['day'].format(h=half))}</p><p><a class="btn btn-outline btn-sm" href="{B.PATH['lastcup'](lang)}">{E(t['day_tool'])} →</a></p></section>
{brand_block(B, lang, i)}
{SG.faq_html(B, lang, faqs)}
<section class="seo-sec"><h2>{E(t['h_more'])}</h2><div class="quiet-links"><a href="{B.PATH['hub_t'](lang)}">{E(t['all_lib'])}</a>{ol}<a href="{B.PATH[SG.key_d(i)](lang)}">{E(t['page_caf'].format(nom=nom))}</a><a href="{B.PATH['calc'](lang)}">{E(t['calc'])}</a><a href="{B.PATH['compare'](lang)}?a={i}&amp;b=filter">{E(t['compare'])}</a></div></section>
{src_block(B, lang, srcs)}
</main>
{jsonld(B, lang, key, nom, faqs)}'''
    return B.shell(lang, key, t['t'].format(nom=nom, rg=rg), t['d'].format(nom=nom, rg=rg), main)


def hub_page(B, lang):
    E = B.E
    t = T[lang]
    order = sorted(IDS, key=lambda i: D(i)['typ'])
    trs = ''
    for i in order:
        d = D(i)
        trs += (f'<tr><th scope="row"><a href="{B.PATH[key_t(i)](lang)}">{E(SG.N[i]["nom"][lang])}</a></th><td>{E(X[lang][i]["kind"])}</td>'
                f'<td>{d["lo"]}–{d["hi"]} mg</td><td>{E(BREW[i][0])}</td></tr>')
    table = f'<div class="chart-card" style="margin-top:0"><table class="cmp"><thead><tr><th>{E(t["th_tea"])}</th><th>{E(t["th_kind"])}</th><th>{E(t["th_cup"])}</th><th>{E(t["th_temp"])}</th></tr></thead><tbody>{trs}</tbody></table></div>'
    cards = ''.join(f'<a class="lib-card" href="{B.PATH[key_t(i)](lang)}"><span class="lib-name">{E(SG.N[i]["nom"][lang])}</span><span class="lib-kind">{E(X[lang][i]["kind"])}</span><span class="lib-taste">{E(X[lang][i]["taste"])}</span></a>' for i in IDS)
    xcards = ''.join(f'<a class="lib-card" href="{B.PATH[key_t(i)](lang)}"><span class="lib-name">{E(XT.NAMES[i]["nom"][lang])}</span><span class="lib-kind">{E(XT.X[lang][i]["kind"])}</span><span class="lib-taste">{E(caf_cell(i, lang))}</span></a>' for i in XT.IDS)
    srcs = ['ift', 'ka', 'nutr', 'foods', 'mayo', 'efsa', 'wp_puerh', 'wp_mate', 'wp_matcha', 'wp_white', 'wp_rooibos', 'wp_herbal', 'wp_sencha', 'wp_yellow', 'wp_earlgrey', 'yama_hojicha', 'ci_herbal']
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <span>{E(t['hub'])}</span></div>
<h1 class="page-title">{E(t['hub_h1'])}</h1><p class="lead">{E(t['hub_lead'])}</p>
<section class="seo-sec"><h2>{E(t['h_order'])}</h2><p>{E(t['order_note'])}</p>{table}</section>
<section class="seo-sec"><div class="lib-grid">{cards}</div></section>
<section class="seo-sec"><h2>{E(t['x_title'])}</h2><p>{E(t['x_note'])}</p><div class="lib-grid">{xcards}</div></section>
<section class="seo-sec"><h2>{E(t['h_theanine'])}</h2><p>{E(t['theanine'])}</p></section>
<section class="seo-sec"><div class="quiet-links"><a href="{B.PATH['hub_r'](lang)}">{E(__import__('rituals_gen').UI[lang]['hub'])}</a><a href="{B.PATH['hub_b'](lang)}">{E(t['hub_b'])}</a><a href="{B.PATH['hub_c'](lang)}">{E(t['hub_c'])}</a><a href="{B.PATH['calc'](lang)}">{E(t['calc'])}</a><a href="{B.PATH['quiz'](lang)}">{E(__import__('tools_gen').TXT['quiz'][lang]['menu'])}</a></div></section>
{src_block(B, lang, srcs)}
</main>
{jsonld(B, lang, 'hub_t', t['hub'], [])}'''
    return B.shell(lang, 'hub_t', t['hub_t'], t['hub_desc'], main)


def pages(B):
    register(B)
    out = []
    for lang in B.LANGS:
        out.append((B.PATH['hub_t'](lang) + 'index.html', hub_page(B, lang)))
        for i in IDS:
            out.append((B.PATH[key_t(i)](lang) + 'index.html', tea_page(B, i, lang)))
        for i in XT.IDS:
            out.append((B.PATH[key_t(i)](lang) + 'index.html', extra_page(B, i, lang)))
    return out
