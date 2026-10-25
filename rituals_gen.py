"""Receptai ir ritualai (LT/EN/IT): hub + 5 puslapiai. PATH raktai: hub_r, r_<id>.
Kofeino skaičiai imami iš caff.py (tealib_gen.D); ko šaltiniai nepatvirtina (pvz. kofeinas šalto užpilo arbatoje), nerašome."""
import json
import caff
import seo_gen as SG
import tealib_gen as TL
import rituals_more as RM

DIR = {'lt': 'ritualai', 'en': 'rituals', 'it': 'rituali'}
IDS = ['cold', 'matcha', 'rooibos', 'morning', 'break'] + RM.IDS
SLUG = {
    'cold': {'lt': 'salto-uzpilo-arbata', 'en': 'cold-brew-tea', 'it': 'te-cold-brew'},
    'matcha': {'lt': 'matcha-latte', 'en': 'matcha-latte', 'it': 'matcha-latte'},
    'rooibos': {'lt': 'rooibos-latte', 'en': 'rooibos-latte', 'it': 'rooibos-latte'},
    'morning': {'lt': 'ryto-ritualas-be-kavos', 'en': 'morning-ritual-without-coffee', 'it': 'rituale-del-mattino-senza-caffe'},
    'break': {'lt': 'kavos-pertraukos-pakaitalas', 'en': 'coffee-break-swap', 'it': 'pausa-caffe-alternativa'},
}
SLUG.update(RM.SLUG)
SRC = {
    'takeout': ('The Takeout: Maybe don\'t make sun tea this summer (cold brewing in the fridge vs warm sun tea)', 'https://thetakeout.com/what-is-sun-tea-how-to-make-food-safety-vs-cold-brew-1850570516'),
}


def key_r(i): return 'r_' + i


def register(B):
    B.PATH['hub_r'] = lambda l: f'/{l}/{DIR[l]}/'
    for i in IDS:
        B.PATH[key_r(i)] = (lambda i: lambda l: f'/{l}/{DIR[l]}/{SLUG[i][l]}/')(i)


def all_keys():
    return ['hub_r'] + [key_r(i) for i in IDS]


def source(k):
    return SRC[k] if k in SRC else TL.source(k)


def rg(i):
    d = TL.D(i)
    return f'{d["lo"]}–{d["hi"]} mg'


def typ(i): return TL.D(i)['typ']


# ---------- tekstai ----------
UI = {
 'lt': dict(hub='Receptai ir ritualai', home='Pagrindinis', h_ing='Ko reikės', h_steps='Kaip gaminti', h_caf='Kiek kofeino', h_tips='Patarimai',
            h_faq='Dažni klausimai', h_more='Taip pat naudinga', h_src='Šaltiniai', all_r='Visi receptai ir ritualai',
            note='Kofeino skaičiai iš mūsų duomenų bazės (patikrinta {d}); jie priklauso nuo arbatos ir plikymo. Bendra informacija, ne medicininė konsultacija. Receptų kiekiai yra tiesiog pradinė vieta, derink pagal skonį.',
            hub_t='Receptai ir ritualai: šalto užpilo arbata, matcha latte, ryto rutina vietoj kavos', hub_d='Praktiniai receptai ir ritualai, padedantys pakeisti kavą arbata: šalto užpilo arbata, matcha ir rooibos latte, ryto ir pertraukos rutinos su kofeino skaičiais.',
            hub_h1='Receptai ir ritualai vietoj kavos', hub_lead='Kava dažnai yra ne tik kofeinas, bet ir ritualas: karštas puodelis rankose, pertrauka, pradėta diena. Čia receptai ir rutinos, kurios užpildo tą vietą, o kofeino kiekį rodome iš savo duomenų bazės su šaltiniais.',
            h_rec='Receptai', h_rit='Ritualai', rit_note='Čia idėjos, ne taisyklės: svarbiausia pasirinkti tai, ką iš tikrųjų darysi.'),
 'en': dict(hub='Recipes and rituals', home='Home', h_ing='What you need', h_steps='How to make it', h_caf='How much caffeine', h_tips='Tips',
            h_faq='FAQ', h_more='Also useful', h_src='Sources', all_r='All recipes and rituals',
            note='Caffeine figures come from our database (checked {d}) and vary with the tea and brewing. General information, not medical advice. Amounts in recipes are only a starting point; adjust to taste.',
            hub_t='Recipes and rituals: cold brew tea, matcha latte, a morning routine instead of coffee', hub_d='Practical recipes and rituals for swapping coffee for tea: cold brew tea, matcha and rooibos lattes, morning and break routines, with caffeine figures.',
            hub_h1='Recipes and rituals instead of coffee', hub_lead='Coffee is often more than caffeine: a hot cup in your hands, a break, a day getting started. Here are recipes and routines that fill that place, with caffeine figures from our sourced database.',
            h_rec='Recipes', h_rit='Rituals', rit_note='These are ideas, not rules: pick what you will actually do.'),
 'it': dict(hub='Ricette e rituali', home='Home', h_ing='Cosa serve', h_steps='Come si prepara', h_caf='Quanta caffeina', h_tips='Consigli',
            h_faq='Domande frequenti', h_more='Può servire anche', h_src='Fonti', all_r='Tutte le ricette e i rituali',
            note='I valori di caffeina vengono dal nostro database (verificato {d}) e variano con il tè e l’infusione. Informazioni generali, non consulenza medica. Le quantità delle ricette sono un punto di partenza: regola a gusto.',
            hub_t='Ricette e rituali: tè cold brew, matcha latte, routine del mattino senza caffè', hub_d='Ricette e rituali pratici per sostituire il caffè con il tè: tè cold brew, matcha e rooibos latte, routine del mattino e della pausa, con i valori di caffeina.',
            hub_h1='Ricette e rituali al posto del caffè', hub_lead='Il caffè è spesso più della caffeina: una tazza calda tra le mani, una pausa, l’inizio della giornata. Qui ricette e routine che riempiono quel posto, con valori di caffeina dal nostro database con fonti.',
            h_rec='Ricette', h_rit='Rituali', rit_note='Sono idee, non regole: scegli ciò che farai davvero.'),
}


