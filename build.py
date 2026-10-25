#!/usr/bin/env python3
"""Sugeneruoja statinę Arbata svetainę (LT / EN / IT) į ./dist"""
import html, os, shutil

BASE = 'https://arbata.pajusk.lt'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'dist')
LANGS = ['lt', 'en', 'it']
LOCALE = {'lt': 'lt_LT', 'en': 'en_US', 'it': 'it_IT'}
TOOLS_DIR = {'lt': 'irankiai', 'en': 'tools', 'it': 'strumenti'}
CALC = {'lt': 'kofeino-skaiciuokle', 'en': 'caffeine-calculator', 'it': 'calcolatore-caffeina'}
EMBED_DIR = {'lt': 'ideti', 'en': 'embed', 'it': 'incorpora'}
PRIV = {'lt': 'privatumas', 'en': 'privacy', 'it': 'privacy'}

PATH = {
    'home': lambda l: f'/{l}/',
    'tools': lambda l: f'/{l}/{TOOLS_DIR[l]}/',
    'calc': lambda l: f'/{l}/{TOOLS_DIR[l]}/{CALC[l]}/',
    'embed': lambda l: f'/{l}/{EMBED_DIR[l]}/{CALC[l]}/',
    'privacy': lambda l: f'/{l}/{PRIV[l]}/',
}
import tools_gen as TG
for _k, _sl in TG.SLUG.items():
    PATH[_k] = (lambda k: lambda l: f'/{l}/{TOOLS_DIR[l]}/{TG.SLUG[k][l]}/')(_k)
    PATH['e_' + _k] = (lambda k: lambda l: f'/{l}/{EMBED_DIR[l]}/{TG.SLUG[k][l]}/')(_k)
import seo_gen as _SG0
_SG0.register(__import__('sys').modules[__name__])
LANGS_OF = {}   # puslapio raktas -> kalbos, kuriomis jis egzistuoja (nenurodyta = visos)


def langs_of(key):
    return LANGS_OF.get(key, LANGS)


def lang_url(key, l):
    return PATH[key](l) if l in langs_of(key) else PATH['blog'](l) if key.startswith('b_') else PATH['home'](l)


import blog_gen as _BG
_BG.register(__import__('sys').modules[__name__])
import brands_gen as _BR
_BR.register(__import__('sys').modules[__name__])
import tealib_gen as _TL
_TL.register(__import__('sys').modules[__name__])
import rituals_gen as _RG
_RG.register(__import__('sys').modules[__name__])

E = lambda s: html.escape(s, quote=True)

ICONS = {
    'book': 'M4 5a2 2 0 012-2h5v16H6a2 2 0 00-2 2zM20 5a2 2 0 00-2-2h-5v16h5a2 2 0 012 2z',
    'leaf': 'M5 19c0-8 6-14 14-14 0 8-6 14-14 14zM5 19l8-8',
    'cup': 'M4 8h13v5a5 5 0 01-5 5H9a5 5 0 01-5-5zM17 9h1.5a2.5 2.5 0 010 5H17M7 3v2M11 3v2',
    'heart': 'M12 20s-7-4.5-7-10a4 4 0 017-2.5A4 4 0 0119 10c0 5.5-7 10-7 10z',
    'globe': 'M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18',
    'gear': 'M5 10h11v6a4 4 0 01-4 4H9a4 4 0 01-4-4zM16 12h2a2 2 0 010 4h-2M10 3c0 2 2 2 2 4',
    'calc': 'M6 3h12v18H6zM9 7h6M9 12h2M13 12h2M9 16h2M13 16h2',
    'cal': 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4',
    'spark': 'M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z',
    'compare': 'M8 4L4 8l4 4M4 8h13M16 20l4-4-4-4M20 16H7',
    'chart': 'M4 20V4M4 20h16M8 16l4-5 3 3 5-7',
    'tag': 'M3 12V4h8l10 10-8 8zM7.5 8.5h.01',
    'bars': 'M4 20V10M10 20V4M16 20v-7M22 20H2',
    'moon': 'M20 14A8 8 0 019.5 4 8 8 0 1020 14z',
    'timer': 'M9 3h6M12 9v4l3 2M12 6a8 8 0 100 16 8 8 0 000-16z',
    'code': 'M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14',
    'info': 'M12 3a9 9 0 100 18 9 9 0 000-18zM12 11v6M12 7.5v.01',
    'link': 'M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1',
}


def svg(name, size=24, sw='1.7'):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'<path d="{ICONS[name]}"/></svg>')


LEAF_LOGO = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F5F6F0" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-14 14-14 0 8-6 14-14 14zM5 19l8-8"/></svg>')

