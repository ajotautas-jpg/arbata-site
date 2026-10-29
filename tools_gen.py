"""Greitieji įrankiai (LT/EN/IT): keitiklis, palyginimas, paskutinis puodelis, laikmatis, sekiklis, kofeinas organizme.
Puslapius generuoja build.py (žr. register/pages), logika – static/assets/tools.js, duomenys – caff.py."""
import json

SLUG = {
    'convert': {'lt': 'kava-i-arbata', 'en': 'coffee-to-tea', 'it': 'caffe-a-te'},
    'compare': {'lt': 'gerimu-palyginimas', 'en': 'compare-drinks', 'it': 'confronta-bevande'},
    'lastcup': {'lt': 'paskutinis-puodelis', 'en': 'last-cup', 'it': 'ultima-tazza'},
    'timer': {'lt': 'plikymo-laikmatis', 'en': 'brewing-timer', 'it': 'timer-infusione'},
    'tracker': {'lt': 'dienos-sekiklis', 'en': 'daily-tracker', 'it': 'diario-caffeina'},
    'body': {'lt': 'kofeinas-organizme', 'en': 'caffeine-in-body', 'it': 'caffeina-nel-corpo'},
}
ICON = {'convert': 'compare', 'compare': 'compare', 'lastcup': 'moon', 'timer': 'timer', 'tracker': 'bars', 'body': 'chart'}
ORDER = ['convert', 'compare', 'lastcup', 'timer', 'tracker', 'body']
# tools, kuriems prasminga dalintis nuoroda su pasirinkimais
SHARE = {'convert': True, 'compare': True, 'lastcup': True, 'timer': True, 'tracker': False, 'body': False}

# Bendri tekstai
S = {
 'lt': {
  'zero_eq': 'puodelių be kofeino (kofeino −100 %)', 'zero_none': 'be kofeino', 'zero_cup': '0 mg puodelyje', 'zero_more': 'Apie šį gėrimą bibliotekoje',
  'zero_rooibos': 'Rooibos pagal šaltinius natūraliai neturi kofeino.', 'zero_herbal': 'Dauguma žolelių arbatų kofeino neturi, bet mišiniai su arbata, mate ar guarana gali turėti. Žiūrėk pakuotę.',
  'zero_plan': 'Su gėrimu be kofeino puodelis keičiamas puodeliu, todėl kofeinas mažėja kiekvieną savaitę.',
  'cups': 'Puodelių per dieną', 'coffee_kind': 'Tavo kava', 'target': 'Arbata vietoj kavos', 'drink': 'Gėrimas', 'a': 'Pirmas gėrimas', 'b': 'Antras gėrimas',
  'result': 'Rezultatas', 'per_cup': 'Kofeinas puodelyje', 'volume': 'Tūris', 'per100': 'mg / 100 ml', 'times': 'kartų',
  'bedtime': 'Einu miegoti', 'sens': 'Jautrumas kofeinui', 'sens_names': ['Jautrus', 'Vidutinis', 'Mažai jautrus'],
  'start': 'Pradėti', 'pause': 'Sustabdyti', 'resume': 'Tęsti', 'reset': 'Iš naujo', 'minutes': 'min.', 'steeping': 'Plikymo laikas', 'temp_hint': 'Įprasta temperatūra',
  'add': 'Pridėti', 'remove': 'Pašalinti', 'time': 'Laikas', 'today': 'Šiandien', 'empty': 'Dar nieko nepridėta.', 'clear': 'Išvalyti dieną',
  'profile': 'Profilis', 'profiles': ['Suaugęs', 'Nėščia ar žindanti'], 'limit': 'Dienos riba', 'total': 'Šiandien iš viso',
  'copy': 'Kopijuoti nuorodą', 'copied': 'Nukopijuota', 'embed': 'Įterpti į svetainę', 'embed_hide': 'Slėpti kodą', 'share_title': 'Pasidalink šiuo įrankiu',
  'link_note': 'Nuoroda atidaro įrankį su tavo pasirinkimais.', 'embed_note': 'Nukopijuok kodą ir įdėk į savo puslapį.',
  'all_tools': 'Visi įrankiai', 'more_tools': 'Daugiau įrankių', 'credit': 'Įrankis iš Arbata', 'src': 'Šaltiniai ir metodika', 'save_note': 'Duomenys saugomi tik šioje naršyklėje.',
  'note': 'Rodomi diapazonai, nes tyrimų skaičiai skiriasi. Bendra informacija, ne medicininė konsultacija.', 'related': 'Taip pat naudinga',
  'cups_word': 'puodeliai', 'about': 'apie', 'range': 'diapazonas', 'mg': 'mg', 'hour_short': 'val.',
 },
 'en': {
  'zero_eq': 'caffeine-free cups (caffeine −100%)', 'zero_none': 'caffeine-free', 'zero_cup': '0 mg per cup', 'zero_more': 'About this drink in the library',
  'zero_rooibos': 'According to the sources, rooibos is naturally caffeine-free.', 'zero_herbal': 'Most herbal teas contain no caffeine, but blends with tea, mate or guarana may. Check the packaging.',
  'zero_plan': 'With a caffeine-free drink, a cup is swapped for a cup, so caffeine drops every week.',
  'cups': 'Cups per day', 'coffee_kind': 'Your coffee', 'target': 'Tea instead of coffee', 'drink': 'Drink', 'a': 'First drink', 'b': 'Second drink',
  'result': 'Result', 'per_cup': 'Caffeine per cup', 'volume': 'Volume', 'per100': 'mg / 100 ml', 'times': 'times',
  'bedtime': 'I go to sleep at', 'sens': 'Caffeine sensitivity', 'sens_names': ['Sensitive', 'Average', 'Not very sensitive'],
  'start': 'Start', 'pause': 'Pause', 'resume': 'Resume', 'reset': 'Reset', 'minutes': 'min', 'steeping': 'Steeping time', 'temp_hint': 'Typical temperature',
  'add': 'Add', 'remove': 'Remove', 'time': 'Time', 'today': 'Today', 'empty': 'Nothing added yet.', 'clear': 'Clear the day',
  'profile': 'Profile', 'profiles': ['Adult', 'Pregnant or breastfeeding'], 'limit': 'Daily limit', 'total': 'Total today',
  'copy': 'Copy link', 'copied': 'Copied', 'embed': 'Embed on your site', 'embed_hide': 'Hide code', 'share_title': 'Share this tool',
  'link_note': 'The link opens the tool with your choices.', 'embed_note': 'Copy the code and paste it into your page.',
  'all_tools': 'All tools', 'more_tools': 'More tools', 'credit': 'Tool from Arbata', 'src': 'Sources and method', 'save_note': 'Data is stored only in this browser.',
  'note': 'Ranges are shown because studies report different numbers. General information, not medical advice.', 'related': 'Also useful',
  'cups_word': 'cups', 'about': 'about', 'range': 'range', 'mg': 'mg', 'hour_short': 'h',
 },
 'it': {
  'zero_eq': 'tazze senza caffeina (caffeina −100 %)', 'zero_none': 'senza caffeina', 'zero_cup': '0 mg per tazza', 'zero_more': 'Su questa bevanda nella libreria',
  'zero_rooibos': 'Secondo le fonti, il rooibos è naturalmente privo di caffeina.', 'zero_herbal': 'La maggior parte delle tisane non contiene caffeina, ma i miscugli con tè, mate o guaranà possono contenerne. Controlla la confezione.',
  'zero_plan': 'Con una bevanda senza caffeina una tazza sostituisce una tazza, quindi la caffeina cala ogni settimana.',
  'cups': 'Tazze al giorno', 'coffee_kind': 'Il tuo caffè', 'target': 'Tè al posto del caffè', 'drink': 'Bevanda', 'a': 'Prima bevanda', 'b': 'Seconda bevanda',
  'result': 'Risultato', 'per_cup': 'Caffeina per tazza', 'volume': 'Volume', 'per100': 'mg / 100 ml', 'times': 'volte',
  'bedtime': 'Vado a dormire alle', 'sens': 'Sensibilità alla caffeina', 'sens_names': ['Sensibile', 'Nella media', 'Poco sensibile'],
  'start': 'Avvia', 'pause': 'Pausa', 'resume': 'Riprendi', 'reset': 'Azzera', 'minutes': 'min', 'steeping': 'Tempo di infusione', 'temp_hint': 'Temperatura tipica',
  'add': 'Aggiungi', 'remove': 'Rimuovi', 'time': 'Ora', 'today': 'Oggi', 'empty': 'Ancora nulla.', 'clear': 'Svuota la giornata',
  'profile': 'Profilo', 'profiles': ['Adulto', 'Gravidanza o allattamento'], 'limit': 'Limite giornaliero', 'total': 'Totale di oggi',
  'copy': 'Copia il link', 'copied': 'Copiato', 'embed': 'Incorpora nel tuo sito', 'embed_hide': 'Nascondi il codice', 'share_title': 'Condividi questo strumento',
  'link_note': 'Il link apre lo strumento con le tue scelte.', 'embed_note': 'Copia il codice e incollalo nella tua pagina.',
  'all_tools': 'Tutti gli strumenti', 'more_tools': 'Altri strumenti', 'credit': 'Strumento di Arbata', 'src': 'Fonti e metodo', 'save_note': 'I dati restano solo in questo browser.',
  'note': 'Mostriamo intervalli perché gli studi riportano valori diversi. Informazioni generali, non parere medico.', 'related': 'Può servire anche',
  'cups_word': 'tazze', 'about': 'circa', 'range': 'intervallo', 'mg': 'mg', 'hour_short': 'h',
 },
}