def page_data(lang):
    d = _page_data(lang)
    d.update(RM.data(lang))
    return d


def _page_data(lang):
    b, g, m, f = rg('black'), rg('green'), rg('matcha'), rg('filter')
    c200 = 200 // typ('black')
    if lang == 'lt':
        return {
         'cold': dict(
            name='Šalto užpilo arbata', h1='Šalto užpilo arbata: kaip pasigaminti namuose', kind='r',
            desc='Šalto užpilo (cold brew) arbatos receptas: kiek arbatos, kiek laiko laikyti šaldytuve ir ką žinoma apie kofeiną.',
            ans='Apie 8 g arbatos užpilk litru šalto vandens, palik šaldytuve 6–12 valandų, nukošk ir gerk su ledu. Kofeino šalto užpilo arbatoje patikimai nenurodome: mūsų skaičiai (juodoji ' + b + ', žalioji ' + g + ' puodelyje) skirti karštam užpilui.',
            ing=['Apie 8 g birių arbatos lapų arba 4 maišeliai litrui vandens (tiek pat arbatos puodeliui, kiek naudojame skaičiavimuose: 2 g / 237 ml)', '1 litras šalto filtruoto vandens', 'Pasirinktinai: citrina, mėta, ledas'],
            steps=['Pasirink arbatą: juodoji, žalioji ar baltoji turi kofeino, rooibos ir žolelių arbatos paprastai neturi.', 'Suberk arbatą į stiklinį ąsotį ir užpilk šaltu vandeniu.', 'Uždenk ir palik šaldytuve 6–12 valandų. Per ilgai laikyta arbata gali tapti kartesnė, todėl pirmą kartą paragauk po 6 valandų.', 'Nukošk lapus ar išimk maišelius.', 'Laikyk šaldytuve ir išgerk per 1–2 dienas. Patiekk su ledu, citrinos griežinėliu ar mėtų lapeliu.'],
            caf='Mūsų duomenų bazės skaičiai (juodoji ' + b + ', žalioji ' + g + ' vienam puodeliui) gauti karštu užpilu. Patikimų duomenų, kiek kofeino išsiskiria šaltame vandenyje, neradome, todėl nežadame, kad šaltas užpilas turi mažiau. Jei seki kofeiną, laikyk jį tokiu pat kaip karšto puodelio.',
            tips=['Laikyk šaldytuve, ne virtuvės stalo ar saulės: šiltoje vietoje stovintis užpilas ilgiau būna temperatūrų zonoje, kur dauginasi bakterijos (žr. šaltinį).', 'Ruošk iš vakaro: ryte jau paruošta, tai lengvas pirmas žingsnis nuo kavos.', 'Skonį derink laiku ir arbatos kiekiu, ne vandens šiluma.'],
            faq=[('Ar šalto užpilo arbatoje mažiau kofeino?', 'Patikimų duomenų neradome, todėl to nežadame. Skaičiuok kaip karštą puodelį.'), ('Kiek laiko galima laikyti?', 'Šaldytuve, uždengtą, 1–2 dienas. Tai bendras virtuvės patarimas, ne standartas.'), ('Kokia arbata tinka?', 'Tinka juodoji, žalioji, baltoji, rooibos ir žolelių arbatos; ką pasirinksi, ta turės arba neturės kofeino.')],
            links=['tl_black', 'tl_green', 'tl_herbal', 'calc', 'timer'], src=['takeout', 'mayo', 'foods']),
         'matcha': dict(
            name='Matcha latte', h1='Matcha latte: receptas ir kofeinas', kind='r',
            desc='Matcha latte receptas su kofeino skaičiais: kiek matcha, koks vanduo ir kiek kofeino puodelyje, palyginti su kava.',
            ans='2 g matcha suplak su ~60 ml 80–90 °C vandens, pilk šilto pieno ar augalinio gėrimo. Kofeino porcijoje ' + m + ' (tipinė ' + str(typ('matcha')) + ' mg): mažiau nei filtruotos kavos puodelyje (' + f + '), bet daugiau nei juodosios arbatos (' + b + ').',
            ing=['2 g matcha (apie pusė arbatinio šaukštelio)', '~60 ml 80–90 °C vandens', '150–200 ml pieno ar augalinio gėrimo', 'Pasirinktinai: saldiklis'],
            steps=['Matcha perkošk per sietelį, kad nebūtų gumulėlių.', 'Užpilk karštu (ne verdančiu) vandeniu ir suplak šluotele ar nedideliu plakikliu iki putų.', 'Pašildyk pieną ar augalinį gėrimą ir supilk į matcha.', 'Pasaldink pagal skonį.'],
            caf='Matcha geriama kartu su lapų milteliais, todėl kofeino daugiau nei paprastos žaliosios arbatos užpile. Mūsų duomenimis, porcijoje (2 g, ~200 ml) yra ' + m + ' (tipinė ' + str(typ('matcha')) + ' mg), todėl laikas ir dydis svarbūs, jei ją renkiesi vietoj kavos.',
            tips=['Karštas, bet ne verdantis vanduo mažiau kartina.', 'Jei nori vakare, rinkis rooibos latte (be kofeino).', 'Matcha kokybė labai skiriasi, todėl skaičiuok su diapazonu, ne tipine reikšme.'],
            faq=[('Kiek kofeino matcha latte?', 'Pagal mūsų duomenų bazę 2 g matcha porcijoje ' + m + '.'), ('Ar matcha stipresnė už kavą?', 'Paprastai ne: filtruotos kavos puodelyje ' + f + ', matcha porcijoje ' + m + '.')],
            links=['tl_matcha', 'd_matcha', 'calc', 'compare'], src=['matcha', 'wp_matcha', 'mayo']),
         'rooibos': dict(
            name='Rooibos latte', h1='Rooibos latte: šiltas gėrimas be kofeino', kind='r',
            desc='Rooibos latte receptas be kofeino: stipriai užplikyta rooibos su šiltu pienu ar augaliniu gėrimu, vakarui ir pertraukai.',
            ans='Stipriai užplikyk rooibos (dvigubai daugiau arbatos nei įprastai), sumaišyk su šiltu pienu ar augaliniu gėrimu ir pagardink cinamonu ar vanile. Rooibos natūraliai neturi kofeino, todėl tinka ir vakarui.',
            ing=['Apie 4 g rooibos 200 ml vandens (dvigubai daugiau nei įprastam puodeliui)', '100–150 ml pieno ar augalinio gėrimo', 'Pasirinktinai: cinamono lazdelė, vanilė, medus'],
            steps=['Užplikyk rooibos verdančiu vandeniu ir palik ilgiau nei įprastai (pagal pakuotę), kad užpilas būtų stiprus.', 'Pašildyk pieną ar augalinį gėrimą ir išplak iki putų.', 'Sumaišyk su rooibos, pagal skonį pridėk cinamono ar vanilės.'],
            caf='Rooibos natūraliai neturi kofeino. Vis dėlto pirkdamas aromatizuotą mišinį pasitikrink pakuotę, nes į jį gali būti įdėta arbatos su kofeinu.',
            tips=['Gera idėja vakarui, kai nenori kofeino.', 'Šildyk pieną atsargiai, kad neprisviltų.'],
            faq=[('Ar rooibos latte turi kofeino?', 'Pati rooibos neturi. Jei dedi kitos arbatos ar kavos, kofeino atsiras.'), ('Ar tinka kavos pakaitalu ryte?', 'Skonis kitoks, bet ritualas tas pats: šiltas puodelis su pienu. Kofeino neduos, todėl rytą gali pasirinkti ir matcha ar juodąją.')],
            links=['tl_rooibos', 'tl_herbal', 'plan', 'convert'], src=['wp_rooibos', 'ci_herbal']),
         'morning': dict(
            name='Ryto ritualas', h1='Ryto ritualas be kavos: kaip pradėti dieną su arbata', kind='t',
            desc='Kaip pakeisti rytinę kavą arbata: pirmo puodelio pakeitimas, kofeino skaičiai ir paprastas ritualas.',
            ans='Pirmiausia pakeisk tik rytinį puodelį: filtruotos kavos puodelyje ' + f + ', juodosios arbatos ' + b + ', žaliosios ' + g + ', matcha ' + m + '. Puodelis, laikas ir 10 minučių be ekrano padaro rutiną ritualu.',
            ing=['Tas pats puodelis kasdien', 'Arbata, kurią pasirinksi (pradžiai juodoji ar matcha)', '10 minučių ryto pradžioje'],
            steps=['Išsiaiškink, kiek kofeino šiuo metu gauni: kofeino skaičiuoklė parodo dienos sumą.', 'Pakeisk pirmą puodelį: tai paprastai lengviausia, nes prie jo labiausiai pripratai.', 'Kasdien gerk tuo pačiu metu ir iš to paties puodelio; prie arbatos pridėk 10 minučių be telefono, jei gali.', 'Po savaitės pakeisk antrą puodelį. Jei nori palaipsniui, naudok plano įrankį.'],
            caf='EFSA nurodo, kad suaugusiam saugu iki 400 mg kofeino per dieną, o vienu metu iki 200 mg. 200 mg yra apie ' + str(c200) + ' puodelių juodosios arbatos pagal mūsų tipinę reikšmę (' + str(typ('black')) + ' mg). Pusinės eliminacijos laikas siekia 3–7 val.',
            tips=['Pirmosiomis dienomis galimas galvos skausmas ar mieguistumas: apie tai straipsnyje apie kavos abstinenciją.', 'Nesitaikyk iš karto į nulį: palaipsnis mažinimas lengvesnis.'],
            faq=[('Nuo ko pradėti keisti kavą arbata?', 'Nuo vieno puodelio ryte. Kai pripras, keisk kitus.'), ('Kokia arbata artimiausia kavai?', 'Pagal kofeiną artimiausia matcha (' + m + ') arba yerba mate; skonis skiriasi.')],
            links=['calc', 'plan', 'convert', 'quiz', 'b_mesti-kava', 'b_abstinencija', 'b_kava-ar-arbata-ryte'], src=['efsa', 'mayo', 'matcha']),
         'break': dict(
            name='Pertraukos pakaitalas', h1='Kavos pertraukos pakaitalas: ką gerti vietoj popietinės kavos', kind='t',
            desc='Ką gerti vietoj popietinės kavos: rooibos, žolelių arbata, šalto užpilo arbata ir kaip nepakenkti miegui kofeino riba.',
            ans='Popietinę kavą pakeisk šiltu gėrimu be kofeino (rooibos, žolelių arbata) arba šaltu užpilu. Kofeino pusinės eliminacijos laikas 3–7 val., todėl vėlai gerta kava dar likusi vakare.',
            ing=['Du ar trys gėrimai, kuriuos gali paruošti darbe', 'Puodelis, kuris tau patinka', '10 minučių pertraukai'],
            steps=['Pasirink 2–3 gėrimus be kofeino ar su mažai: rooibos, žolelių arbata, šalto užpilo žalioji arbata.', 'Paruošk iš anksto, kad nereikėtų eiti prie kavos aparato.', 'Eik pasivaikščioti ar pakalbėk su kolega, kol geri: pertrauka, o ne tik gėrimas.', 'Naudok „paskutinio puodelio“ įrankį, kad žinotum, kada geriausia baigti kofeiną.'],
            caf='Rooibos ir daugumoje žolelių arbatų kofeino nėra, juodoji ' + b + ', žalioji ' + g + '. Kofeino pusinės eliminacijos laikas 3–7 val., todėl po pietų išgertas kofeinas gali likti iki vakaro.',
            tips=['Jei popietė sunki, pirmiausia atsisakyk paskutinio kavos puodelio, ne pirmojo.', 'Šalto užpilo arbata gerai tinka darbo dienai: paruošta iš vakaro.'],
            faq=[('Kada nutraukti kofeiną per dieną?', 'Tai priklauso nuo žmogaus; kofeinas lieka 3–7 val. pusinės eliminacijos laiku. Paskutinio puodelio įrankis padeda įvertinti.'), ('Kuo pakeisti popietinę kavą?', 'Rooibos latte, žolelių arbata arba šalto užpilo arbata.')],
            links=['tl_rooibos', 'tl_herbal', 'r_cold', 'r_rooibos', 'lastcup', 'tracker'], src=['efsa', 'mayo', 'wp_rooibos']),
        }
    if lang == 'en':
        return {
         'cold': dict(
            name='Cold brew tea', h1='Cold brew tea: how to make it at home', kind='r',
            desc='Cold brew tea recipe: how much tea, how long in the fridge and what is known about caffeine.',
            ans='Put about 8 g of tea into a litre of cold water, leave it in the fridge for 6–12 hours, strain and serve over ice. We do not give a caffeine figure for cold brewed tea: our numbers (black ' + b + ', green ' + g + ' per cup) are for hot brewing.',
            ing=['About 8 g loose tea or 4 tea bags per litre (the same amount per cup we use in calculations: 2 g per 237 ml)', '1 litre cold filtered water', 'Optional: lemon, mint, ice'],
            steps=['Choose a tea: black, green or white contain caffeine; rooibos and herbal teas usually do not.', 'Put the tea in a glass jug and cover with cold water.', 'Cover and refrigerate for 6–12 hours. Tea left too long can turn bitter, so taste after 6 hours the first time.', 'Strain out the leaves or remove the bags.', 'Keep it refrigerated and finish within 1–2 days. Serve over ice with lemon or mint.'],
            caf='Our database figures (black ' + b + ', green ' + g + ' per cup) are for hot brewing. We found no reliable data on how much caffeine cold water extracts from tea, so we do not claim cold brew has less. If you track caffeine, count it like a hot cup.',
            tips=['Keep it in the fridge, not on the counter or in the sun: warm tea spends longer in the temperature range where bacteria grow (see source).', 'Make it the evening before: it is ready in the morning, a good first step away from coffee.', 'Adjust taste with time and amount, not heat.'],
            faq=[('Does cold brew tea have less caffeine?', 'We found no reliable data, so we do not promise that. Count it like a hot cup.'), ('How long does it keep?', 'Covered in the fridge for 1–2 days. That is general kitchen advice, not a standard.'), ('Which tea works?', 'Black, green, white, rooibos and herbal teas all work; the caffeine depends on the tea you choose.')],
            links=['tl_black', 'tl_green', 'tl_herbal', 'calc', 'timer'], src=['takeout', 'mayo', 'foods']),
         'matcha': dict(
            name='Matcha latte', h1='Matcha latte: recipe and caffeine', kind='r',
            desc='Matcha latte recipe with caffeine figures: how much matcha, what water and how much caffeine per cup compared with coffee.',
            ans='Whisk 2 g of matcha with ~60 ml of 80–90 °C water and add warm milk or a plant drink. A serving has ' + m + ' of caffeine (typical ' + str(typ('matcha')) + ' mg): less than a cup of filter coffee (' + f + ') but more than black tea (' + b + ').',
            ing=['2 g matcha (about half a teaspoon)', '~60 ml water at 80–90 °C', '150–200 ml milk or plant drink', 'Optional: sweetener'],
            steps=['Sift the matcha to avoid lumps.', 'Add hot (not boiling) water and whisk with a bamboo whisk or small frother until foamy.', 'Warm the milk or plant drink and pour into the matcha.', 'Sweeten to taste.'],
            caf='You drink the leaf powder with matcha, so there is more caffeine than in an ordinary green tea infusion. In our data a serving (2 g, ~200 ml) has ' + m + ' (typical ' + str(typ('matcha')) + ' mg), so size and timing matter if you pick it instead of coffee.',
            tips=['Hot but not boiling water is less bitter.', 'For the evening choose rooibos latte (no caffeine).', 'Matcha quality varies a lot, so count with the range, not the typical value.'],
            faq=[('How much caffeine is in a matcha latte?', 'In our database a serving with 2 g matcha has ' + m + '.'), ('Is matcha stronger than coffee?', 'Usually not: a cup of filter coffee has ' + f + ', a matcha serving ' + m + '.')],
            links=['tl_matcha', 'd_matcha', 'calc', 'compare'], src=['matcha', 'wp_matcha', 'mayo']),
         'rooibos': dict(
            name='Rooibos latte', h1='Rooibos latte: a warm drink without caffeine', kind='r',
            desc='Caffeine-free rooibos latte recipe: strong rooibos with warm milk or a plant drink, for evenings and breaks.',
            ans='Brew rooibos strong (twice the usual amount of tea), mix with warm milk or a plant drink and add cinnamon or vanilla. Rooibos naturally contains no caffeine, so it also works in the evening.',
            ing=['About 4 g rooibos per 200 ml water (twice a usual cup)', '100–150 ml milk or plant drink', 'Optional: cinnamon stick, vanilla, honey'],
            steps=['Brew the rooibos with boiling water and leave it longer than usual (see the pack) so it is strong.', 'Warm the milk or plant drink and froth it.', 'Combine with the rooibos and add cinnamon or vanilla to taste.'],
            caf='Rooibos naturally contains no caffeine. When buying a flavoured blend, check the pack: it may include tea with caffeine.',
            tips=['A good evening alternative to coffee when you want no caffeine.', 'Warm milk gently so it does not scorch.'],
            faq=[('Does rooibos latte contain caffeine?', 'Rooibos itself does not. If you add other tea or coffee, caffeine appears.'), ('Does it work as a morning coffee swap?', 'The taste differs but the ritual is the same: a warm cup with milk. It gives no caffeine, so in the morning you may prefer matcha or black tea.')],
            links=['tl_rooibos', 'tl_herbal', 'plan', 'convert'], src=['wp_rooibos', 'ci_herbal']),
         'morning': dict(
            name='Morning ritual', h1='A morning ritual without coffee: starting the day with tea', kind='t',
            desc='How to swap morning coffee for tea: replacing the first cup, caffeine figures and a simple ritual.',
            ans='Replace only the morning cup first: a cup of filter coffee has ' + f + ', black tea ' + b + ', green tea ' + g + ', matcha ' + m + '. The same cup, the same time and 10 minutes without a screen turn a routine into a ritual.',
            ing=['The same cup every day', 'A tea of your choice (black or matcha to start)', '10 minutes at the start of the morning'],
            steps=['Find out how much caffeine you get now: the caffeine calculator shows the daily total.', 'Replace the first cup: it is usually the easiest, because it is where the habit is strongest.', 'Drink at the same time from the same cup; add 10 minutes without your phone if you can.', 'After a week replace the second cup. For a gradual plan use the planner tool.'],
            caf='EFSA says up to 400 mg of caffeine a day and up to 200 mg at one time is safe for adults. 200 mg is about ' + str(c200) + ' cups of black tea at our typical value (' + str(typ('black')) + ' mg). Caffeine has a half-life of 3–7 hours.',
            tips=['In the first days you may get a headache or sleepiness: see the article on caffeine withdrawal.', 'Do not aim for zero at once: a gradual reduction is easier.'],
            faq=[('Where do I start swapping coffee for tea?', 'With one cup in the morning. When it becomes a habit, swap the next.'), ('Which tea is closest to coffee?', 'By caffeine, matcha (' + m + ') or yerba mate; the taste differs.')],
            links=['calc', 'plan', 'convert', 'quiz', 'b_mesti-kava', 'b_abstinencija', 'b_kava-ar-arbata-ryte'], src=['efsa', 'mayo', 'matcha']),
         'break': dict(
            name='Coffee break swap', h1='A coffee break swap: what to drink instead of afternoon coffee', kind='t',
            desc='What to drink instead of afternoon coffee: rooibos, herbal tea, cold brew tea, and the caffeine half-life.',
            ans='Swap the afternoon coffee for a warm caffeine-free drink (rooibos, herbal tea) or a cold brew. Caffeine has a half-life of 3–7 hours, so late coffee is still partly in your body in the evening.',
            ing=['Two or three drinks you can prepare at work', 'A cup you like', '10 minutes for a break'],
            steps=['Pick 2–3 drinks with no or little caffeine: rooibos, herbal tea, cold brew green tea.', 'Prepare ahead so you do not walk to the coffee machine.', 'Take a short walk or chat with a colleague while you drink: a break, not just a drink.', 'Use the last-cup tool to see when to stop caffeine.'],
            caf='Rooibos and most herbal teas contain no caffeine; black tea has ' + b + ', green ' + g + '. With a half-life of 3–7 hours, caffeine drunk after lunch can remain into the evening.',
            tips=['If the afternoon is hard, drop the last coffee first, not the first.', 'Cold brew tea suits a workday: made the evening before.'],
            faq=[('When should I stop caffeine in the day?', 'It depends on the person; caffeine stays for a half-life of 3–7 hours. The last-cup tool helps estimate.'), ('What can replace afternoon coffee?', 'Rooibos latte, herbal tea or cold brew tea.')],
            links=['tl_rooibos', 'tl_herbal', 'r_cold', 'r_rooibos', 'lastcup', 'tracker'], src=['efsa', 'mayo', 'wp_rooibos']),
        }
    return {
     'cold': dict(
        name='Tè cold brew', h1='Tè cold brew: come prepararlo a casa', kind='r',
        desc='Ricetta del tè cold brew: quanto tè, quante ore in frigo e cosa si sa sulla caffeina.',
        ans='Metti circa 8 g di tè in un litro di acqua fredda, lascia in frigo 6–12 ore, filtra e servi con ghiaccio. Non indichiamo un valore di caffeina per il cold brew: i nostri numeri (nero ' + b + ', verde ' + g + ' a tazza) valgono per l’infusione calda.',
        ing=['Circa 8 g di foglie sfuse o 4 bustine per litro (la stessa quantità per tazza che usiamo nei calcoli: 2 g per 237 ml)', '1 litro di acqua fredda filtrata', 'Facoltativo: limone, menta, ghiaccio'],
        steps=['Scegli un tè: nero, verde o bianco contengono caffeina; rooibos e tisane di solito no.', 'Metti il tè in una caraffa di vetro e copri con acqua fredda.', 'Copri e conserva in frigo 6–12 ore. Un’infusione troppo lunga può diventare più amara, quindi la prima volta assaggia dopo 6 ore.', 'Filtra le foglie o togli le bustine.', 'Conserva in frigo e consuma entro 1–2 giorni. Servi con ghiaccio, limone o menta.'],
        caf='I valori del nostro database (nero ' + b + ', verde ' + g + ' a tazza) riguardano l’infusione calda. Non abbiamo trovato dati affidabili su quanta caffeina estragga l’acqua fredda, quindi non diciamo che il cold brew ne abbia meno. Se monitori la caffeina, contalo come una tazza calda.',
        tips=['Tienilo in frigo, non sul tavolo o al sole: il tè tiepido resta più a lungo nell’intervallo di temperatura in cui crescono i batteri (vedi fonte).', 'Preparalo la sera prima: al mattino è pronto, un buon primo passo lontano dal caffè.', 'Regola il gusto con tempo e quantità, non con il calore.'],
        faq=[('Il tè cold brew ha meno caffeina?', 'Non abbiamo trovato dati affidabili, quindi non lo promettiamo. Contalo come una tazza calda.'), ('Quanto si conserva?', 'Coperto in frigo 1–2 giorni. È un consiglio generale di cucina, non uno standard.'), ('Quale tè va bene?', 'Nero, verde, bianco, rooibos e tisane; la caffeina dipende dal tè scelto.')],
        links=['tl_black', 'tl_green', 'tl_herbal', 'calc', 'timer'], src=['takeout', 'mayo', 'foods']),
     'matcha': dict(
        name='Matcha latte', h1='Matcha latte: ricetta e caffeina', kind='r',
        desc='Ricetta del matcha latte con valori di caffeina: quanto matcha, che acqua e quanta caffeina a porzione rispetto al caffè.',
        ans='Sbatti 2 g di matcha con ~60 ml di acqua a 80–90 °C e aggiungi latte caldo o bevanda vegetale. Una porzione ha ' + m + ' di caffeina (tipico ' + str(typ('matcha')) + ' mg): meno di una tazza di caffè filtrato (' + f + ') ma più del tè nero (' + b + ').',
        ing=['2 g di matcha (circa mezzo cucchiaino)', '~60 ml di acqua a 80–90 °C', '150–200 ml di latte o bevanda vegetale', 'Facoltativo: dolcificante'],
        steps=['Setaccia il matcha per evitare i grumi.', 'Aggiungi acqua calda (non bollente) e sbatti con la frusta di bambù o un piccolo montalatte fino alla schiuma.', 'Scalda il latte o la bevanda vegetale e versa sul matcha.', 'Dolcifica a piacere.'],
        caf='Con il matcha si beve la polvere di foglia, quindi la caffeina è più di una normale infusione di tè verde. Nei nostri dati una porzione (2 g, ~200 ml) ha ' + m + ' (tipico ' + str(typ('matcha')) + ' mg), perciò quantità e orario contano se lo scegli al posto del caffè.',
        tips=['Acqua calda ma non bollente è meno amara.', 'Per la sera scegli un rooibos latte (senza caffeina).', 'La qualità del matcha varia molto: conta con l’intervallo, non con il valore tipico.'],
        faq=[('Quanta caffeina ha un matcha latte?', 'Nel nostro database una porzione con 2 g di matcha ha ' + m + '.'), ('Il matcha è più forte del caffè?', 'Di solito no: una tazza di caffè filtrato ha ' + f + ', una porzione di matcha ' + m + '.')],
        links=['tl_matcha', 'd_matcha', 'calc', 'compare'], src=['matcha', 'wp_matcha', 'mayo']),
     'rooibos': dict(
        name='Rooibos latte', h1='Rooibos latte: una bevanda calda senza caffeina', kind='r',
        desc='Ricetta del rooibos latte senza caffeina: rooibos forte con latte caldo o bevanda vegetale, per sera e pause.',
        ans='Prepara il rooibos forte (il doppio del tè consueto), mescola con latte caldo o bevanda vegetale e aggiungi cannella o vaniglia. Il rooibos è naturalmente privo di caffeina, quindi va bene anche la sera.',
        ing=['Circa 4 g di rooibos per 200 ml di acqua (il doppio di una tazza normale)', '100–150 ml di latte o bevanda vegetale', 'Facoltativo: stecca di cannella, vaniglia, miele'],
        steps=['Prepara il rooibos con acqua bollente e lascialo in infusione più a lungo del solito (vedi confezione) per renderlo forte.', 'Scalda il latte o la bevanda vegetale e montalo.', 'Unisci al rooibos e aggiungi cannella o vaniglia a gusto.'],
        caf='Il rooibos è naturalmente privo di caffeina. Se compri una miscela aromatizzata, controlla la confezione: potrebbe contenere tè con caffeina.',
        tips=['Un buon sostituto serale del caffè quando non vuoi caffeina.', 'Scalda il latte con delicatezza per non bruciarlo.'],
        faq=[('Il rooibos latte contiene caffeina?', 'Il rooibos no. Se aggiungi altro tè o caffè, la caffeina compare.'), ('Va bene al posto del caffè al mattino?', 'Il gusto cambia ma il rituale è lo stesso: una tazza calda con latte. Non dà caffeina, quindi al mattino puoi preferire matcha o tè nero.')],
        links=['tl_rooibos', 'tl_herbal', 'plan', 'convert'], src=['wp_rooibos', 'ci_herbal']),
     'morning': dict(
        name='Rituale del mattino', h1='Rituale del mattino senza caffè: iniziare la giornata con il tè', kind='t',
        desc='Come sostituire il caffè del mattino con il tè: la prima tazza, i valori di caffeina e un rituale semplice.',
        ans='Sostituisci prima solo la tazza del mattino: il caffè filtrato ha ' + f + ', il tè nero ' + b + ', il verde ' + g + ', il matcha ' + m + '. La stessa tazza, lo stesso orario e 10 minuti senza schermo trasformano una routine in un rituale.',
        ing=['La stessa tazza ogni giorno', 'Un tè a tua scelta (nero o matcha per iniziare)', '10 minuti all’inizio della mattina'],
        steps=['Scopri quanta caffeina assumi ora: il calcolatore mostra il totale giornaliero.', 'Sostituisci la prima tazza: di solito è la più facile, perché lì l’abitudine è più forte.', 'Bevi alla stessa ora dalla stessa tazza; se puoi, aggiungi 10 minuti senza telefono.', 'Dopo una settimana sostituisci la seconda tazza. Per un piano graduale usa lo strumento di pianificazione.'],
        caf='L’EFSA indica che fino a 400 mg di caffeina al giorno e fino a 200 mg in una volta sono sicuri per gli adulti. 200 mg sono circa ' + str(c200) + ' tazze di tè nero al nostro valore tipico (' + str(typ('black')) + ' mg). L’emivita della caffeina è di 3–7 ore.',
        tips=['Nei primi giorni possono comparire mal di testa o sonnolenza: vedi l’articolo sull’astinenza da caffeina.', 'Non puntare subito allo zero: ridurre gradualmente è più facile.'],
        faq=[('Da dove iniziare a sostituire il caffè con il tè?', 'Da una tazza al mattino. Quando diventa un’abitudine, sostituisci la successiva.'), ('Quale tè è più vicino al caffè?', 'Per caffeina il matcha (' + m + ') o la yerba mate; il gusto è diverso.')],
        links=['calc', 'plan', 'convert', 'quiz', 'b_mesti-kava', 'b_abstinencija', 'b_kava-ar-arbata-ryte'], src=['efsa', 'mayo', 'matcha']),
     'break': dict(
        name='Alternativa alla pausa caffè', h1='Alternativa alla pausa caffè: cosa bere al posto del caffè pomeridiano', kind='t',
        desc='Cosa bere al posto del caffè del pomeriggio: rooibos, tisane, tè cold brew e l’emivita della caffeina.',
        ans='Sostituisci il caffè del pomeriggio con una bevanda calda senza caffeina (rooibos, tisana) o un cold brew. L’emivita della caffeina è di 3–7 ore, quindi un caffè tardi è ancora in parte nel corpo la sera.',
        ing=['Due o tre bevande che puoi preparare al lavoro', 'Una tazza che ti piace', '10 minuti per la pausa'],
        steps=['Scegli 2–3 bevande senza o con poca caffeina: rooibos, tisana, tè verde cold brew.', 'Preparale prima, così non vai alla macchinetta.', 'Fai due passi o parla con un collega mentre bevi: una pausa, non solo una bevanda.', 'Usa lo strumento dell’ultima tazza per capire quando smettere con la caffeina.'],
        caf='Rooibos e la maggior parte delle tisane non hanno caffeina; il tè nero ha ' + b + ', il verde ' + g + '. Con un’emivita di 3–7 ore, la caffeina bevuta dopo pranzo può restare fino a sera.',
        tips=['Se il pomeriggio è duro, elimina prima l’ultimo caffè, non il primo.', 'Il tè cold brew è ottimo per la giornata di lavoro: preparato la sera prima.'],
        faq=[('Quando smettere con la caffeina durante il giorno?', 'Dipende dalla persona; la caffeina resta per un’emivita di 3–7 ore. Lo strumento dell’ultima tazza aiuta a stimare.'), ('Cosa sostituisce il caffè del pomeriggio?', 'Rooibos latte, tisana o tè cold brew.')],
        links=['tl_rooibos', 'tl_herbal', 'r_cold', 'r_rooibos', 'lastcup', 'tracker'], src=['efsa', 'mayo', 'wp_rooibos']),
    }