# --------------------------------------------------------------------------------------
# TEKSTAI
# --------------------------------------------------------------------------------------
C = {
 'lt': {
  'skip': 'Pereiti prie turinio',
  'nav_tools': 'Įrankiai', 'nav_blog': 'Blogas', 'nav_guides': 'Gidai', 'nav_lib': 'Biblioteka', 'nav_rit': 'Ritualai', 'nav_brands': 'Gamintojai', 'nav_kit': 'Starter rinkinys',
  'cta_list': 'Prisijungti prie sąrašo', 'all_tools': 'Visi įrankiai',
  'soon': 'Netrukus', 'open': 'Atidaryti',
  'home_title': 'Arbata: mesk kavą, pasilik energiją',
  'home_desc': 'Gidai, įrankiai ir rekomendacijos, kaip pereiti nuo kavos prie arbatos be galvos skausmo. Pradėk nuo kofeino skaičiuoklės.',
  'kicker': 'Pagalba tiems, kas nori mažiau kavos',
  'h1': 'Mesk kavą. Pasilik energiją.',
  'sub': 'Gidai, įrankiai ir sąžiningos rekomendacijos, kaip pereiti nuo kavos prie arbatos be galvos skausmo.',
  'cta1': 'Prisijungti prie sąrašo', 'cta2': 'Paskaičiuoti kofeiną',
  'note': 'Įrankiai nemokami ir veikia be registracijos.',
  'calc_title': 'Kofeino skaičiuoklė', 'kind_label': 'Kavos rūšis', 'espresso': 'Espresas', 'filter': 'Filtrinė kava',
  'per_day': 'Kavos per dieną', 'total': 'Kofeino per dieną', 'dec': 'Mažiau', 'inc': 'Daugiau',
  'eq_pre': 'Tai apie ', 'eq_post': ' puod. yerba mate arbatos',
  'calc_note': 'Vidurkiai: espresas ~64 mg, filtrinė ~95 mg, mate ~80 mg. Realus kiekis priklauso nuo paruošimo.',
  'trust': [
    ('Skaičiai be pagražinimo', 'Kofeino kiekiai pateikiami kaip apytiksliai, su paaiškinimu, nuo ko jie priklauso.'),
    ('Paprasta ir aišku', 'Trumpi gidai ir įrankiai, kuriuos galima pritaikyti jau šiandien.'),
    ('Reklama pažymėta', 'Partnerių nuorodos ir reklama visada aiškiai nurodomos.'),
  ],
  'pillars_title': 'Viskas apie perėjimą vienoje vietoje', 'pillars_sub': 'Nuo pirmos dienos be kavos iki mėgstamiausios arbatos. Šiuo metu ruošiame šiuos skyrius.',
  'pillars': [
    ('book', 'Perėjimo gidai', 'Savaitė po savaitės: kaip sumažinti kavą ir ištverti pirmąsias dienas.'),
    ('leaf', 'Arbatų biblioteka', 'Kofeino kiekiai, skoniai ir virimas: nuo matcha iki stiprios juodosios.'),
    ('cup', 'Receptai ir ritualai', 'Cold brew arbata, latte alternatyvos ir ryto rutinos, kurios pakeičia kavos pertrauką.'),
    ('heart', 'Sveikata ir energija', 'Miegas, kofeino laikas ir ramesnė energija, be medicininių pažadų.'),
    ('globe', 'Istorijos ir kelionės', 'Skaitytojų patirtys ir arbatos kelionės: nuo arbatinių iki plantacijų.'),
    ('gear', 'Rekomenduojami daiktai', 'Arbatinukai, svarstyklės, termosai ir knygos. Partnerių nuorodos bus aiškiai pažymėtos.'),
  ],
  'tools_title': 'Įrankiai, kurie tikrai padeda', 'tools_sub': 'Paprasti, greiti ir nemokami.',
  'shop_kicker': 'Kai būsi pasiruošęs', 'shop_title': 'Starter rinkinys perėjimui',
  'shop_text': 'Keturios daugiau kofeino turinčios arbatos, virimo kortelė ir 14 dienų planas.',
  'shop_price': 'Kaina bus paskelbta netrukus', 'shop_cta': 'Pranešti apie startą',
  'shop_note': 'Kai kuriose rekomendacijose bus partnerių nuorodos; jos visada bus pažymėtos.', 'pouch': 'Pirmos partijos ruošiamos',
  'nl_title': 'Vienas laiškas, kai viskas bus paruošta', 'nl_text': 'Pranešime, kai bus paruoštas 14 dienų planas ir kiti įrankiai.',
  'email': 'El. paštas', 'email_ph': 'tavo@pastas.lt', 'subscribe': 'Prenumeruoti',
  'consent': 'Sutinku, kad mano el. paštas būtų naudojamas naujienoms apie Arbata siųsti. Žr. ',
  'privacy_link': 'privatumo politiką', 'form_ok': 'Ačiū! Įrašėme tavo el. paštą.', 'form_err': 'Nepavyko išsiųsti. Patikrink el. paštą ir sutikimą.',
  'disclaimer': 'Turinys skirtas bendrai informacijai ir nėra medicininė konsultacija.', 'privacy': 'Privatumas',
  # tools hub
  'hub_title': 'Arbata įrankiai: kofeino skaičiuoklė ir kiti',
  'hub_desc': 'Paprasti kofeino ir arbatos įrankiai, suskirstyti pagal kelio etapą. Nereikia registracijos.',
  'crumb_home': 'Pagrindinis', 'crumb_tools': 'Įrankiai',
  'hub_h1': 'Rask įrankį pagal tai, ką nori padaryti',
  'hub_sub': 'Paprasti įrankiai, suskirstyti pagal kelio etapą. Pradžiai nereikia registracijos.',
  'chooser': 'Ką nori padaryti?',
  'chips': [('Sužinoti savo kofeiną', 'know'), ('Rasti arbatą vietoj kavos', 'choose'), ('Sumažinti kavą', 'switch'), ('Palengvinti dieną', 'daily')],
  'start_kicker': 'Pradėk čia', 'start_title': 'Trys žingsniai nuo kavos iki arbatos', 'start_sub': 'Jei nežinai, nuo ko pradėti, eik šiuo keliu.',
  'steps': [('know', 'Kofeino skaičiuoklė', 'Sužinok, kiek kofeino gauni.'), ('choose', 'Kava → arbata keitiklis', 'Gauk lygiavertį arbatos kiekį.'), ('switch', 'Mažinimo planas', 'Gauk dienų planą.')],
  'groups': [
    ('know', 'Sužinok', 'Kiek kofeino gauni ir kuo skiriasi gėrimai.', [
      ('calc', 'calc', 'Kofeino skaičiuoklė', 'Arbata, gramai, vanduo, temperatūra ir laikas: gauni mg kofeino.', '1 min.'),
      ('compare', None, 'Lyginimo įrankis', 'Pasirink bet kuriuos du gėrimus ir gauk lentelę bei grafiką.', '1 min.'),
      ('chart', None, 'Kofeinas organizme', 'Įvesk dienos gėrimus ir pamatyk apytikslį kofeino kiekį laike.', '2 min.')]),
    ('choose', 'Pasirink', 'Rask arbatą vietoj kavos ir palygink kainas.', [
      ('compare', None, 'Kava → arbata keitiklis', 'Įvesk savo kavą ir gauk lygiavertį arbatos kiekį bei kelis pasiūlymus.', '1 min.'),
      ('spark', None, 'Arbatos parinkimo testas', 'Skonis, kofeino tikslas, valanda, pienas, biudžetas: gauni 3 arbatas ir kodėl.', '6–8 klausimai'),
      ('tag', None, 'Kainų palyginimas', 'Kaina už puodelį ir už 100 mg kofeino pagal gamintojus ir parduotuves.', '1 min.')]),
    ('switch', 'Pereik', 'Planas ir palaikymas per pirmąsias savaites.', [
      ('cal', None, 'Mažinimo planas', 'Dienų planas pagal tavo kavos kiekį; eksportuok į kalendorių ar PDF.', '3 min.'),
      ('book', None, 'Atsisakymo dienoraštis', 'Dienų serija, simptomai, pastabos ir trumpi patarimai.', '30 s per dieną')]),
    ('daily', 'Kasdien', 'Įrankiai, kuriais naudojiesi kiekvieną dieną.', [
      ('bars', None, 'Dienos sekiklis ir riba', 'Pridėk gėrimus ir matyk dienos ribą pagal profilį. Saugoma naršyklėje.', '30 s'),
      ('moon', None, 'Paskutinio puodelio laikas', 'Įvesk miego laiką ir jautrumą, gauk apytikslę paskutinę valandą.', '1 min.'),
      ('timer', None, 'Plikymo laikmatis', 'Laikmatis pagal arbatos rūšį ir silpnesnio ar stipresnio kofeino pasirinkimą.', 'Kiekvieną kartą')]),
  ],
  'widgets_title': 'Svetainės ar tinklaraščio savininkui', 'widgets_text': 'Įterpk kofeino skaičiuoklę į savo puslapį.', 'widgets_cta': 'Gauti kodą',
  'data_title': 'Apie skaičius', 'data_text': 'Kofeino kiekiai pateikiami kaip apytiksliai diapazonai. Tai bendra informacija, ne medicininė konsultacija.',
  # calc page
  'calc_page_title': 'Kofeino skaičiuoklė: kiek kofeino yra tavo arbatoje?',
  'calc_page_desc': 'Pasirink arbatą, kiekį, vandenį ir plikymo laiką ir pamatyk apytikslį kofeino kiekį puodelyje bei palyginimą su kava.',
  'calc_h1': 'Kofeino skaičiuoklė', 'calc_lead': 'Sužinok, kiek kofeino gauni iš savo puodelio arbatos. Nereikia registracijos.',
  'l_tea': 'Arbata', 'l_grams': 'Arbatos kiekis', 'l_water': 'Vandens kiekis', 'l_temp': 'Vandens temperatūra', 'l_time': 'Plikymo laikas', 'min': 'min.',
  'result': 'Kofeino puodelyje', 'compare': 'Palyginimas', 'cup': 'Tavo puodelis', 'vs': 'filtrinės kavos puodelio',
  'tool_note': 'Rodomas diapazonas: skirtingi tyrimai gauna skirtingus skaičius, nes kofeino kiekis priklauso nuo arbatos, partijos ir ruošimo. Bendra informacija, ne medicininė konsultacija.',
  'share_title': 'Dalintis ir įterpti', 'copy': 'Kopijuoti nuorodą', 'copied': 'Nuoroda nukopijuota', 'embed': 'Įterpti į svetainę', 'embed_hide': 'Slėpti kodą',
  'link_note': 'Nuoroda išsaugo tavo pasirinkimus.', 'embed_note': 'Įklijuok šį kodą į savo puslapį.',
  'related': 'Netrukus', 'related_items': ['Kava → arbata keitiklis', 'Paskutinio puodelio laikas', 'Plikymo laikmatis'], 'more_about': 'Daugiau apie Arbata →',
  # embed
  'embed_title': 'Kofeino skaičiuoklė (įterpiama)', 'embed_note_s': 'Apytikslis diapazonas. Ne medicininė konsultacija.', 'credit': 'Skaičiuoklė: arbata.pajusk.lt', 'more_tools': 'Daugiau įrankių',
  # privacy
  'priv_title': 'Privatumo politika', 'priv_desc': 'Kaip Arbata naudoja el. pašto adresus.',
  'priv': [
    ('h1', 'Privatumo politika'),
    ('p', 'Šis tekstas yra pirminis pagrindas ir prieš viešą paleidimą turi būti papildytas bei peržiūrėtas.'),
    ('h2', 'Duomenų valdytojas'),
    ('p', 'El. paštas: info@pajusk.lt, telefonas: +37069639386.'),
    ('h2', 'Kokius duomenis renkame'),
    ('p', 'Jei užpildai formą: el. pašto adresą, kalbą, formos pavadinimą ir sutikimo bei pateikimo laiką. Kofeino skaičiuoklė veikia tavo naršyklėje ir mums nesiunčia pasirinkimų.'),
    ('h2', 'Tikslas ir pagrindas'),
    ('p', 'Siunčiame naujienas apie Arbata (planus, įrankius, starter rinkinio startą). Pagrindas yra tavo sutikimas, kurį gali atšaukti bet kada.'),
    ('h2', 'Saugojimas ir atšaukimas'),
    ('p', 'Adresą saugome, kol atšauksi sutikimą arba paprašysi jį ištrinti. Parašyk info@pajusk.lt arba skambink +37069639386.'),
    ('h2', 'Teisės'),
    ('p', 'Turi teisę susipažinti su duomenimis, juos ištaisyti, ištrinti, apriboti tvarkymą ir pateikti skundą Valstybinei duomenų apsaugos inspekcijai.'),
    ('h2', 'Slapukai ir trečiosios šalys'),
    ('p', 'Svetainė šiuo metu nenaudoja sekimo ar reklamos slapukų. Šriftai įkeliami iš Google Fonts, todėl tavo IP adresas gali būti perduotas Google. Svetainę talpina Hostinger.'),
    ('h2', 'Lankomumo statistika'),
    ('p', 'Naudojame savo paprastą statistiką be slapukų ir be naršyklės saugyklos. Užfiksuojame puslapio adresą, kalbą, nukreipiančią svetainę (tik domeną), įrenginio tipą (telefonas, planšetė, kompiuteris) ir paspaudimus ant įrankių ar nuorodų į kitas svetaines. IP adreso neišsaugome: iš jo, naršyklės duomenų ir kasdien keičiamos atsitiktinės reikšmės sudaroma trumpa maiša, kuri galioja tik tą dieną ir neleidžia atpažinti tavęs kitą dieną. Duomenys saugomi ne ilgiau kaip 14 mėnesių ir naudojami tik svetainei gerinti. Jei naršyklėje įjungta „Do Not Track“ ar „Global Privacy Control“, statistikos nesiunčiame. Įrankių (dienoraštis, sekiklis, planas) duomenys lieka tik tavo naršyklėje.'),
  ],
 },
 'en': {
  'skip': 'Skip to content',
  'nav_tools': 'Tools', 'nav_blog': 'Blog', 'nav_guides': 'Guides', 'nav_lib': 'Library', 'nav_rit': 'Rituals', 'nav_brands': 'Brands', 'nav_kit': 'Starter kit',
  'cta_list': 'Join the list', 'all_tools': 'All tools',
  'soon': 'Coming soon', 'open': 'Open',
  'home_title': 'Arbata: quit coffee, keep the energy',
  'home_desc': 'Guides, tools and recommendations for switching from coffee to tea without the headaches. Start with the caffeine calculator.',
  'kicker': 'Help for anyone who wants less coffee',
  'h1': 'Quit coffee. Keep the energy.',
  'sub': 'Guides, tools and honest recommendations for switching from coffee to tea without the headaches.',
  'cta1': 'Join the list', 'cta2': 'Calculate your caffeine',
  'note': 'Tools are free and work without sign-up.',
  'calc_title': 'Caffeine calculator', 'kind_label': 'Type of coffee', 'espresso': 'Espresso', 'filter': 'Filter coffee',
  'per_day': 'Coffees per day', 'total': 'Caffeine per day', 'dec': 'Fewer', 'inc': 'More',
  'eq_pre': 'About ', 'eq_post': ' cups of yerba mate tea',
  'calc_note': 'Averages: espresso ~64 mg, filter ~95 mg, mate ~80 mg. Actual amounts depend on preparation.',
  'trust': [
    ('Numbers without the gloss', 'Caffeine amounts are shown as approximations, with a note on what they depend on.'),
    ('Simple and clear', 'Short guides and tools you can put to use today.'),
    ('Ads are labelled', 'Partner links and advertising are always clearly marked.'),
  ],
  'pillars_title': 'Everything about the switch, in one place', 'pillars_sub': 'From your first day without coffee to your favourite tea. These sections are in preparation.',
  'pillars': [
    ('book', 'Transition guides', 'Week by week: how to cut down on coffee and get through the first days.'),
    ('leaf', 'Tea library', 'Caffeine levels, flavours and brewing: from matcha to strong black tea.'),
    ('cup', 'Recipes and rituals', 'Cold brew tea, latte alternatives and morning routines that replace the coffee break.'),
    ('heart', 'Health and energy', 'Sleep, caffeine timing and calmer energy, with no medical promises.'),
    ('globe', 'Stories and travel', 'Reader experiences and tea journeys: from tea rooms to plantations.'),
    ('gear', 'Recommended gear', 'Teapots, scales, flasks and books. Partner links will be clearly marked.'),
  ],
  'tools_title': 'Tools that actually help', 'tools_sub': 'Simple, quick and free.',
  'shop_kicker': 'When you are ready', 'shop_title': 'A starter kit for the switch',
  'shop_text': 'Four higher-caffeine teas, a brewing card and the 14-day plan.',
  'shop_price': 'Price announced soon', 'shop_cta': 'Tell me when it launches',
  'shop_note': 'Some recommendations will contain partner links; they will always be marked.', 'pouch': 'First batches in preparation',
  'nl_title': 'One email when everything is ready', 'nl_text': 'We will let you know when the 14-day plan and the other tools are ready.',
  'email': 'Email', 'email_ph': 'you@email.com', 'subscribe': 'Subscribe',
  'consent': 'I agree that my email is used to send news about Arbata. See the ',
  'privacy_link': 'privacy policy', 'form_ok': 'Thank you! We saved your email.', 'form_err': 'Could not send. Check your email and the consent box.',
  'disclaimer': 'Content is for general information and is not medical advice.', 'privacy': 'Privacy',
  'hub_title': 'Arbata tools: caffeine calculator and more',
  'hub_desc': 'Simple caffeine and tea tools, grouped by stage of the journey. No sign-up needed.',
  'crumb_home': 'Home', 'crumb_tools': 'Tools',
  'hub_h1': 'Find the tool for what you want to do',
  'hub_sub': 'Simple tools, grouped by stage of the journey. No sign-up needed to start.',
  'chooser': 'What do you want to do?',
  'chips': [('Know my caffeine', 'know'), ('Find a tea instead of coffee', 'choose'), ('Cut down on coffee', 'switch'), ('Make my day easier', 'daily')],
  'start_kicker': 'Start here', 'start_title': 'Three steps from coffee to tea', 'start_sub': 'Not sure where to begin? Follow this path.',
  'steps': [('know', 'Caffeine calculator', 'See how much caffeine you get.'), ('choose', 'Coffee → tea converter', 'Get an equivalent amount of tea.'), ('switch', 'Cutting-down plan', 'Get a day-by-day plan.')],
  'groups': [
    ('know', 'Know', 'How much caffeine you get and how drinks differ.', [
      ('calc', 'calc', 'Caffeine calculator', 'Tea, grams, water, temperature and time: get mg of caffeine.', '1 min'),
      ('compare', None, 'Comparison tool', 'Pick any two drinks and get a table and a chart.', '1 min'),
      ('chart', None, 'Caffeine in the body', 'Enter your day\'s drinks and see approximate caffeine levels over time.', '2 min')]),
    ('choose', 'Choose', 'Find a tea instead of coffee and compare prices.', [
      ('compare', None, 'Coffee → tea converter', 'Enter your coffee and get an equivalent tea amount plus a few suggestions.', '1 min'),
      ('spark', None, 'Tea finder quiz', 'Flavour, caffeine goal, time of day, milk, budget: get 3 teas and why.', '6–8 questions'),
      ('tag', None, 'Price comparison', 'Price per cup and per 100 mg of caffeine across brands and shops.', '1 min')]),
    ('switch', 'Switch', 'A plan and support for the first weeks.', [
      ('cal', None, 'Cutting-down plan', 'A day-by-day plan based on your coffee intake; export to calendar or PDF.', '3 min'),
      ('book', None, 'Quit diary', 'Day streak, symptoms, notes and short tips.', '30 s a day')]),
    ('daily', 'Daily', 'Tools you use every day.', [
      ('bars', None, 'Daily tracker and limit', 'Add drinks and see your daily limit by profile. Stored in your browser.', '30 s'),
      ('moon', None, 'Last cup time', 'Enter your bedtime and sensitivity to get an approximate last hour.', '1 min'),
      ('timer', None, 'Brewing timer', 'A timer by tea type with a weaker or stronger caffeine choice.', 'Every brew')]),
  ],
  'widgets_title': 'For website and blog owners', 'widgets_text': 'Embed the caffeine calculator on your own page.', 'widgets_cta': 'Get the code',
  'data_title': 'About the numbers', 'data_text': 'Caffeine amounts are shown as approximate ranges. This is general information, not medical advice.',
  'calc_page_title': 'Caffeine calculator: how much caffeine is in your tea?',
  'calc_page_desc': 'Pick your tea, amount, water and steeping time to see the approximate caffeine in your cup and how it compares to coffee.',
  'calc_h1': 'Caffeine calculator', 'calc_lead': 'See how much caffeine you get from your cup of tea. No sign-up needed.',
  'l_tea': 'Tea', 'l_grams': 'Tea amount', 'l_water': 'Water', 'l_temp': 'Water temperature', 'l_time': 'Steeping time', 'min': 'min',
  'result': 'Caffeine in your cup', 'compare': 'Comparison', 'cup': 'Your cup', 'vs': 'of a cup of filter coffee',
  'tool_note': 'A range is shown because studies report different numbers: caffeine depends on the tea, the batch and how it is prepared. General information, not medical advice.',
  'share_title': 'Share and embed', 'copy': 'Copy link', 'copied': 'Link copied', 'embed': 'Embed on your site', 'embed_hide': 'Hide code',
  'link_note': 'The link keeps your choices.', 'embed_note': 'Paste this code into your page.',
  'related': 'Coming soon', 'related_items': ['Coffee → tea converter', 'Last cup time', 'Brewing timer'], 'more_about': 'More about Arbata →',
  'embed_title': 'Caffeine calculator (embed)', 'embed_note_s': 'Approximate range. Not medical advice.', 'credit': 'Calculator by arbata.pajusk.lt', 'more_tools': 'More tools',
  'priv_title': 'Privacy policy', 'priv_desc': 'How Arbata uses email addresses.',
  'priv': [
    ('h1', 'Privacy policy'),
    ('p', 'This text is a starting point and must be completed and reviewed before the public launch.'),
    ('h2', 'Data controller'),
    ('p', 'Email: info@pajusk.lt, phone: +37069639386.'),
    ('h2', 'What we collect'),
    ('p', 'If you fill in a form: your email address, language, form name and the time of consent and submission. The caffeine calculator runs in your browser and does not send your choices to us.'),
    ('h2', 'Purpose and basis'),
    ('p', 'We send news about Arbata (plans, tools, the starter kit launch). The basis is your consent, which you can withdraw at any time.'),
    ('h2', 'Storage and withdrawal'),
    ('p', 'We keep your address until you withdraw consent or ask us to delete it. Write to info@pajusk.lt or call +37069639386.'),
    ('h2', 'Your rights'),
    ('p', 'You may access, correct or delete your data, restrict processing and lodge a complaint with your data protection authority.'),
    ('h2', 'Cookies and third parties'),
    ('p', 'The site currently uses no tracking or advertising cookies. Fonts load from Google Fonts, so your IP address may be shared with Google. The site is hosted by Hostinger.'),
    ('h2', 'Visit statistics'),
    ('p', 'We use our own simple statistics with no cookies and no browser storage. We record the page address, language, referring site (domain only), device type (phone, tablet, desktop) and clicks on tools or links to other sites. We do not store your IP address: a short hash is made from it, your browser details and a random value that changes every day, so it is valid for that day only and cannot recognise you on another day. Data is kept for no more than 14 months and is used only to improve the site. If your browser sends Do Not Track or Global Privacy Control, we send no statistics. Data in the tools (diary, tracker, plan) stays in your browser only.'),
  ],
 },
 'it': {
  'skip': 'Vai al contenuto',
  'nav_tools': 'Strumenti', 'nav_blog': 'Blog', 'nav_guides': 'Guide', 'nav_lib': 'Libreria', 'nav_rit': 'Rituali', 'nav_brands': 'Marche', 'nav_kit': 'Starter kit',
  'cta_list': 'Iscriviti alla lista', 'all_tools': 'Tutti gli strumenti',
  'soon': 'In arrivo', 'open': 'Apri',
  'home_title': 'Arbata: lascia il caffè, tieni l\'energia',
  'home_desc': 'Guide, strumenti e consigli per passare dal caffè al tè senza mal di testa. Parti dal calcolatore di caffeina.',
  'kicker': 'Un aiuto per chi vuole meno caffè',
  'h1': 'Lascia il caffè. Tieni l\'energia.',
  'sub': 'Guide, strumenti e consigli onesti per passare dal caffè al tè senza mal di testa.',
  'cta1': 'Iscriviti alla lista', 'cta2': 'Calcola la caffeina',
  'note': 'Gli strumenti sono gratuiti e funzionano senza registrazione.',
  'calc_title': 'Calcolatore di caffeina', 'kind_label': 'Tipo di caffè', 'espresso': 'Espresso', 'filter': 'Caffè filtro',
  'per_day': 'Caffè al giorno', 'total': 'Caffeina al giorno', 'dec': 'Meno', 'inc': 'Di più',
  'eq_pre': 'Circa ', 'eq_post': ' tazze di tè yerba mate',
  'calc_note': 'Medie: espresso ~64 mg, filtro ~95 mg, mate ~80 mg. Il valore reale dipende dalla preparazione.',
  'trust': [
    ('Numeri senza abbellimenti', 'Le quantità di caffeina sono approssimative e spieghiamo da cosa dipendono.'),
    ('Semplice e chiaro', 'Guide brevi e strumenti da usare già oggi.'),
    ('Pubblicità segnalata', 'Link di partner e pubblicità sono sempre indicati chiaramente.'),
  ],
  'pillars_title': 'Tutto sul passaggio, in un solo posto', 'pillars_sub': 'Dal primo giorno senza caffè al tuo tè preferito. Queste sezioni sono in preparazione.',
  'pillars': [
    ('book', 'Guide alla transizione', 'Settimana dopo settimana: come ridurre il caffè e superare i primi giorni.'),
    ('leaf', 'Biblioteca dei tè', 'Caffeina, sapori e preparazione: dal matcha al tè nero deciso.'),
    ('cup', 'Ricette e rituali', 'Tè cold brew, alternative al latte macchiato e routine che sostituiscono la pausa caffè.'),
    ('heart', 'Salute ed energia', 'Sonno, orari della caffeina ed energia più calma, senza promesse mediche.'),
    ('globe', 'Storie e viaggi', 'Esperienze dei lettori e viaggi nel tè: dalle sale da tè alle piantagioni.'),
    ('gear', 'Strumenti consigliati', 'Teiere, bilance, thermos e libri. I link di partner saranno sempre segnalati.'),
  ],
  'tools_title': 'Strumenti che aiutano davvero', 'tools_sub': 'Semplici, veloci e gratuiti.',
  'shop_kicker': 'Quando sei pronto', 'shop_title': 'Starter kit per la transizione',
  'shop_text': 'Quattro tè con più caffeina, una scheda di preparazione e il piano di 14 giorni.',
  'shop_price': 'Prezzo in arrivo', 'shop_cta': 'Avvisami al lancio',
  'shop_note': 'Alcuni consigli conterranno link di partner; saranno sempre segnalati.', 'pouch': 'Primi lotti in preparazione',
  'nl_title': 'Una email quando tutto è pronto', 'nl_text': 'Ti avviseremo quando saranno pronti il piano di 14 giorni e gli altri strumenti.',
  'email': 'Email', 'email_ph': 'tua@email.it', 'subscribe': 'Iscriviti',
  'consent': 'Acconsento all\'uso della mia email per ricevere novità su Arbata. Vedi l\'',
  'privacy_link': 'informativa sulla privacy', 'form_ok': 'Grazie! Abbiamo salvato la tua email.', 'form_err': 'Invio non riuscito. Controlla l\'email e il consenso.',
  'disclaimer': 'Contenuti a scopo informativo; non sostituiscono il parere medico.', 'privacy': 'Privacy',
  'hub_title': 'Strumenti Arbata: calcolatore di caffeina e altro',
  'hub_desc': 'Strumenti semplici su caffeina e tè, divisi per tappa del percorso. Non serve registrarsi.',
  'crumb_home': 'Home', 'crumb_tools': 'Strumenti',
  'hub_h1': 'Trova lo strumento giusto per ciò che vuoi fare',
  'hub_sub': 'Strumenti semplici, divisi per tappa del percorso. Per iniziare non serve registrarsi.',
  'chooser': 'Cosa vuoi fare?',
  'chips': [('Conoscere la mia caffeina', 'know'), ('Trovare un tè al posto del caffè', 'choose'), ('Ridurre il caffè', 'switch'), ('Facilitare la giornata', 'daily')],
  'start_kicker': 'Parti da qui', 'start_title': 'Tre passi dal caffè al tè', 'start_sub': 'Non sai da dove iniziare? Segui questo percorso.',
  'steps': [('know', 'Calcolatore di caffeina', 'Scopri quanta caffeina assumi.'), ('choose', 'Convertitore caffè → tè', 'Ottieni la quantità di tè equivalente.'), ('switch', 'Piano di riduzione', 'Ottieni un piano giorno per giorno.')],
  'groups': [
    ('know', 'Scopri', 'Quanta caffeina assumi e come differiscono le bevande.', [
      ('calc', 'calc', 'Calcolatore di caffeina', 'Tè, grammi, acqua, temperatura e tempo: ottieni i mg di caffeina.', '1 min'),
      ('compare', None, 'Strumento di confronto', 'Scegli due bevande qualsiasi e ottieni tabella e grafico.', '1 min'),
      ('chart', None, 'Caffeina nel corpo', 'Inserisci le bevande del giorno e vedi la caffeina approssimativa nel tempo.', '2 min')]),
    ('choose', 'Scegli', 'Trova un tè al posto del caffè e confronta i prezzi.', [
      ('compare', None, 'Convertitore caffè → tè', 'Inserisci il tuo caffè e ottieni la quantità di tè equivalente e alcuni consigli.', '1 min'),
      ('spark', None, 'Quiz: quale tè scegliere', 'Gusto, obiettivo di caffeina, orario, latte, budget: ottieni 3 tè e perché.', '6–8 domande'),
      ('tag', None, 'Confronto prezzi', 'Prezzo per tazza e per 100 mg di caffeina tra marchi e negozi.', '1 min')]),
    ('switch', 'Passa', 'Un piano e un sostegno per le prime settimane.', [
      ('cal', None, 'Piano di riduzione', 'Un piano giorno per giorno in base al tuo caffè; esporta su calendario o PDF.', '3 min'),
      ('book', None, 'Diario senza caffè', 'Serie di giorni, sintomi, note e brevi consigli.', '30 s al giorno')]),
    ('daily', 'Ogni giorno', 'Strumenti da usare tutti i giorni.', [
      ('bars', None, 'Contatore e limite giornaliero', 'Aggiungi le bevande e vedi il limite giornaliero per profilo. Salvato nel browser.', '30 s'),
      ('moon', None, 'Ora dell\'ultima tazza', 'Inserisci l\'ora del sonno e la sensibilità per avere l\'ultima ora indicativa.', '1 min'),
      ('timer', None, 'Timer di infusione', 'Timer per tipo di tè con scelta di caffeina più leggera o più forte.', 'Ogni infusione')]),
  ],
  'widgets_title': 'Per chi ha un sito o un blog', 'widgets_text': 'Inserisci il calcolatore di caffeina nella tua pagina.', 'widgets_cta': 'Ottieni il codice',
  'data_title': 'Sui numeri', 'data_text': 'Le quantità di caffeina sono indicate come intervalli approssimativi. Informazioni generali, non parere medico.',
  'calc_page_title': 'Calcolatore di caffeina: quanta caffeina c\'è nel tuo tè?',
  'calc_page_desc': 'Scegli tè, quantità, acqua e tempo di infusione per vedere la caffeina approssimativa nella tazza e il confronto con il caffè.',
  'calc_h1': 'Calcolatore di caffeina', 'calc_lead': 'Scopri quanta caffeina assumi con la tua tazza di tè. Non serve registrarsi.',
  'l_tea': 'Tè', 'l_grams': 'Quantità di tè', 'l_water': 'Acqua', 'l_temp': 'Temperatura dell\'acqua', 'l_time': 'Tempo di infusione', 'min': 'min',
  'result': 'Caffeina nella tazza', 'compare': 'Confronto', 'cup': 'La tua tazza', 'vs': 'di una tazza di caffè filtro',
  'tool_note': 'Mostriamo un intervallo perché gli studi riportano valori diversi: la caffeina dipende dal tè, dal lotto e dalla preparazione. Informazioni generali, non parere medico.',
  'share_title': 'Condividi e incorpora', 'copy': 'Copia il link', 'copied': 'Link copiato', 'embed': 'Incorpora nel tuo sito', 'embed_hide': 'Nascondi il codice',
  'link_note': 'Il link conserva le tue scelte.', 'embed_note': 'Incolla questo codice nella tua pagina.',
  'related': 'In arrivo', 'related_items': ['Convertitore caffè → tè', 'Ora dell\'ultima tazza', 'Timer di infusione'], 'more_about': 'Di più su Arbata →',
  'embed_title': 'Calcolatore di caffeina (incorporabile)', 'embed_note_s': 'Intervallo indicativo. Non è un parere medico.', 'credit': 'Calcolatore di arbata.pajusk.lt', 'more_tools': 'Altri strumenti',
  'priv_title': 'Informativa sulla privacy', 'priv_desc': 'Come Arbata usa gli indirizzi email.',
  'priv': [
    ('h1', 'Informativa sulla privacy'),
    ('p', 'Questo testo è una base di partenza e va completato e rivisto prima del lancio pubblico.'),
    ('h2', 'Titolare del trattamento'),
    ('p', 'E-mail: info@pajusk.lt, telefono: +37069639386.'),
    ('h2', 'Quali dati raccogliamo'),
    ('p', 'Se compili un modulo: indirizzo email, lingua, nome del modulo e data del consenso e dell\'invio. Il calcolatore di caffeina funziona nel tuo browser e non ci invia le tue scelte.'),
    ('h2', 'Finalità e base giuridica'),
    ('p', 'Inviamo novità su Arbata (piani, strumenti, lancio dello starter kit). La base è il tuo consenso, che puoi revocare in qualsiasi momento.'),
    ('h2', 'Conservazione e revoca'),
    ('p', 'Conserviamo l\'indirizzo finché non revochi il consenso o ne chiedi la cancellazione. Scrivi a info@pajusk.lt o chiama +37069639386.'),
    ('h2', 'I tuoi diritti'),
    ('p', 'Puoi accedere ai dati, rettificarli, cancellarli, limitarne il trattamento e proporre reclamo al Garante per la protezione dei dati personali.'),
    ('h2', 'Cookie e terze parti'),
    ('p', 'Il sito non usa al momento cookie di tracciamento o pubblicitari. I caratteri sono caricati da Google Fonts, quindi il tuo indirizzo IP può essere condiviso con Google. Il sito è ospitato da Hostinger.'),
    ('h2', 'Statistiche di visita'),
    ('p', 'Usiamo statistiche semplici e nostre, senza cookie e senza archiviazione nel browser. Registriamo l\'indirizzo della pagina, la lingua, il sito di provenienza (solo dominio), il tipo di dispositivo (telefono, tablet, computer) e i clic sugli strumenti o sui link verso altri siti. Non conserviamo il tuo indirizzo IP: ne ricaviamo un breve hash insieme ai dati del browser e a un valore casuale che cambia ogni giorno, valido solo per quel giorno e che non ti riconosce nei giorni successivi. I dati sono conservati al massimo 14 mesi e usati solo per migliorare il sito. Se il browser invia Do Not Track o Global Privacy Control, non inviamo statistiche. I dati degli strumenti (diario, tracker, piano) restano solo nel tuo browser.'),
  ],
 },
}