# Kiekvieno įrankio pavadinimas, aprašymas, pasirinkimų tekstai
TXT = {
 'convert': {
  'lt': dict(title='Kava → arbata keitiklis: kiek arbatos atitinka tavo kavą', desc='Įvesk, kiek kavos geri, ir gauk apytikslį arbatos puodelių kiekį su tokiu pačiu kofeino kiekiu.', h1='Kava → arbata keitiklis', lead='Pasirink savo kavą ir arbatą, gausi apytikslį puodelių kiekį, kuris duoda panašų kofeino kiekį.', menu='Kava → arbata keitiklis',
             out_coffee='Tavo kava per dieną', out_tea='Vienas arbatos puodelis', out_eq='arbatos puodelių', note_limit='Bendra dienos riba suaugusiam: 400 mg (EFSA).'),
  'en': dict(title='Coffee to tea converter: how much tea equals your coffee', desc='Enter how much coffee you drink and get the approximate number of tea cups with the same caffeine.', h1='Coffee → tea converter', lead='Pick your coffee and a tea to get the approximate number of cups with similar caffeine.', menu='Coffee → tea converter',
             out_coffee='Your coffee per day', out_tea='One cup of tea', out_eq='cups of tea', note_limit='General daily limit for adults: 400 mg (EFSA).'),
  'it': dict(title='Convertitore caffè → tè: quanto tè equivale al tuo caffè', desc='Inserisci quanto caffè bevi e ottieni il numero approssimativo di tazze di tè con la stessa caffeina.', h1='Convertitore caffè → tè', lead='Scegli il tuo caffè e un tè: ottieni il numero approssimativo di tazze con caffeina simile.', menu='Convertitore caffè → tè',
             out_coffee='Il tuo caffè al giorno', out_tea='Una tazza di tè', out_eq='tazze di tè', note_limit='Limite giornaliero generale per adulti: 400 mg (EFSA).'),
 },
 'compare': {
  'lt': dict(title='Gėrimų kofeino palyginimas: bet kurie du gėrimai', desc='Pasirink bet kuriuos du gėrimus (kava, arbata, kola, energinis) ir palygink kofeino kiekį puodelyje.', h1='Gėrimų palyginimas', lead='Pasirink du gėrimus ir pamatyk lentelę bei grafiką.', menu='Lyginimo įrankis', ratio_pre='Vidutiniškai', ratio_mid='kartų daugiau kofeino nei', ratio_same='Panašus kofeino kiekis'),
  'en': dict(title='Caffeine comparison: any two drinks', desc='Pick any two drinks (coffee, tea, cola, energy drink) and compare the caffeine per cup.', h1='Drink comparison', lead='Pick two drinks to see a table and a chart.', menu='Comparison tool', ratio_pre='On average', ratio_mid='times more caffeine than', ratio_same='Similar caffeine'),
  'it': dict(title='Confronto caffeina: due bevande a scelta', desc='Scegli due bevande qualsiasi (caffè, tè, cola, energy drink) e confronta la caffeina per tazza.', h1='Confronto tra bevande', lead='Scegli due bevande e guarda tabella e grafico.', menu='Strumento di confronto', ratio_pre='In media', ratio_mid='volte più caffeina di', ratio_same='Caffeina simile'),
 },
 'lastcup': {
  'lt': dict(title='Paskutinio puodelio laikas: kada nustoti gerti kofeiną', desc='Įvesk miego laiką, gėrimą ir jautrumą ir gauk apytikslę paskutinio puodelio valandą.', h1='Paskutinio puodelio laikas', lead='Apytikslė valanda, po kurios kofeino likutis iki miego jau nedidelis.', menu='Paskutinio puodelio laikas',
             out_pre='Paskutinis puodelis apie', out_range='Priklausomai nuo organizmo: nuo', out_to='iki', out_any='Šio gėrimo kofeino kiekis mažas, laikas nesvarbus.', method='Skaičiuojama pagal pusėjimo trukmę 3–7 val. (centras 5 val.) ir pasirinktą likutį miegui: 25, 50 arba 100 mg. Tai orientacinė taisyklė, ne tyrimo riba.'),
  'en': dict(title='Last cup time: when to stop drinking caffeine', desc='Enter your bedtime, drink and sensitivity to get an approximate time for your last cup.', h1='Last cup time', lead='An approximate time after which the caffeine left at bedtime is small.', menu='Last cup time',
             out_pre='Last cup around', out_range='Depending on your body: from', out_to='to', out_any='This drink has little caffeine, timing hardly matters.', method='Calculated from a half-life of 3–7 h (centre 5 h) and a chosen remainder at bedtime: 25, 50 or 100 mg. A rule of thumb, not a research threshold.'),
  'it': dict(title='Ora dell\'ultima tazza: quando smettere con la caffeina', desc='Inserisci l\'ora in cui dormi, la bevanda e la sensibilità: ottieni un\'ora approssimativa per l\'ultima tazza.', h1='Ora dell\'ultima tazza', lead='Un\'ora indicativa dopo la quale la caffeina rimasta al momento di dormire è poca.', menu='Ora dell\'ultima tazza',
             out_pre='Ultima tazza verso le', out_range='A seconda del tuo corpo: dalle', out_to='alle', out_any='Questa bevanda ha poca caffeina, l\'orario conta poco.', method='Calcolo con emivita di 3–7 h (centro 5 h) e un residuo scelto al momento di dormire: 25, 50 o 100 mg. È una regola pratica, non una soglia scientifica.'),
 },
 'timer': {
  'lt': dict(title='Arbatos plikymo laikmatis su kofeino įvertinimu', desc='Pasirink arbatą ir plikymo laiką: laikmatis skaičiuoja laiką, o įrankis rodo apytikslį kofeino kiekį.', h1='Plikymo laikmatis', lead='Ilgesnis plikymas dažniausiai atneša daugiau kofeino. Pasirink laiką ir paleisk.', menu='Plikymo laikmatis', est='Apytikslis kofeinas (2 g arbatos)', done='Arbata paruošta!'),
  'en': dict(title='Tea brewing timer with caffeine estimate', desc='Pick a tea and steeping time: the timer counts down and the tool shows the approximate caffeine.', h1='Brewing timer', lead='Longer steeping usually brings more caffeine. Pick a time and start.', menu='Brewing timer', est='Approximate caffeine (2 g of tea)', done='Your tea is ready!'),
  'it': dict(title='Timer di infusione del tè con stima della caffeina', desc='Scegli il tè e il tempo di infusione: il timer conta e lo strumento mostra la caffeina approssimativa.', h1='Timer di infusione', lead='Un\'infusione più lunga di solito porta più caffeina. Scegli il tempo e avvia.', menu='Timer di infusione', est='Caffeina approssimativa (2 g di tè)', done='Il tè è pronto!'),
 },
 'tracker': {
  'lt': dict(title='Dienos kofeino sekiklis ir riba', desc='Pridėk dienos gėrimus ir matyk, kiek kofeino jau išgerta, palyginus su dienos riba. Be registracijos.', h1='Dienos sekiklis ir riba', lead='Pridėk gėrimus ir matyk dienos sumą. Duomenys lieka tavo naršyklėje.', menu='Dienos sekiklis ir riba',
             ok='Žemiau ribos', near='Artėji prie ribos', over='Riba viršyta', pregnancy_note='Nėštumo ir žindymo metu EFSA rekomenduoja ne daugiau kaip 200 mg per dieną.'),
  'en': dict(title='Daily caffeine tracker and limit', desc='Add your drinks and see how much caffeine you have had compared with the daily limit. No sign-up.', h1='Daily tracker and limit', lead='Add drinks and see the day\'s total. Data stays in your browser.', menu='Daily tracker and limit',
             ok='Below the limit', near='Close to the limit', over='Limit exceeded', pregnancy_note='During pregnancy and breastfeeding EFSA suggests no more than 200 mg a day.'),
  'it': dict(title='Diario giornaliero della caffeina e limite', desc='Aggiungi le bevande e guarda quanta caffeina hai assunto rispetto al limite giornaliero. Senza registrazione.', h1='Diario giornaliero e limite', lead='Aggiungi le bevande e vedi il totale del giorno. I dati restano nel tuo browser.', menu='Diario giornaliero e limite',
             ok='Sotto il limite', near='Vicino al limite', over='Limite superato', pregnancy_note='In gravidanza e allattamento l\'EFSA suggerisce al massimo 200 mg al giorno.'),
 },
 'body': {
  'lt': dict(title='Kofeinas organizme: kiek jo lieka per dieną', desc='Įvesk dienos gėrimus ir laiką ir pamatyk apytikslį kofeino kiekį organizme per dieną.', h1='Kofeinas organizme', lead='Pridėk gėrimus su laiku ir pamatyk, kaip kofeino kiekis kyla ir krenta.', menu='Kofeinas organizme',
           peak='Didžiausias kiekis', below='Nukris žemiau 50 mg apie', hours='Valanda', method='Pusėjimo trukmė 3–7 val. (linija – 5 val., juosta – 3 ir 7 val. kraštutinumai). Tai modelis, ne matavimas.', never='Per pasirinktą laiką nenukris'),
  'en': dict(title='Caffeine in the body: how much is left through the day', desc='Enter your drinks and times to see an approximate caffeine level in the body across the day.', h1='Caffeine in the body', lead='Add drinks with times and see how caffeine rises and falls.', menu='Caffeine in the body',
           peak='Peak level', below='Drops below 50 mg around', hours='Hour', method='Half-life 3–7 h (line: 5 h, band: 3 h and 7 h extremes). A model, not a measurement.', never='Does not drop within the chart'),
  'it': dict(title='Caffeina nel corpo: quanta ne resta durante il giorno', desc='Inserisci bevande e orari per vedere un livello approssimativo di caffeina nel corpo durante il giorno.', h1='Caffeina nel corpo', lead='Aggiungi le bevande con l\'orario e guarda come sale e scende la caffeina.', menu='Caffeina nel corpo',
           peak='Livello massimo', below='Scende sotto 50 mg verso le', hours='Ora', method='Emivita 3–7 h (linea: 5 h, fascia: estremi 3 e 7 h). È un modello, non una misura.', never='Non scende entro il grafico'),
 },
}