def label(B, key, lang):
    if key.startswith('r_'):
        return page_data(lang)[key[2:]]['name']
    if key == 'hub_r':
        return UI[lang]['hub']
    import blog_gen
    if key.startswith('b_'):
        return blog_gen.POSTS[key[2:]][lang]['title']
    return blog_gen.page_label(B, key, lang)


def jsonld(B, lang, key, name, faqs):
    t = UI[lang]
    crumbs = [(t['home'], B.BASE + B.PATH['home'](lang)), (t['hub'], B.BASE + B.PATH['hub_r'](lang))]
    if key != 'hub_r':
        crumbs.append((name, B.BASE + B.PATH[key](lang)))
    out = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'name': a, 'item': u} for n, (a, u) in enumerate(crumbs)]}]
    if faqs:
        out.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]})
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>' for o in out)


def src_block(B, lang, keys):
    E = B.E
    t = UI[lang]
    items = ''.join(f'<li><a href="{source(k)[1]}" target="_blank" rel="noopener nofollow">{E(source(k)[0])}</a></li>' for k in dict.fromkeys(keys))
    return f'<section class="seo-sec"><h2>{E(t["h_src"])}</h2><ul class="small srclist">{items}</ul><p class="small">{E(t["note"].format(d=caff.CHECKED))}</p></section>'