LIVE = {('switch', 0): 'plan', ('switch', 1): 'diary', ('choose', 1): 'quiz', ('know', 1): 'compare', ('know', 2): 'body', ('choose', 0): 'convert', ('daily', 0): 'tracker', ('daily', 1): 'lastcup', ('daily', 2): 'timer'}
for _l in LANGS:
    _g = C[_l]['groups']
    for _gi, (_gid, _t, _s, _tools) in enumerate(_g):
        _g[_gi] = (_gid, _t, _s, [(ic, LIVE.get((_gid, ti), key), tt, d, m) for ti, (ic, key, tt, d, m) in enumerate(_tools)])
    C[_l]['steps'] = C[_l]['steps']

import caff
TEAS = [(tid, lo, hi, 1 if whole else 0, caff.TEA_NAMES[tid]) for tid, lo, hi, g, whole, src, conf in caff.TEAS]
EMBED_TEAS = ['black', 'green', 'mate', 'matcha']
TIME_F = caff.TIME_F
DEF_G = 2
ESP = [d for d in caff.drinks() if d['id'] == 'espresso'][0]['typ']
FIL = [d for d in caff.drinks() if d['id'] == 'filter'][0]['typ']
MATE_CUP = [d for d in caff.drinks() if d['id'] == 'mate'][0]['typ']