TEMP_HINT = {'black': '95–100 °C', 'green': '70–80 °C', 'oolong': '85–95 °C', 'white': '75–85 °C', 'puerh': '95–100 °C', 'mate': '70–80 °C'}


def i18n_json(lang, tool):
    d = dict(S[lang])
    d.update(TXT[tool][lang])
    d['temp'] = TEMP_HINT
    return json.dumps(d, ensure_ascii=False).replace('</', '<\\/')


def pages(B):
    """B – build modulis. Grąžina [(failo kelias, html)] visiems įrankiams ir jų įterpiamoms versijoms."""
    out = []
    for tool in ORDER:
        for lang in B.LANGS:
            out.append((B.PATH[tool](lang) + 'index.html', page(B, tool, lang, False)))
            out.append((B.PATH['e_' + tool](lang) + 'index.html', page(B, tool, lang, True)))
    return out


def page(B, tool, lang, embed):
    E = B.E
    c = B.C[lang]
    s = S[lang]
    t = TXT[tool][lang]
    key = ('e_' + tool) if embed else tool
    share = ''
    if not embed:
        share_url = B.BASE + B.PATH[tool](lang)
        share = f'''<section class="share" id="share" aria-labelledby="share-h">
<div class="share-top"><h2 id="share-h">{E(s['share_title'])}</h2>
<button class="btn btn-amber btn-sm" type="button" id="copy-btn" data-copy="{E(s['copy'])}" data-copied="{E(s['copied'])}">{B.svg('link', 18, '1.9')}<span id="copy-label">{E(s['copy'])}</span></button>
<button class="btn btn-outline btn-sm" type="button" id="embed-btn" aria-expanded="false" aria-controls="embed-panel" data-show="{E(s['embed'])}" data-hide="{E(s['embed_hide'])}">{B.svg('code', 18, '1.9')}<span id="embed-label">{E(s['embed'])}</span></button></div>
<div><span class="small">{E(s['link_note'])}</span><label class="sr-only" for="share-url">URL</label><input class="code" id="share-url" type="text" readonly value="{share_url}"></div>
<div id="embed-panel" hidden><span class="small">{E(s['embed_note'])}</span><label class="sr-only" for="embed-code">iframe</label><textarea class="code code-dark" id="embed-code" rows="3" readonly></textarea></div>
</section>'''
        others = [o for o in ORDER if o != tool][:3]
        if tool in ('convert', 'lastcup', 'tracker', 'body', 'compare', 'plan'):
            others = ['cups'] + [o for o in ORDER if o not in (tool, 'cups')][:2]
        links = ''.join(f'<a href="{B.PATH[o](lang)}">{E(TXT[o][lang]["menu"])}</a>' for o in others)
        related = f'<div class="quiet"><span class="fld-label">{E(s["related"])}</span><div class="quiet-links">{links}</div></div>'
    else:
        related = ''
    src = f'<a class="small" href="{B.PATH["calc"](lang)}#src-h" {"target=_blank rel=noopener" if embed else ""}>{E(s["src"])}</a>'
    embed_src = B.BASE + B.PATH['e_' + tool](lang)
    foot = ''
    if embed:
        foot = (f'<div class="embed-foot"><a class="b" href="{B.BASE}{B.PATH[tool](lang)}" target="_blank" rel="noopener">{E(s["credit"])} →</a>'
                f'<a class="m" href="{B.BASE}{B.PATH["tools"](lang)}" target="_blank" rel="noopener">{E(s["more_tools"])}</a></div>')
    main = f'''<main id="main" class="wrap wrap-narrow tool-wrap">
<div><h1>{E(t['h1'])}</h1><p class="lead" style="margin-top:10px">{E(t['lead'])}</p></div>
<div id="tool" data-tool="{tool}" data-embed-src="{E(embed_src)}" data-title="{E(t['h1'])}" data-share="{1 if SHARE[tool] else 0}">
<noscript><p class="small">JavaScript is required.</p></noscript>
<div class="tool-cols" id="tool-body"></div>
<div id="tool-extra"></div>
</div>
<p class="tool-note" style="color:var(--muted)">{E(s['note'])} {src}</p>
{cups_extra(B, lang) if (tool == 'cups' and not embed) else ''}
{share}
{related}
{foot}
</main>
<script type="application/json" id="i18n">{i18n_json(lang, tool)}</script>'''
    scripts = ('data.js', 'tools.js')
    js = ''.join(f'<script src="/assets/{x}" defer></script>' for x in scripts)
    if embed:
        return (B.head(lang, key, t['title'], t['desc'], noindex=True) + '\n<body class="is-embed-tool">\n' + main + '\n' + js + '\n</body>\n</html>\n')
    return B.shell(lang, key, t['title'], t['desc'], main, quiet_footer=True, slim=True, scripts=scripts)