def page(B, i, lang):
    E = B.E
    t = UI[lang]
    p = page_data(lang)[i]
    ol = lambda xs: '<ol>' + ''.join(f'<li>{E(x)}</li>' for x in xs) + '</ol>'
    ul = lambda xs: '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in xs) + '</ul>'
    links = ''.join(f'<a href="{B.PATH[k](lang)}">{E(label(B, k, lang))}</a>' for k in p['links'])
    key = key_r(i)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <a href="{B.PATH['hub_r'](lang)}">{E(t['hub'])}</a> / <span>{E(p['name'])}</span></div>
<h1 class="page-title">{E(p['h1'])}</h1>
<div class="answer"><p class="answer-main">{E(p['ans'])}</p></div>
<section class="seo-sec"><h2>{E(t['h_ing'])}</h2>{ul(p['ing'])}</section>
<section class="seo-sec"><h2>{E(t['h_steps'])}</h2>{ol(p['steps'])}</section>
<section class="seo-sec"><h2>{E(t['h_caf'])}</h2><p>{E(p['caf'])}</p></section>
<section class="seo-sec"><h2>{E(t['h_tips'])}</h2>{ul(p['tips'])}</section>
{SG.faq_html(B, lang, p['faq']).replace(SG.L[lang]['h_faq'], t['h_faq'], 1)}
<section class="seo-sec"><h2>{E(t['h_more'])}</h2><div class="quiet-links"><a href="{B.PATH['hub_r'](lang)}">{E(t['all_r'])}</a>{links}</div></section>
{src_block(B, lang, p['src'])}
</main>
{jsonld(B, lang, key, p['name'], p['faq'])}'''
    return B.shell(lang, key, p['h1'] + ' | ' + t['hub'] if len(p['h1']) < 50 else p['h1'], p['desc'], main)


def hub_page(B, lang):
    E = B.E
    t = UI[lang]
    pd = page_data(lang)
    def cards(kind):
        return ''.join(f'<a class="lib-card" href="{B.PATH[key_r(i)](lang)}"><span class="lib-name">{E(pd[i]["name"])}</span><span class="lib-taste">{E(pd[i]["desc"])}</span></a>' for i in IDS if pd[i]['kind'] == kind)
    main = f'''<main id="main" class="wrap wrap-narrow seo">