def rnd(x):
    return int(x + 0.5)


def fmt(n, lang):
    s = str(n)
    return s if lang == 'en' else s.replace('.', ',')


# --------------------------------------------------------------------------------------
# BENDRI BLOKAI
# --------------------------------------------------------------------------------------
def head(lang, key, title, desc, noindex=False):
    av = langs_of(key)
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{PATH[key](l)}">' for l in av)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{PATH[key]("en" if "en" in av else av[0])}">'
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{BASE}{PATH[key](lang)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Arbata">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{BASE}{PATH[key](lang)}">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta name="theme-color" content="#1E4D36">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/a.js" defer></script>
</head>'''


def header(lang, key, slim=False):
    c = C[lang]
    langs = ''.join(
        f'<a href="{lang_url(key, l)}" lang="{l}" hreflang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>'
        for l in LANGS)
    logo = (f'<a class="logo" href="/{lang}/"><span class="logo-mark">{LEAF_LOGO}</span>'
            f'<span class="logo-text">arbata</span></a>')
    if slim:
        return (f'<header class="wrap wrap-narrow hdr hdr-slim">{logo}<div class="hdr-right">'
                f'<a class="hdr-link" href="{PATH["tools"](lang)}">{E(c["all_tools"])}</a>'
                f'<div class="langs" role="group" aria-label="Language">{langs}</div></div></header>')
    cur = ' aria-current="page"' if key == 'tools' else ''
    curb = ' aria-current="page"' if key == 'blog' or key.startswith('b_') else ''
    curt = ' aria-current="page"' if key == 'hub_t' or key.startswith('tl_') else ''
    curm = ' aria-current="page"' if key == 'hub_b' or key.startswith('br_') else ''
    nav = (f'<nav class="nav" aria-label="Main"><a href="{PATH["tools"](lang)}"{cur}>{E(c["nav_tools"])}</a>'
           f'<a href="{PATH["blog"](lang)}"{curb}>{E(c["nav_blog"])}</a>'
           f'<a href="{PATH["hub_t"](lang)}"{curt}>{E(c["nav_lib"])}</a>'
           f'<a href="{PATH["hub_r"](lang)}"{"" if not (key == "hub_r" or key.startswith("r_")) else " aria-current=page"}>{E(c["nav_rit"])}</a>'
           f'<a href="{PATH["hub_b"](lang)}"{curm}>{E(c["nav_brands"])}</a>'
           f'<a href="{PATH["home"](lang)}#pillars">{E(c["nav_guides"])}</a>'
           f'<a href="{PATH["home"](lang)}#shop">{E(c["nav_kit"])}</a></nav>')
    cta = f'<a class="btn btn-forest btn-sm" href="{PATH["home"](lang)}#newsletter">{E(c["cta_list"])}</a>'
    return (f'<header class="wrap hdr">{logo}{nav}<div class="hdr-right">'
            f'<div class="langs" role="group" aria-label="Language">{langs}</div>{cta}</div></header>')


CONTACT_PHONE = '+37069639386'
CONTACT_EMAIL = 'info@pajusk.lt'


def contact_html():
    parts = []
    if CONTACT_EMAIL:
        parts.append(f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>')
    parts.append(f'<a href="tel:{CONTACT_PHONE}">{CONTACT_PHONE[:4]} {CONTACT_PHONE[4:7]} {CONTACT_PHONE[7:]}</a>')
    return ' · '.join(parts)


def footer(lang, quiet=False):
    c = C[lang]
    priv = f'<a href="{PATH["privacy"](lang)}">{E(c["privacy"])}</a>'
    if not quiet:
        priv = ' · '.join(f'<a href="{PATH[k](lang)}">{E(c[n])}</a>' for k, n in (('blog', 'nav_blog'), ('hub_t', 'nav_lib'), ('hub_r', 'nav_rit'), ('hub_b', 'nav_brands'), ('tools', 'nav_tools'))) + ' · ' + priv
    if quiet:
        return (f'<footer class="ftr ftr-quiet"><div class="wrap wrap-narrow ftr-in"><span>© 2026 Arbata</span>'
                f'<span>{contact_html()} · {priv}</span></div></footer>')
    return (f'<footer class="ftr"><div class="wrap ftr-in"><div><span class="logo-text">arbata</span>'
            f'<small>{E(c["disclaimer"])}</small></div><div>{contact_html()}<br>{priv}</div></div>'
            f'<div class="wrap ftr-bottom">© 2026 Arbata</div></footer>')


def shell(lang, key, title, desc, main, quiet_footer=False, slim=False, scripts=(), noindex=False):
    c = C[lang]
    main = _BG.augment(__import__('sys').modules[__name__], key, lang, main)
    js = ''.join(f'<script src="/assets/{s}" defer></script>' for s in scripts)
    return (head(lang, key, title, desc, noindex) + '\n<body>\n'
            f'<a class="skip" href="#main">{E(c["skip"])}</a>\n'
            + header(lang, key, slim) + '\n' + main + '\n' + footer(lang, quiet_footer) + '\n' + js + '\n</body>\n</html>\n')


def form(lang, source, btn_label, dark=False):
    c = C[lang]
    uid = f'{source}-{lang}'
    return f'''<form class="form" action="/subscribe.php" method="post" data-subscribe data-ok="{E(c['form_ok'])}" data-err="{E(c['form_err'])}">
<input type="hidden" name="lang" value="{lang}"><input type="hidden" name="source" value="{source}">
<div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-row">
<label class="sr-only" for="em-{uid}">{E(c['email'])}</label>
<input id="em-{uid}" type="email" name="email" required autocomplete="email" placeholder="{E(c['email_ph'])}">
<button class="btn btn-amber btn-lg" type="submit">{E(btn_label)}</button>
</div>
<label class="consent"><input type="checkbox" name="consent" value="1" required><span>{E(c['consent'])}<a href="{PATH['privacy'](lang)}">{E(c['privacy_link'])}</a>.</span></label>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>'''


# --------------------------------------------------------------------------------------
# PUSLAPIAI
# --------------------------------------------------------------------------------------
def tool_card(lang, icon, key, title, text, meta):
    c = C[lang]
    inner = (f'<span class="ico ico-round">{svg(icon, 28)}</span><span class="card-title">{E(title)}</span>'
             f'<span class="card-text">{E(text)}</span>')
    if key:
        return (f'<a class="card" href="{PATH[key](lang)}">{inner}<span class="card-foot"><span class="chip">{E(meta)}</span>'
                f'<span class="go">{E(c["open"])} →</span></span></a>')
    return (f'<div class="card card-soon">{inner}<span class="card-foot"><span class="chip">{E(meta)}</span>'
            f'<span class="chip chip-soon">{E(c["soon"])}</span></span></div>')


def home(lang):
    c = C[lang]
    cups, per, mate = 3, FIL, MATE_CUP
    mg = cups * per
    eq = fmt(round(mg / mate * 10) / 10, lang)
    trust = ''.join(f'<div class="trust-item"><i></i><div><b>{E(t)}</b><span>{E(d)}</span></div></div>' for t, d in c['trust'])
    pillars = ''
    for i, (ic, t, d) in enumerate(c['pillars']):
        dark = ' card-dark' if i == 5 else ''
        tgt = {'leaf': 'hub_t', 'book': 'blog', 'heart': 'g_limit', 'cup': 'hub_r'}.get(ic)
        if tgt:
            pillars += (f'<a class="card" href="{PATH[tgt](lang)}"><span class="ico">{svg(ic, 26)}</span><span class="card-title">{E(t)}</span>'
                        f'<span class="card-text">{E(d)}</span><span class="card-foot"><span class="chip">{E(c["open"])}</span></span></a>')
            continue
        pillars += (f'<div class="card{dark}"><span class="ico">{svg(ic, 26)}</span><span class="card-title">{E(t)}</span>'
                    f'<span class="card-text">{E(d)}</span><span class="card-foot"><span class="chip chip-soon">{E(c["soon"])}</span></span></div>')
    tools_cards = ''
    sel = [c['groups'][0][3][0], c['groups'][1][3][0], c['groups'][2][3][0]]
    for ic, key, t, d, m in sel:
        tools_cards += tool_card(lang, ic, key, t, d, m)
    pouch = '''<svg width="220" height="300" viewBox="0 0 220 300" aria-hidden="true"><path d="M30 20h160a10 10 0 0 1 10 10v250a10 10 0 0 1-10 10H30a10 10 0 0 1-10-10V30a10 10 0 0 1 10-10z" fill="#F5F6F0"/><rect x="20" y="20" width="180" height="22" rx="10" fill="#E8A33D"/><rect x="45" y="96" width="130" height="130" rx="16" fill="#1E4D36"/><path d="M92 150c0-18 13-30 31-30 0 18-13 30-31 30zM92 150l16-16" fill="none" stroke="#F2C67A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="110" y="196" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="700" font-size="30" fill="#F5F6F0">arbata</text><circle cx="110" cy="262" r="6" fill="#C77F12"/></svg>'''
    main = f'''<main id="main">
<section class="wrap hero" id="top">
<div class="hero-l">
<span class="kicker"><i></i>{E(c['kicker'])}</span>
<h1 class="hero-title">{E(c['h1'])}</h1>
<p class="lead">{E(c['sub'])}</p>
<div class="row-btns"><a class="btn btn-amber btn-lg" href="#newsletter">{E(c['cta1'])}</a><a class="btn btn-outline btn-lg" href="#calc">{E(c['cta2'])}</a></div>
<span class="small">{E(c['note'])}</span>
</div>
<div class="hero-r"><div class="hero-panel" id="calc">
<svg class="c1" width="320" height="320" viewBox="0 0 320 320" aria-hidden="true"><circle cx="160" cy="160" r="160" fill="#C5D9B5"/></svg>
<svg class="c2" width="200" height="200" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="100" fill="#E8A33D" opacity="0.55"/></svg>
<div class="calc-card" id="hc" data-espresso="{ESP}" data-filter="{FIL}" data-mate="{MATE_CUP}" data-eq-pre="{E(c['eq_pre'])}" data-eq-post="{E(c['eq_post'])}">
<div class="cc-head"><span class="cc-ico">{svg('calc', 22)}</span><span class="cc-title">{E(c['calc_title'])}</span></div>
<div class="seg" role="group" aria-label="{E(c['kind_label'])}"><button type="button" data-kind="espresso" aria-pressed="false">{E(c['espresso'])}</button><button type="button" data-kind="filter" aria-pressed="true">{E(c['filter'])}</button></div>
<div class="row"><span class="row-label">{E(c['per_day'])}</span><div class="stepper"><button type="button" data-act="dec" aria-label="{E(c['dec'])}">−</button><output id="hc-cups">{cups}</output><button type="button" data-act="inc" aria-label="{E(c['inc'])}">+</button></div></div>
<div class="res"><span class="eyebrow">{E(c['total'])}</span><div><span class="big" id="hc-mg">{mg}</span> <span class="unit">mg</span></div><span class="res-eq" id="hc-eq">{E(c['eq_pre'])}{eq}{E(c['eq_post'])}</span></div>
<span class="small">{E(c['calc_note'])}</span>
</div></div></div>
</section>

<section class="trust-band"><div class="wrap trust">{trust}</div></section>

<section class="wrap sec" id="pillars">
<div class="sec-head"><h2 class="sec-title">{E(c['pillars_title'])}</h2><p class="sec-sub">{E(c['pillars_sub'])}</p></div>
<div class="grid">{pillars}</div>
</section>

<section class="wrap sec" id="tools">
<div class="sec-head"><h2 class="sec-title">{E(c['tools_title'])}</h2><p class="sec-sub">{E(c['tools_sub'])}</p></div>
<div class="grid">{tools_cards}</div>
<p style="margin-top:24px"><a class="btn btn-outline btn-sm" href="{PATH['tools'](lang)}">{E(c['all_tools'])} →</a></p>
</section>

<section class="wrap sec" id="shop">
<div class="shop"><div class="shop-l">
<span class="eyebrow">{E(c['shop_kicker'])}</span>
<h2 class="sec-title">{E(c['shop_title'])}</h2>
<p class="lead">{E(c['shop_text'])}</p>
<div class="price">{E(c['shop_price'])}</div>
{form(lang, 'starter-kit', c['shop_cta'])}
<span class="small">{E(c['shop_note'])}</span>
</div><div class="shop-r">{pouch}<span class="small">{E(c['pouch'])}</span></div></div>
</section>

<section class="wrap sec" id="newsletter">
<div class="nl"><div class="nl-l"><h2>{E(c['nl_title'])}</h2><p>{E(c['nl_text'])}</p></div>
<div class="nl-r">{form(lang, 'newsletter', c['subscribe'])}</div></div>
</section>
</main>'''
    return shell(lang, 'home', c['home_title'], c['home_desc'], main, scripts=('home.js', 'forms.js'))


def tools_hub(lang):
    c = C[lang]
    chips = ''.join(f'<a href="#{g}">{E(t)}</a>' for t, g in c['chips'])
    steps = ''
    for i, (g, t, d) in enumerate(c['steps'], 1):
        steps += f'<a class="step" href="#{g}"><span class="step-n">{i}</span><span><b>{E(t)}</b><span>{E(d)}</span></span></a>'
    groups = ''
    for i, (gid, gt, gs, tools) in enumerate(c['groups'], 1):
        cards = ''.join(tool_card(lang, ic, key, t, d, m) for ic, key, t, d, m in tools)
        groups += (f'<div id="{gid}" class="g{i}"><div class="group-head"><span class="group-n">{i}</span><div><h2>{E(gt)}</h2>'
                   f'<span class="sub">{E(gs)}</span></div></div><div class="grid">{cards}</div></div>')
    main = f'''<main id="main">
<section class="wrap hub-head">
<div class="crumbs"><a href="{PATH['home'](lang)}">{E(c['crumb_home'])}</a> / <span>{E(c['crumb_tools'])}</span></div>
<h1 class="page-title">{E(c['hub_h1'])}</h1>
<p class="lead">{E(c['hub_sub'])}</p>
<div><span class="eyebrow" style="display:block;margin-bottom:10px">{E(c['chooser'])}</span><div class="chips">{chips}</div></div>
</section>
<section class="wrap"><div class="start"><div><span class="eyebrow">{E(c['start_kicker'])}</span><h2>{E(c['start_title'])}</h2><p>{E(c['start_sub'])}</p></div><div class="steps">{steps}</div></div></section>
<section class="wrap groups">{groups}</section>
<section class="wrap duo">
<div class="panel panel-leaf"><span class="ico" style="background:var(--forest);color:var(--ground)">{svg('code', 24)}</span><h2>{E(c['widgets_title'])}</h2><p class="card-text" style="color:var(--muted-2)">{E(c['widgets_text'])}</p><a class="btn btn-forest btn-sm" href="{PATH['calc'](lang)}#share">{E(c['widgets_cta'])}</a></div>
<div class="panel panel-white"><span class="ico" style="background:var(--sand);color:var(--sand-fg)">{svg('info', 24)}</span><h2>{E(c['data_title'])}</h2><p class="card-text">{E(c['data_text'])}</p><a class="btn btn-outline btn-sm" href="{PATH['hub_d'](lang)}">{E(__import__('seo_gen').L[lang]['hub_d'])}</a> <a class="btn btn-outline btn-sm" href="{PATH['hub_b'](lang)}">{E(__import__('brands_gen').T[lang]['hub'])}</a> <a class="btn btn-outline btn-sm" href="{PATH['hub_t'](lang)}">{E(__import__('tealib_gen').T[lang]['hub'])}</a></div>
</section>
</main>'''
    return shell(lang, 'tools', c['hub_title'], c['hub_desc'], main)


def calc_defaults():
    lo_, hi_ = TEAS[0][1], TEAS[0][2]
    f = TIME_F[4]
    lo, hi = rnd(DEF_G * lo_ * f), rnd(DEF_G * hi_ * f)
    return lo, hi


SRC_H = {'lt': ('Šaltiniai', 'Duomenys patikrinti', 'Mažesnio patikimumo duomenys (mate): rodomas platus diapazonas.'),
         'en': ('Sources', 'Data checked', 'Lower-confidence data (mate): a wide range is shown.'),
         'it': ('Fonti', 'Dati verificati', 'Dati meno solidi (mate): mostriamo un intervallo ampio.')}


def sources_html(lang):
    h, chk, low = SRC_H[lang]
    used = []
    for d in caff.drinks():
        for k in d['src']:
            if k not in used:
                used.append(k)
    for k in ('fsanz',):
        if k not in used:
            used.append(k)
    items = ''.join(f'<li><a href="{caff.SOURCES[k][1]}" target="_blank" rel="noopener nofollow">{E(caff.SOURCES[k][0])}</a></li>' for k in used)
    return f'''<section class="sources" aria-labelledby="src-h"><h2 id="src-h" style="font-size:18px">{h}</h2><ul class="small" style="padding-left:18px;display:grid;gap:4px">{items}</ul><span class="small">{chk}: {caff.CHECKED}. {low}</span></section>'''


def calc_page(lang):
    c = C[lang]
    lo, hi = calc_defaults()
    mid = (lo + hi) / 2
    pct = lambda v: f'{min(100, rnd(v / 120 * 100))}%'
    teas = ''.join(
        f'<button type="button" data-tea="{tid}" data-lo="{l}" data-hi="{h}" data-whole="{w}" aria-pressed="{"true" if i == 0 else "false"}">{E(names[lang])}</button>'
        for i, (tid, l, h, w, names) in enumerate(TEAS))
    times = ''.join(f'<button type="button" data-time="{m}" aria-pressed="{"true" if m == 4 else "false"}">{m} {E(c["min"])}</button>' for m in (2, 3, 4, 5))
    a, b = round(lo / 250 * 100 * 10) / 10, round(hi / 250 * 100 * 10) / 10
    related = ''.join(f'<a href="{PATH[k](lang)}">{E(TG.TXT[k][lang]["menu"])}</a>' for k in ('convert', 'lastcup', 'timer'))
    embed_src = BASE + PATH['embed'](lang)
    main = f'''<main id="main" class="wrap wrap-narrow tool-wrap">
<div><h1>{E(c['calc_h1'])}</h1><p class="lead" style="margin-top:10px">{E(c['calc_lead'])}</p></div>
<div id="calc" class="tool-cols" data-embed-src="{E(embed_src)}" data-title="{E(c['calc_h1'])}">
<div class="tool-in">
<div class="fld"><span class="fld-label">{E(c['l_tea'])}</span><div class="pills">{teas}</div></div>
<div class="fld-row">
<div class="fld"><span class="fld-label">{E(c['l_grams'])}</span><div class="stepper"><button type="button" data-act="g-dec" aria-label="−">−</button><output id="o-grams" style="min-width:84px">2 g</output><button type="button" data-act="g-inc" aria-label="+">+</button></div></div>
<div class="fld"><span class="fld-label">{E(c['l_water'])}</span><div class="stepper"><button type="button" data-act="w-dec" aria-label="−">−</button><output id="o-water" style="min-width:104px">250 ml</output><button type="button" data-act="w-inc" aria-label="+">+</button></div></div>
</div>
<div class="fld"><span class="fld-label">{E(c['l_time'])}</span><div class="seg seg-fit" role="group" aria-label="{E(c['l_time'])}">{times}</div></div>
</div>
<div class="tool-out">
<div><span class="eyebrow">{E(c['result'])}</span>
<div style="margin-top:6px"><span class="big" id="o-range">{lo}–{hi}</span> <span class="unit">mg</span></div>
<span class="per" id="o-per">≈ {fmt(a, lang)}–{fmt(b, lang)} mg / 100 ml</span></div>
<div class="bars"><span class="fld-label" style="color:var(--leaf)">{E(c['compare'])}</span>
<div><div class="bar-top"><span>{E(c['cup'])}</span><b id="bar-cup-v">{lo}–{hi} mg</b></div><div class="bar"><i class="me" id="bar-cup" style="width:{pct(mid)}"></i></div></div>
<div><div class="bar-top"><span>{E(c['espresso'])}</span><b>~{ESP} mg</b></div><div class="bar"><i style="width:{pct(ESP)}"></i></div></div>
<div><div class="bar-top"><span>{E(c['filter'])}</span><b>~{FIL} mg</b></div><div class="bar"><i style="width:{pct(FIL)}"></i></div></div></div>
<p class="tool-note">{E(c['tool_note'])}</p>
</div>
</div>
<section class="share" id="share" aria-labelledby="share-h">
<div class="share-top"><h2 id="share-h">{E(c['share_title'])}</h2>
<button class="btn btn-amber btn-sm" type="button" id="copy-btn" data-copy="{E(c['copy'])}" data-copied="{E(c['copied'])}">{svg('link', 18, '1.9')}<span id="copy-label">{E(c['copy'])}</span></button>
<button class="btn btn-outline btn-sm" type="button" id="embed-btn" aria-expanded="false" aria-controls="embed-panel" data-show="{E(c['embed'])}" data-hide="{E(c['embed_hide'])}">{svg('code', 18, '1.9')}<span id="embed-label">{E(c['embed'])}</span></button></div>
<div><span class="small">{E(c['link_note'])}</span><label class="sr-only" for="share-url">URL</label><input class="code" id="share-url" type="text" readonly value="{BASE}{PATH['calc'](lang)}"></div>
<div id="embed-panel" hidden><span class="small">{E(c['embed_note'])}</span><label class="sr-only" for="embed-code">iframe</label><textarea class="code code-dark" id="embed-code" rows="3" readonly></textarea></div>
</section>
{sources_html(lang)}
<div class="quiet"><span class="fld-label">{E(c['related'])}</span><div class="quiet-links">{related}</div><a class="quiet-guide" href="{PATH['home'](lang)}">{E(c['more_about'])}</a></div>
</main>'''
    return shell(lang, 'calc', c['calc_page_title'], c['calc_page_desc'], main, quiet_footer=True, slim=True, scripts=('calc.js',))


def embed_page(lang):
    c = C[lang]
    lo, hi = calc_defaults()
    mid = (lo + hi) / 2
    pct = rnd(mid / FIL * 100)
    pills = ''.join(
        f'<button type="button" data-tea="{tid}" data-lo="{l}" data-hi="{h}" data-whole="{w}" aria-pressed="{"true" if i == 0 else "false"}">{E(names[lang])}</button>'
        for i, (tid, l, h, w, names) in enumerate(t for t in TEAS if t[0] in EMBED_TEAS))
    full = BASE + PATH['calc'](lang)
    tools = BASE + PATH['tools'](lang)
    body = f'''<body class="is-embed">
<main class="embed" id="calc">
<div class="cc-head"><span class="cc-ico">{svg('calc', 20)}</span><span class="cc-title">{E(c['calc_h1'])}</span></div>
<div class="pills">{pills}</div>
<div class="row"><span class="row-label">{E(c['l_grams'])}</span><div class="stepper"><button type="button" data-act="g-dec" aria-label="−">−</button><output id="o-grams" style="min-width:64px;font-size:26px">2 g</output><button type="button" data-act="g-inc" aria-label="+">+</button></div></div>
<div class="res-box"><span class="eyebrow">{E(c['result'])}</span><div><span class="big" id="o-range">{lo}–{hi}</span> <span class="unit">mg</span></div><span class="per" id="o-vs" data-vs="{E(c['vs'])}">≈ {pct}% {E(c['vs'])}</span></div>
<span class="fine">{E(c['embed_note_s'])}</span>
<div class="embed-foot"><a class="b" href="{full}" target="_blank" rel="noopener">{E(c['credit'])} →</a><a class="m" href="{tools}" target="_blank" rel="noopener">{E(c['more_tools'])}</a></div>
</main>
<script src="/assets/calc.js" defer></script>
</body>
</html>
'''
    return head(lang, 'embed', c['embed_title'], c['calc_page_desc'], noindex=True) + '\n' + body


def privacy(lang):
    c = C[lang]
    parts = ''
    for tag, text in c['priv']:
        parts += f'<{tag}>{E(text)}</{tag}>'
    main = f'<main id="main" class="wrap prose">{parts}</main>'
    return shell(lang, 'privacy', c['priv_title'], c['priv_desc'], main, quiet_footer=True, slim=True, noindex=True)


def write(path, content):
    full = os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


def cache_bust():
    """CSS/JS nuorodoms prideda ?v=<turinio maiša>, kad pakeitimai pasiektų lankytojus nelaukiant talpyklos galiojimo pabaigos."""
    import hashlib, re
    hashes = {}
    def h(name):
        if name not in hashes:
            p = os.path.join(OUT, 'assets', name)
            hashes[name] = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8] if os.path.exists(p) else ''
        return hashes[name]
    pat = re.compile(r'(/assets/)([\w.-]+\.(?:css|js))(?=["\'])')
    for root, _, files in os.walk(OUT):
        for fn in files:
            if fn.endswith('.html'):
                p = os.path.join(root, fn)
                t = open(p, encoding='utf-8').read()
                t2 = pat.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={h(m.group(2))}' if h(m.group(2)) else m.group(0), t)
                if t2 != t:
                    open(p, 'w', encoding='utf-8').write(t2)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(HERE, 'static'), OUT)
    for lang in LANGS:
        write(PATH['home'](lang) + 'index.html', home(lang))
        write(PATH['tools'](lang) + 'index.html', tools_hub(lang))
        write(PATH['calc'](lang) + 'index.html', calc_page(lang))
        write(PATH['embed'](lang) + 'index.html', embed_page(lang))
        write(PATH['privacy'](lang) + 'index.html', privacy(lang))
    for _p, _h in TG.pages(__import__('sys').modules[__name__]):
        write(_p, _h)
    write('/assets/data.js', caff.data_js())
    import seo_gen as SG
    for _p, _h in SG.pages(__import__('sys').modules[__name__]):
        write(_p, _h)
    for _p, _h in _BG.pages(__import__('sys').modules[__name__]):
        write(_p, _h)
    for _p, _h in _BR.pages(__import__('sys').modules[__name__]):
        write(_p, _h)
    for _p, _h in _TL.pages(__import__('sys').modules[__name__]):
        write(_p, _h)
    for _p, _h in _RG.pages(__import__('sys').modules[__name__]):
        write(_p, _h)

    # šaknis: nukreipia pagal naršyklės kalbą
    write('/index.html', f'''<!doctype html>
<html lang="lt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arbata</title>
<link rel="canonical" href="{BASE}/lt/">
<noscript><meta http-equiv="refresh" content="0; url=/lt/"></noscript>
<script>var l=(navigator.language||'lt').slice(0,2).toLowerCase();location.replace(l==='en'?'/en/':l==='it'?'/it/':'/lt/');</script>
</head><body><p><a href="/lt/">Lietuvių</a> · <a href="/en/">English</a> · <a href="/it/">Italiano</a></p></body></html>
''')

    # sitemap (be įterpiamų puslapių ir privatumo)
    urls = ''
    import seo_gen as SG
    for key in ('home', 'tools', 'calc') + tuple(TG.ORDER) + tuple(SG.all_keys()) + tuple(_BG.all_keys()) + tuple(_BR.all_keys()) + tuple(_TL.all_keys()) + tuple(_RG.all_keys()):
        for lang in langs_of(key):
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{PATH[key](l)}"/>' for l in langs_of(key))
            lm = _BG.lastmod(key, lang)
            lm = f'<lastmod>{lm}</lastmod>' if lm else ''
            urls += f'<url><loc>{BASE}{PATH[key](lang)}</loc>{lm}{alts}</url>\n'
    write('/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    write('/robots.txt', f'User-agent: *\nDisallow: /_data/\nDisallow: /stats/\nDisallow: /a.php\nSitemap: {BASE}/sitemap.xml\n')
    cache_bust()
    print('OK', sum(len(f) for _, _, f in os.walk(OUT)), 'failų')


if __name__ == '__main__':
    main()