# ---------- Antra partija: mažinimo planas, dienoraštis, arbatos testas ----------
SLUG.update({
    'plan': {'lt': 'mazinimo-planas', 'en': 'switch-plan', 'it': 'piano-di-passaggio'},
    'diary': {'lt': 'atsisakymo-dienorastis', 'en': 'switch-diary', 'it': 'diario-del-passaggio'},
    'quiz': {'lt': 'arbatos-testas', 'en': 'tea-finder', 'it': 'trova-il-tuo-te'},
})
ICON.update({'plan': 'cal', 'diary': 'book', 'quiz': 'spark'})
ORDER += ['plan', 'diary', 'quiz']
SHARE.update({'plan': True, 'diary': False, 'quiz': True})

TXT['plan'] = {
 'lt': dict(title='Kavos keitimo į arbatą planas: dienų planas su kalendoriumi', desc='Įvesk, kiek kavos geri, ir gauk savaičių planą, kaip pereiti prie arbatos. Parsisiųsk į kalendorių arba atsispausdink.', h1='Perėjimo nuo kavos prie arbatos planas', lead='Planas pakeičia kavos puodelius arbata palaipsniui ir stengiasi išlaikyti panašų kofeino kiekį, kad pereiti būtų lengviau.', menu='Mažinimo planas',
            weeks='Trukmė (savaitės)', start='Pradžia', week='Savaitė', coffee='Kava', tea='Arbata', mg='Kofeinas per dieną', ics='Į kalendorių (.ics)', print='Spausdinti / PDF', ev='Kavos keitimas arbata', ev_d='Kava: {c} p. per dieną, arbata: {t} p. per dieną (apie {lo}–{hi} mg kofeino).',
            plan_note='Arbatos puodelių skaičius ribojamas iki 6 per dieną, todėl bendras kofeino kiekis gali mažėti. Tai bendro pobūdžio pavyzdinis planas, ne gydytojo rekomendacija. Jei esi nėščia, žindai ar vartoji vaistus, pasitark su gydytoju.', goal='Tikslas', g_same='Panašus kofeinas', g_less='Mažiau kofeino', g_free='Be kofeino', free='Be kofeino', limit='400 mg dienos riba (EFSA)', bars='Kofeinas per dieną pagal savaitę', ev_d_f='Kava: {c} p. per dieną, arbata ar žolelių gėrimas be kofeino: {f} p. per dieną (apie {lo}–{hi} mg kofeino).',
            g_note='Panašus kofeinas: arbatos puodelių tiek, kad kofeino liktų panašiai. Mažiau kofeino: vienas arbatos puodelis už kiekvieną kavos puodelį. Be kofeino: vietoj kavos rooibos ar žolelių arbata (pasitikrink pakuotę).',
            tips_h='Kas gali padėti', tip_a='Pirmą savaitę pakeisk tik rytinį puodelį', tip_b='Popietės pertraukai', tip_c='Vakarui', tip_d='Jei skauda galvą ar mieguista', tip_e='Daugiau apie planą ir ritualus',
            over='Kai kuriomis savaitėmis viršutinė riba viršija 400 mg: rinkis „Mažiau kofeino“ ar „Be kofeino“.', cups_short='p.'),
 'en': dict(title='Coffee to tea switching plan with calendar export', desc='Enter how much coffee you drink and get a weekly plan for moving to tea. Download to your calendar or print it.', h1='Coffee-to-tea switching plan', lead='The plan swaps coffee cups for tea step by step and tries to keep caffeine roughly similar, so the move is easier.', menu='Switching plan',
            weeks='Length (weeks)', start='Start date', week='Week', coffee='Coffee', tea='Tea', mg='Caffeine per day', ics='Add to calendar (.ics)', print='Print / PDF', ev='Switching coffee to tea', ev_d='Coffee: {c} cups a day, tea: {t} cups a day (about {lo}–{hi} mg caffeine).',
            plan_note='Tea is capped at 6 cups a day, so total caffeine may fall. This is a general example plan, not medical advice. If you are pregnant, breastfeeding or take medication, talk to your doctor.', goal='Goal', g_same='Similar caffeine', g_less='Less caffeine', g_free='Caffeine-free', free='Caffeine-free', limit='400 mg daily limit (EFSA)', bars='Caffeine per day by week', ev_d_f='Coffee: {c} cups a day, caffeine-free tea or herbal drink: {f} cups a day (about {lo}–{hi} mg caffeine).',
            g_note='Similar caffeine: enough tea cups to keep caffeine roughly the same. Less caffeine: one tea cup for each coffee cup removed. Caffeine-free: rooibos or herbal tea instead of coffee (check the pack).',
            tips_h='What can help', tip_a='In week one swap only the morning cup', tip_b='For the afternoon break', tip_c='For the evening', tip_d='If you get a headache or feel sleepy', tip_e='More about the plan and rituals',
            over='In some weeks the upper end is above 400 mg: choose “Less caffeine” or “Caffeine-free”.', cups_short='cups'),
 'it': dict(title='Piano per passare dal caffè al tè con calendario', desc='Inserisci quanto caffè bevi e ottieni un piano settimanale per passare al tè. Scarica nel calendario o stampa.', h1='Piano per passare dal caffè al tè', lead='Il piano sostituisce le tazze di caffè con il tè gradualmente, cercando di mantenere una caffeina simile per rendere il passaggio più facile.', menu='Piano di passaggio',
            weeks='Durata (settimane)', start='Data di inizio', week='Settimana', coffee='Caffè', tea='Tè', mg='Caffeina al giorno', ics='Nel calendario (.ics)', print='Stampa / PDF', ev='Dal caffè al tè', ev_d='Caffè: {c} tazze al giorno, tè: {t} tazze al giorno (circa {lo}–{hi} mg di caffeina).',
            plan_note='Il tè è limitato a 6 tazze al giorno, quindi la caffeina totale può diminuire. È un piano di esempio generale, non un parere medico. In gravidanza, allattamento o se prendi farmaci, parla con il medico.', goal='Obiettivo', g_same='Caffeina simile', g_less='Meno caffeina', g_free='Senza caffeina', free='Senza caffeina', limit='Limite giornaliero 400 mg (EFSA)', bars='Caffeina al giorno per settimana', ev_d_f='Caffè: {c} tazze al giorno, tè o tisana senza caffeina: {f} tazze al giorno (circa {lo}–{hi} mg di caffeina).',
            g_note='Caffeina simile: tante tazze di tè da mantenere la caffeina quasi uguale. Meno caffeina: una tazza di tè per ogni tazza di caffè tolta. Senza caffeina: rooibos o tisana al posto del caffè (controlla la confezione).',
            tips_h='Cosa può aiutare', tip_a='Nella prima settimana sostituisci solo la tazza del mattino', tip_b='Per la pausa del pomeriggio', tip_c='Per la sera', tip_d='Se hai mal di testa o sonnolenza', tip_e='Altro sul piano e sui rituali',
            over='In alcune settimane il valore massimo supera 400 mg: scegli “Meno caffeina” o “Senza caffeina”.', cups_short='taz.'),
}

