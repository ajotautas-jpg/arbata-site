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
            plan_note='Arbatos puodelių skaičius ribojamas iki 6 per dieną, todėl bendras kofeino kiekis gali mažėti. Tai bendro pobūdžio pavyzdinis planas, ne gydytojo rekomendacija. Jei esi nėščia, žindai ar vartoji vaistus, pasitark su gydytoju.', cups_short='p.'),
 'en': dict(title='Coffee to tea switching plan with calendar export', desc='Enter how much coffee you drink and get a weekly plan for moving to tea. Download to your calendar or print it.', h1='Coffee-to-tea switching plan', lead='The plan swaps coffee cups for tea step by step and tries to keep caffeine roughly similar, so the move is easier.', menu='Switching plan',
            weeks='Length (weeks)', start='Start date', week='Week', coffee='Coffee', tea='Tea', mg='Caffeine per day', ics='Add to calendar (.ics)', print='Print / PDF', ev='Switching coffee to tea', ev_d='Coffee: {c} cups a day, tea: {t} cups a day (about {lo}–{hi} mg caffeine).',
            plan_note='Tea is capped at 6 cups a day, so total caffeine may fall. This is a general example plan, not medical advice. If you are pregnant, breastfeeding or take medication, talk to your doctor.', cups_short='cups'),
 'it': dict(title='Piano per passare dal caffè al tè con calendario', desc='Inserisci quanto caffè bevi e ottieni un piano settimanale per passare al tè. Scarica nel calendario o stampa.', h1='Piano per passare dal caffè al tè', lead='Il piano sostituisce le tazze di caffè con il tè gradualmente, cercando di mantenere una caffeina simile per rendere il passaggio più facile.', menu='Piano di passaggio',
            weeks='Durata (settimane)', start='Data di inizio', week='Settimana', coffee='Caffè', tea='Tè', mg='Caffeina al giorno', ics='Nel calendario (.ics)', print='Stampa / PDF', ev='Dal caffè al tè', ev_d='Caffè: {c} tazze al giorno, tè: {t} tazze al giorno (circa {lo}–{hi} mg di caffeina).',
            plan_note='Il tè è limitato a 6 tazze al giorno, quindi la caffeina totale può diminuire. È un piano di esempio generale, non un parere medico. In gravidanza, allattamento o se prendi farmaci, parla con il medico.', cups_short='taz.'),
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


def _i18n_extra(tool, d):
    if tool == 'quiz':
        d['sc'] = SC
    return d


_orig_i18n = i18n_json


def i18n_json(lang, tool):  # noqa: F811
    d = dict(S[lang])
    d.update(TXT[tool][lang])
    d['temp'] = TEMP_HINT
    _i18n_extra(tool, d)
    return json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