<div class="crumbs"><a href="{B.PATH['home'](lang)}">{E(t['home'])}</a> / <span>{E(t['hub'])}</span></div>
<h1 class="page-title">{E(t['hub_h1'])}</h1><p class="lead">{E(t['hub_lead'])}</p>
<section class="seo-sec"><h2>{E(t['h_rec'])}</h2><div class="lib-grid">{cards('r')}</div></section>
<section class="seo-sec"><h2>{E(t['h_rit'])}</h2><p>{E(t['rit_note'])}</p><div class="lib-grid">{cards('t')}</div></section>
<section class="seo-sec"><div class="quiet-links"><a href="{B.PATH['hub_t'](lang)}">{E(label(B, 'hub_t', lang))}</a><a href="{B.PATH['calc'](lang)}">{E(label(B, 'calc', lang))}</a><a href="{B.PATH['plan'](lang)}">{E(label(B, 'plan', lang))}</a><a href="{B.PATH['blog'](lang)}">{E(B.C[lang]['nav_blog'])}</a></div></section>
{src_block(B, lang, ['efsa', 'mayo', 'matcha'])}
</main>
{jsonld(B, lang, 'hub_r', t['hub'], [])}'''
    return B.shell(lang, 'hub_r', t['hub_t'], t['hub_d'], main)


def pages(B):
    register(B)
    out = []
    for lang in B.LANGS:
        out.append((B.PATH['hub_r'](lang) + 'index.html', hub_page(B, lang)))
        for i in IDS:
            out.append((B.PATH[key_r(i)](lang) + 'index.html', page(B, i, lang)))
    return out