TXT['diary'] = {
 'lt': dict(title='Atsisakymo dienoraštis: dienos be kavos, savijauta ir pastabos', desc='Kasdien užrašyk kavos ir arbatos puodelius, savijautą ir pastabas. Duomenys lieka tavo naršyklėje.', h1='Atsisakymo dienoraštis', lead='Trumpas įrašas kartą per dieną: kiek išgerta, kaip jautiesi. Matai serijas be kavos ir savo kelią.', menu='Atsisakymo dienoraštis',
            coffee='Kavos puodeliai', tea='Arbatos puodeliai', energy='Energija', symptoms='Kas pasireiškė', sym=['Galvos skausmas', 'Mieguistumas', 'Dirglumas', 'Sunku susikaupti'], note='Pastaba', save='Išsaugoti dienai', streak='Dienų be kavos iš eilės', days='Įrašų', history='Paskutiniai įrašai', export='Kopijuoti kaip tekstą', exported='Nukopijuota', del_='Ištrinti visus įrašus', confirm='Ištrinti visus dienoraščio įrašus?', saved='Išsaugota', lvl=['Labai žema', 'Žema', 'Vidutinė', 'Gera', 'Puiki']),
 'en': dict(title='Switch diary: coffee-free days, how you feel and notes', desc='Log coffee and tea cups, how you feel and notes every day. The data stays in your browser.', h1='Switch diary', lead='A short entry once a day: what you drank and how you feel. See your coffee-free streak and your progress.', menu='Switch diary',
            coffee='Coffee cups', tea='Tea cups', energy='Energy', symptoms='What showed up', sym=['Headache', 'Sleepiness', 'Irritability', 'Hard to focus'], note='Note', save='Save for today', streak='Coffee-free days in a row', days='Entries', history='Latest entries', export='Copy as text', exported='Copied', del_='Delete all entries', confirm='Delete all diary entries?', saved='Saved', lvl=['Very low', 'Low', 'Medium', 'Good', 'Great']),
 'it': dict(title='Diario del passaggio: giorni senza caffè, come stai e note', desc='Ogni giorno annota tazze di caffè e tè, come ti senti e le note. I dati restano nel tuo browser.', h1='Diario del passaggio', lead='Una breve voce al giorno: cosa hai bevuto e come stai. Vedi la serie di giorni senza caffè e i tuoi progressi.', menu='Diario del passaggio',
            coffee='Tazze di caffè', tea='Tazze di tè', energy='Energia', symptoms='Cosa hai notato', sym=['Mal di testa', 'Sonnolenza', 'Irritabilità', 'Difficoltà a concentrarsi'], note='Nota', save='Salva per oggi', streak='Giorni di fila senza caffè', days='Voci', history='Ultime voci', export='Copia come testo', exported='Copiato', del_='Elimina tutte le voci', confirm='Eliminare tutte le voci del diario?', saved='Salvato', lvl=['Molto bassa', 'Bassa', 'Media', 'Buona', 'Ottima']),
}

# Testas: balai nepriklauso nuo kalbos. SC[klausimas][atsakymas] = {arbata: taškai}
SC = [
 [{'matcha': 3, 'mate': 3, 'black': 3, 'puerh': 2, 'green': 1, 'oolong': 1},
  {'green': 3, 'oolong': 3, 'white': 3, 'puerh': 2, 'black': 1, 'mate': 1, 'matcha': 1},
  {'white': 3, 'oolong': 3, 'green': 2, 'puerh': 1, 'black': 1},
  {'oolong': 3, 'puerh': 3, 'matcha': 3, 'green': 2, 'white': 2, 'mate': 2, 'black': 1}],
 [{'green': 2, 'oolong': 2, 'white': 2, 'black': 1, 'puerh': 1, 'mate': 1, 'matcha': 1},
  {'black': 2, 'mate': 2, 'matcha': 2, 'puerh': 2, 'oolong': 1, 'green': 1},
  {'matcha': 3, 'mate': 3, 'black': 3, 'puerh': 2}],
 [{'black': 2, 'matcha': 2, 'mate': 2, 'puerh': 1, 'green': 1},
  {'green': 2, 'oolong': 2, 'puerh': 2, 'mate': 2, 'black': 1, 'matcha': 1, 'white': 1},
  {'white': 3, 'oolong': 2, 'green': 1}],
 [{'black': 3, 'mate': 2, 'puerh': 2},
  {'green': 3, 'white': 2, 'matcha': 2},
  {'oolong': 3, 'white': 3, 'green': 1},
  {'puerh': 3, 'mate': 3, 'black': 1}],
 [{'black': 3, 'matcha': 2, 'puerh': 1, 'mate': 1},
  {'green': 2, 'oolong': 2, 'white': 2, 'puerh': 1, 'mate': 1}],
 [{'black': 3, 'green': 2, 'white': 2, 'mate': 1, 'puerh': 1, 'oolong': 1},
  {'black': 1, 'green': 2, 'oolong': 2, 'white': 2, 'puerh': 2, 'mate': 2, 'matcha': 1},
  {'matcha': 3, 'oolong': 3, 'puerh': 2, 'white': 1}],
]

TXT['quiz'] = {
 'lt': dict(title='Arbatos parinkimo testas: kokia arbata tau vietoj kavos', desc='Šeši klausimai ir gauk tris arbatų rūšis, kurios gali tikti vietoj kavos, bei kodėl.', h1='Kokia arbata tau vietoj kavos?', lead='Atsakyk į šešis klausimus ir gausi tris rūšis su paaiškinimu.', menu='Arbatos parinkimo testas',
            qs=[('Ko labiausiai nori iš arbatos?', ['Stipraus postūmio kaip iš kavos', 'Švelnesnio poveikio nei kava', 'Kažko, ką galima gerti ir vėliau dieną', 'Skonio ir ritualo']),
                ('Kiek kavos geri dabar?', ['1–2 puodelius', '3–4 puodelius', '5 ir daugiau']),
                ('Kada dažniausiai geri kofeiną?', ['Rytais', 'Po pietų', 'Vakare']),
                ('Koks skonis tau artimiausias?', ['Stiprus, tamsus', 'Lengvas, žolinis', 'Saldesnis, gėlių', 'Žemiškas, dūmų']),
                ('Ar geri su pienu?', ['Taip', 'Ne']),
                ('Kiek pastangų esi pasiruošęs?', ['Greitai užpilti', 'Paplikyti 3–5 min.', 'Ritualas, net plakimas'])],
            next='Toliau', back='Atgal', again='Pradėti iš naujo', top='Tau gali tikti', why='Kodėl', because='Sutampa su:', cup='Kofeino puodelyje', q_of='Klausimas', of='iš', note_q='Tai bendra orientacinė rekomendacija pagal rūšis, ne konkretūs produktai.'),
 'en': dict(title='Tea finder quiz: which tea to drink instead of coffee', desc='Six questions and you get three types of tea that may suit you instead of coffee, and why.', h1='Which tea instead of coffee?', lead='Answer six questions and get three types with the reasons.', menu='Tea finder quiz',
            qs=[('What do you want most from tea?', ['A strong boost like coffee', 'Something gentler than coffee', 'Something I can drink later in the day', 'Taste and ritual']),
                ('How much coffee do you drink now?', ['1–2 cups', '3–4 cups', '5 or more']),
                ('When do you usually have caffeine?', ['Mornings', 'Afternoons', 'Evenings']),
                ('Which taste is closest to yours?', ['Strong and dark', 'Light and grassy', 'Sweeter, floral', 'Earthy, smoky']),
                ('Do you drink it with milk?', ['Yes', 'No']),
                ('How much effort are you up for?', ['Just pour water', 'Steep for 3–5 min', 'A ritual, even whisking'])],
            next='Next', back='Back', again='Start again', top='May suit you', why='Why', because='Matches:', cup='Caffeine per cup', q_of='Question', of='of', note_q='A general guide by type of tea, not specific products.'),
 'it': dict(title='Quiz: quale tè bere al posto del caffè', desc='Sei domande e ottieni tre tipi di tè che possono andare bene al posto del caffè, e perché.', h1='Quale tè al posto del caffè?', lead='Rispondi a sei domande e ottieni tre tipi con le ragioni.', menu='Quiz trova il tuo tè',
            qs=[('Cosa vuoi di più dal tè?', ['Una spinta forte come il caffè', 'Qualcosa di più delicato del caffè', 'Qualcosa da bere anche più tardi nella giornata', 'Gusto e rituale']),
                ('Quanto caffè bevi ora?', ['1–2 tazze', '3–4 tazze', '5 o più']),
                ('Quando bevi di solito caffeina?', ['La mattina', 'Il pomeriggio', 'La sera']),
                ('Quale gusto senti più vicino?', ['Forte e scuro', 'Leggero, erbaceo', 'Più dolce, floreale', 'Terroso, affumicato']),
                ('Lo bevi con il latte?', ['Sì', 'No']),
                ('Quanto impegno vuoi metterci?', ['Basta versare l\'acqua', 'Infusione di 3–5 min', 'Un rituale, anche con la frusta'])],
            next='Avanti', back='Indietro', again='Ricomincia', top='Può andarti bene', why='Perché', because='Corrisponde a:', cup='Caffeina per tazza', q_of='Domanda', of='di', note_q='Una guida generale per tipo di tè, non prodotti specifici.'),
}


WD_SLUG = {'lt': 'kavos-abstinencija-kiek-trunka', 'en': 'caffeine-withdrawal-how-long', 'it': 'astinenza-da-caffeina-quanto-dura'}


def _i18n_extra(tool, d, lang=None):
    if tool == 'quiz':
        d['sc'] = SC
    if tool == 'plan' and lang:
        import rituals_gen as RG
        u = lambda i: f'/{lang}/{RG.DIR[lang]}/{RG.SLUG[i][lang]}/'
        d['urls'] = {'a': u('morning'), 'b': u('break'), 'c': u('calm'), 'd': f'/{lang}/blog/{WD_SLUG[lang]}/', 'e': f'/{lang}/{RG.DIR[lang]}/'}
    if tool in ('convert', 'plan') and lang:
        import tealib_gen as TL
        d['zurls'] = {i: f'/{lang}/{TL.DIR[lang]}/{(TL.SG.N[i] if i in TL.SG.N else TL.XT.NAMES[i])["slug"][lang]}/' for i in ('rooibos', 'herbal')}
    return d


_orig_i18n = i18n_json


def i18n_json(lang, tool):  # noqa: F811
    d = dict(S[lang])
    d.update(TXT[tool][lang])
    d['temp'] = TEMP_HINT
    _i18n_extra(tool, d, lang)
    return json.dumps(d, ensure_ascii=False).replace('</', '<\\/')


# ---------- Trečia partija: „Kaip jausiesi po N-to puodelio“ (raktas `cups`) ----------
SLUG['cups'] = {'lt': 'kelintas-puodelis', 'en': 'nth-cup', 'it': 'quante-tazze'}
ICON['cups'] = 'chart'
ORDER.append('cups')
SHARE['cups'] = True

CUPS_SRC = {
    'efsa': ('EFSA 2015', 'https://doi.org/10.2903/j.efsa.2015.4102', 'EFSA NDA Panel. Scientific Opinion on the safety of caffeine. EFSA Journal 2015;13(5):4102 (200 mg vienu kartu, 400 mg per dieną, 200 mg nėštumo metu; santrauka: EUFIC)'),
    'mayo': ('Mayo Clinic', 'https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/caffeine/art-20045678', 'Mayo Clinic Staff. Caffeine: How much is too much? (2025)'),
    'fda': ('FDA', 'https://www.fda.gov/consumers/consumer-updates/spilling-beans-how-much-caffeine-too-much', 'FDA. Spilling the Beans: How Much Caffeine Is Too Much?'),
    'drake': ('Drake 2013', 'https://doi.org/10.5664/jcsm.3170', 'Drake C, et al. Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed. J Clin Sleep Med 2013;9(11):1195–1200'),
    'gardiner23': ('Gardiner 2023', 'https://doi.org/10.1016/j.smrv.2023.101764', 'Gardiner C, et al. The effect of caffeine on subsequent sleep: a systematic review and meta-analysis. Sleep Med Rev 2023;69:101764 (abstract)'),
    'gardiner25': ('Gardiner 2025', 'https://doi.org/10.1093/sleep/zsae230', 'Gardiner CL, et al. Dose and timing effects of caffeine on subsequent sleep. Sleep 2025;48(4):zsae230'),
    'chang': ('Chang 2025', 'https://doi.org/10.1016/j.sleep.2025.106874', 'Chang YH, et al. Age- and dose-specific effects of caffeine on sleep: a meta-analysis. Sleep Med 2025;136:106874 (abstract)'),
    'clark': ('Clark & Landolt 2017', 'https://doi.org/10.1016/j.smrv.2016.01.006', 'Clark I, Landolt HP. Coffee, caffeine, and sleep. Sleep Med Rev 2017;31:70–78 (abstract)'),
    'mccusker': ('McCusker 2006', 'https://pubmed.ncbi.nlm.nih.gov/17132260/', 'McCusker RR, et al. Caffeine content of decaffeinated coffee. J Anal Toxicol 2006;30(8):611–613'),
}

TXT['cups'] = {
 'lt': dict(title='Kaip jausiesi po N-to puodelio: kofeino kiekis ir ką rodo šaltiniai', desc='Pasirink gėrimą ir puodelių skaičių: gausi kofeino kiekį mg, dalį dienos ribos, šaltiniais paremtą poveikio aprašymą ir pakaitalus su mažiau kofeino.', h1='Kaip jausiesi po N-to puodelio', lead='Pasirink gėrimą ir puodelių skaičių. Pamatysi kofeino kiekį, dalį dienos ribos ir ką apie tokius kiekius sako EFSA, Mayo Clinic bei FDA.', menu='Kaip jausiesi po N-to puodelio',
  cups_l='Puodelių skaičius', preg_chk='Esu nėščia (riba 200 mg per dieną)', wt_chk='Skaičiuoti tiksliau pagal svorį', wt_l='Svoris (kg)', sleep_chk='Rodyti pastabą apie miegą', last_l='Paskutinio puodelio laikas', bed_l='Einu miegoti',
  out_total='Kofeino iš viso', typ_pre='Tipinis kiekis', limit_l='Dienos riba', preg_short='nėštumas', mgkg='Kofeino kiekis kūno svoriui', mgkg_note='EFSA: 200 mg suaugusiam atitinka apie 3 mg/kg.',
  b0='Šiame gėrime kofeino nėra, todėl kofeino poveikio nesitikima.',
  b1='Iki 200 mg vienu kartu EFSA suaugusiems nelaiko keliančia rūpesčių. Vėlai dienos metu ir jautresniems žmonėms toks kiekis gali paveikti miegą.',
  b2='Kai kuriems žmonėms tokiu kiekiu gali pasireikšti nerimastingumas, greitas širdies plakimas, skrandžio sutrikimas ar nemiga. Iki 400 mg per dieną EFSA, FDA ir Mayo Clinic suaugusiems nelaiko keliančia rūpesčių.',
  b2_once='Jei visa tai išgeriama vienu kartu, tai viršija EFSA 200 mg vienkartinės dozės reikšmę.',
  hi_over='Viršutinis įvertis ({x} mg) jau viršija 400 mg.',
  b3='Tai viršija 400 mg dienos ribą suaugusiems (EFSA, FDA, Mayo Clinic). Tie patys poveikiai gali būti stipresni: nerimastingumas, greitas ar nereguliarus širdies plakimas, drebulys, skrandžio sutrikimas, nemiga. Jei simptomai stiprūs, kreipkis į gydytoją.',
  b4='FDA nurodo, kad toksinis poveikis (pavyzdžiui, traukuliai) galimas greitai suvartojus apie 1 200 mg kofeino.',
  preg_over='Nėštumo metu EFSA nurodo ne daugiau kaip 200 mg per dieną, todėl šis kiekis ją viršija. Pasitark su gydytoju.',
  preg_ok='Nėštumo metu EFSA nurodo ne daugiau kaip 200 mg per dieną; dėl savo atvejo pasitark su gydytoju.',
  decaf_note='Kava be kofeino vis tiek gali turėti keletą mg kofeino (FDA: apie 2–15 mg 237 ml puodelyje).',
  sleep_h='Miegas.', sleep_gap='Nuo paskutinio puodelio iki miego praeina apie {h} val.', sleep_rem='Pagal modelį (pusėjimo trukmė 3–7 val.) iki miego organizme gali likti apie {a}–{b} mg, jei visas kiekis išgertas paskutinio puodelio metu. Tai modelis, ne matavimas.',
  sleep_res='Tyrimuose apie 400 mg kofeino, išgerti net likus 6 val. iki miego, sutrumpino miegą daugiau nei valanda; metaanalizėse vidutinis sutrumpėjimas buvo apie 35–45 min. O 100 mg vienoje tyrimo grupėje miego reikšmingai nepakeitė. Žmonės poveikį jaučia nevienodai.',
  l_lastcup='Apskaičiuok paskutinį puodelį', l_body='Kofeinas organizme',
  swap_h='Tas pats ritualas su mažiau kofeino', l_convert='Kava → arbata keitiklis',
  safety='Jei jauti spaudimą krūtinėje, labai greitą ar netvarkingą širdies plakimą, alpsti ar jautiesi labai blogai, kreipkis medicininės pagalbos. Bendra informacija, ne medicininis patarimas.',
  indiv='Žmonės reaguoja skirtingai: svarbu svoris, vaistai, ligos, genetika ir tai, ar kofeino geri kasdien. Nėščios, žindančios, sergančios širdies ligomis ar nerimo sutrikimais ir vartojančios vaistus turėtų pasitarti su gydytoju.',
  h_what='Kas nutinka išgėrus kelis puodelius kavos?', p_what='Atsakymas priklauso nuo kiekio, laiko ir paties žmogaus. Pagal mūsų duomenis puodelis (237 ml) filtruotos kavos turi apie 80–107 mg kofeino, todėl 4 puodeliai – apie 320–430 mg, t. y. ties 400 mg riba, kurią EFSA, FDA ir Mayo Clinic laiko nekeliančia rūpesčių daugumai suaugusiųjų. Nėštumo metu riba yra 200 mg per dieną.',
  h_faq='Dažni klausimai', h_src='Šaltiniai',
  faq=[('Kiek puodelių kavos viršija dienos ribą?', 'Pagal mūsų duomenis (filtruota kava, 237 ml, 80–107 mg): 3 puodeliai – apie 240–320 mg, 4 puodeliai – apie 320–430 mg, 5 puodeliai – apie 400–540 mg. Todėl 5 ir daugiau puodelių viršija 400 mg ribą, o 4 gali ją pasiekti. Tikslus kiekis priklauso nuo kavos ir plikymo būdo.'),
       ('Ar kava po pietų gali sutrikdyti miegą?', 'Kontroliuojamuose tyrimuose didesnės kofeino dozės (apie 400 mg), išgertos net likus 6 val. iki miego, sutrumpino miegą. Mažesnė, 100 mg, dozė vienoje tyrimo grupėje miego reikšmingai nepakeitė. Poveikis priklauso nuo dozės, laiko ir žmogaus; vieni jį jaučia, kiti ne.'),
       ('Ar tai medicininė rekomendacija?', 'Ne. Tai bendra informacija iš EFSA, Mayo Clinic ir FDA. Jei kofeinas kelia nerimą, širdies plakimo ar miego problemų, arba esi nėščia, žindai ar vartoji vaistus, pasitark su gydytoju.')]),
 'en': dict(title='How you may feel after the Nth cup: caffeine amount and what the sources say', desc='Pick a drink and a number of cups: get the caffeine in mg, the share of the daily limit, a sourced description of what such amounts may do, and lower-caffeine swaps.', h1='How you may feel after the Nth cup', lead='Pick a drink and a number of cups. See the caffeine amount, the share of the daily limit and what EFSA, Mayo Clinic and the FDA say about such amounts.', menu='How you may feel after the Nth cup',
  cups_l='Number of cups', preg_chk='I am pregnant (limit 200 mg a day)', wt_chk='Use my weight for a closer estimate', wt_l='Weight (kg)', sleep_chk='Show a sleep note', last_l='Time of the last cup', bed_l='Bedtime',
  out_total='Total caffeine', typ_pre='Typical amount', limit_l='Daily limit', preg_short='pregnancy', mgkg='Caffeine per body weight', mgkg_note='EFSA: 200 mg for an adult corresponds to about 3 mg/kg.',
  b0='This drink has no caffeine, so caffeine effects are not expected.',
  b1='Up to 200 mg in one go is not considered a safety concern for adults by EFSA. Later in the day, and in more sensitive people, this amount may affect sleep.',
  b2='In some people this amount may cause restlessness, a fast heartbeat, an upset stomach or trouble sleeping. Up to 400 mg a day is not considered a safety concern for adults by EFSA, the FDA and Mayo Clinic.',
  b2_once='If it is all taken at once, it is above the EFSA single-dose value of 200 mg.',
  hi_over='The upper estimate ({x} mg) is already above 400 mg.',
  b3='This is above the 400 mg daily limit for adults (EFSA, FDA, Mayo Clinic). The same effects may be stronger: restlessness, a fast or irregular heartbeat, tremor, an upset stomach, trouble sleeping. If symptoms are strong, see a doctor.',
  b4='The FDA says toxic effects (for example seizures) are possible when about 1,200 mg of caffeine is consumed quickly.',
  preg_over='During pregnancy EFSA advises no more than 200 mg a day, so this is above it. Talk to your doctor.',
  preg_ok='During pregnancy EFSA advises no more than 200 mg a day; talk to your doctor about your own case.',
  decaf_note='Decaf coffee can still contain a few mg of caffeine (FDA: about 2–15 mg in a 237 ml cup).',
  sleep_h='Sleep.', sleep_gap='About {h} h pass between your last cup and bedtime.', sleep_rem='By the model (half-life 3–7 h), about {a}–{b} mg may be left at bedtime if all the caffeine was taken at the time of the last cup. A model, not a measurement.',
  sleep_res='In studies, about 400 mg of caffeine taken even 6 hours before bed shortened sleep by more than an hour; in meta-analyses the average reduction was about 35–45 minutes. 100 mg did not significantly change sleep in one study group. People feel the effect differently.',
  l_lastcup='Work out your last cup', l_body='Caffeine in the body',
  swap_h='The same ritual with less caffeine', l_convert='Coffee → tea converter',
  safety='If you feel chest pressure, a very fast or irregular heartbeat, faint, or feel very unwell, seek medical help. General information, not medical advice.',
  indiv='People respond differently: weight, medication, health conditions, genetics and whether you drink caffeine daily all matter. If you are pregnant, breastfeeding, have a heart condition or an anxiety disorder, or take medication, talk to a doctor.',
  h_what='What happens after several cups of coffee?', p_what='It depends on the amount, the timing and the person. By our data a 237 ml cup of filter coffee has about 80–107 mg of caffeine, so 4 cups is about 320–430 mg, right around the 400 mg level that EFSA, the FDA and Mayo Clinic consider not a safety concern for most adults. During pregnancy the limit is 200 mg a day.',
  h_faq='Frequently asked questions', h_src='Sources',
  faq=[('How many cups of coffee go over the daily limit?', 'By our data (filter coffee, 237 ml, 80–107 mg): 3 cups are about 240–320 mg, 4 cups about 320–430 mg and 5 cups about 400–540 mg. So 5 or more cups go over 400 mg and 4 can reach it. The exact amount depends on the coffee and how it is brewed.'),
       ('Can coffee after lunch affect sleep?', 'In controlled studies, larger caffeine doses (about 400 mg) taken even 6 hours before bed shortened sleep. A 100 mg dose did not significantly change sleep in one study group. The effect depends on dose, timing and the person; some feel it, others do not.'),
       ('Is this medical advice?', 'No. It is general information from EFSA, Mayo Clinic and the FDA. If caffeine causes anxiety, a racing heart or sleep problems, or you are pregnant, breastfeeding or on medication, talk to a doctor.')]),
 'it': dict(title='Come ti senti dopo la N-esima tazza: quantità di caffeina e cosa dicono le fonti', desc='Scegli una bevanda e il numero di tazze: ottieni la caffeina in mg, la quota del limite giornaliero, una descrizione con fonti degli effetti possibili e alternative con meno caffeina.', h1='Come ti senti dopo la N-esima tazza', lead='Scegli una bevanda e il numero di tazze. Vedi la quantità di caffeina, la quota del limite giornaliero e cosa dicono EFSA, Mayo Clinic e FDA su queste quantità.', menu='Come ti senti dopo la N-esima tazza',
  cups_l='Numero di tazze', preg_chk='Sono in gravidanza (limite 200 mg al giorno)', wt_chk='Usa il mio peso per una stima più precisa', wt_l='Peso (kg)', sleep_chk='Mostra una nota sul sonno', last_l='Ora dell\'ultima tazza', bed_l='Vado a dormire',
  out_total='Caffeina totale', typ_pre='Quantità tipica', limit_l='Limite giornaliero', preg_short='gravidanza', mgkg='Caffeina per peso corporeo', mgkg_note='EFSA: 200 mg per un adulto corrispondono a circa 3 mg/kg.',
  b0='Questa bevanda non contiene caffeina, quindi non si attendono effetti della caffeina.',
  b1='Fino a 200 mg in una volta l\'EFSA non li considera un problema di sicurezza per gli adulti. Più tardi nella giornata, e nelle persone più sensibili, questa quantità può influire sul sonno.',
  b2='In alcune persone questa quantità può causare agitazione, battito accelerato, mal di stomaco o difficoltà a dormire. Fino a 400 mg al giorno EFSA, FDA e Mayo Clinic non li considerano un problema per gli adulti.',
  b2_once='Se viene assunta tutta in una volta, supera il valore EFSA di 200 mg per dose singola.',
  hi_over='La stima massima ({x} mg) supera già i 400 mg.',
  b3='Supera il limite giornaliero di 400 mg per gli adulti (EFSA, FDA, Mayo Clinic). Gli stessi effetti possono essere più forti: agitazione, battito rapido o irregolare, tremore, mal di stomaco, difficoltà a dormire. Se i sintomi sono forti, rivolgiti a un medico.',
  b4='La FDA indica che effetti tossici (per esempio convulsioni) sono possibili quando si assumono rapidamente circa 1.200 mg di caffeina.',
  preg_over='In gravidanza l\'EFSA indica al massimo 200 mg al giorno, quindi questa quantità la supera. Parlane con il medico.',
  preg_ok='In gravidanza l\'EFSA indica al massimo 200 mg al giorno; per il tuo caso parlane con il medico.',
  decaf_note='Anche il caffè decaffeinato può contenere qualche mg di caffeina (FDA: circa 2–15 mg in una tazza da 237 ml).',
  sleep_h='Sonno.', sleep_gap='Tra l\'ultima tazza e il momento di dormire passano circa {h} h.', sleep_rem='Secondo il modello (emivita 3–7 h) al momento di dormire possono restare circa {a}–{b} mg, se tutta la caffeina è stata assunta all\'ora dell\'ultima tazza. Un modello, non una misura.',
  sleep_res='Negli studi circa 400 mg di caffeina assunti anche 6 ore prima di dormire hanno accorciato il sonno di più di un\'ora; nelle metanalisi la riduzione media è stata di circa 35–45 minuti. 100 mg non hanno modificato in modo significativo il sonno in un gruppo di studio. Le persone sentono l\'effetto in modo diverso.',
  l_lastcup='Calcola l\'ultima tazza', l_body='Caffeina nel corpo',
  swap_h='Lo stesso rituale con meno caffeina', l_convert='Convertitore caffè → tè',
  safety='Se senti oppressione al petto, battito molto rapido o irregolare, stai per svenire o stai molto male, chiedi aiuto medico. Informazioni generali, non un parere medico.',
  indiv='Le persone reagiscono in modo diverso: contano peso, farmaci, malattie, genetica e se bevi caffeina ogni giorno. In gravidanza, allattamento, con malattie cardiache o disturbi d\'ansia, o se prendi farmaci, parla con un medico.',
  h_what='Cosa succede dopo diverse tazze di caffè?', p_what='Dipende dalla quantità, dall\'orario e dalla persona. Secondo i nostri dati una tazza da 237 ml di caffè filtro contiene circa 80–107 mg di caffeina, quindi 4 tazze sono circa 320–430 mg, intorno ai 400 mg che EFSA, FDA e Mayo Clinic non considerano un problema per la maggior parte degli adulti. In gravidanza il limite è 200 mg al giorno.',
  h_faq='Domande frequenti', h_src='Fonti',
  faq=[('Quante tazze di caffè superano il limite giornaliero?', 'Secondo i nostri dati (caffè filtro, 237 ml, 80–107 mg): 3 tazze sono circa 240–320 mg, 4 tazze circa 320–430 mg e 5 tazze circa 400–540 mg. Quindi 5 o più tazze superano i 400 mg e 4 possono raggiungerli. La quantità esatta dipende dal caffè e dalla preparazione.'),
       ('Il caffè dopo pranzo può influire sul sonno?', 'Negli studi controllati dosi più alte di caffeina (circa 400 mg), assunte anche 6 ore prima di dormire, hanno accorciato il sonno. Una dose di 100 mg non ha modificato in modo significativo il sonno in un gruppo di studio. L\'effetto dipende da dose, orario e persona; alcuni lo sentono, altri no.'),
       ('È un consiglio medico?', 'No. Sono informazioni generali di EFSA, Mayo Clinic e FDA. Se la caffeina ti causa ansia, battito accelerato o problemi di sonno, o sei in gravidanza, allatti o prendi farmaci, parla con un medico.')]),
}


TXT['cups']['lt'].update(hl0='Be kofeino', hl1='Iki 200 mg: EFSA vienkartinės ribos ribose', hl2='200–400 mg: artėji prie dienos ribos', hl3='Virš 400 mg dienos ribos', hlp='Virš nėštumo ribos (200 mg per dieną)',
  opt_more='Daugiau parinkčių: nėštumas, svoris, miegas', det_what='Ką tai reiškia', det_src='Šaltiniai ir saugumas', src_l='Šaltiniai')
TXT['cups']['en'].update(hl0='No caffeine', hl1='Up to 200 mg: within the EFSA single-dose value', hl2='200–400 mg: nearing the daily limit', hl3='Above the 400 mg daily limit', hlp='Above the pregnancy limit (200 mg a day)',
  opt_more='More options: pregnancy, weight, sleep', det_what='What this means', det_src='Sources and safety', src_l='Sources')
TXT['cups']['it'].update(hl0='Senza caffeina', hl1='Fino a 200 mg: entro il valore EFSA per dose singola', hl2='200–400 mg: ti avvicini al limite giornaliero', hl3='Oltre il limite giornaliero di 400 mg', hlp='Oltre il limite in gravidanza (200 mg al giorno)',
  opt_more='Altre opzioni: gravidanza, peso, sonno', det_what='Cosa significa', det_src='Fonti e sicurezza', src_l='Fonti')

_TOOLS_DIR = {'lt': 'irankiai', 'en': 'tools', 'it': 'strumenti'}
_prev_extra = _i18n_extra


def _i18n_extra(tool, d, lang=None):  # noqa: F811
    d = _prev_extra(tool, d, lang)
    if tool == 'cups' and lang:
        import tealib_gen as TL
        tl = lambda i: f'/{lang}/{TL.DIR[lang]}/{(TL.SG.N[i] if i in TL.SG.N else TL.XT.NAMES[i])["slug"][lang]}/'
        tu = lambda k: f'/{lang}/{_TOOLS_DIR[lang]}/{SLUG[k][lang]}/'
        d['urls'] = {'green': tl('green'), 'white': tl('white'), 'rooibos': tl('rooibos'), 'herbal': tl('herbal'),
                     'convert': tu('convert'), 'lastcup': tu('lastcup'), 'body': tu('body')}
        d['srcs'] = {k: [v[0], v[1]] for k, v in CUPS_SRC.items()}
    return d


def cups_extra(B, lang):
    """Tekstas po įrankiu: trumpas atsakymas, DUK su JSON-LD, šaltiniai."""
    E = B.E
    t = TXT['cups'][lang]
    faq = ''.join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in t['faq'])
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}, ensure_ascii=False).replace('</', '<\\/')
    src = ''.join(f'<li><a href="{E(v[1])}" target="_blank" rel="noopener">{E(v[2])}</a></li>' for v in CUPS_SRC.values())
    return (f'<section class="seo-sec"><h2>{E(t["h_what"])}</h2><p>{E(t["p_what"])}</p></section>'
            f'<section class="seo-sec"><h2>{E(t["h_faq"])}</h2>{faq}</section>'
            f'<section class="seo-sec" id="src-cups"><h2>{E(t["h_src"])}</h2><ul class="srclist">{src}</ul></section>'
            f'<script type="application/ld+json">{ld}</script>')
