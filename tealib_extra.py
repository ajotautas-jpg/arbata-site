"""Bibliotekos papildomos rūšys (rooibos, žolelių arbatos, sencha, hojicha, geltonoji, Earl Grey).
Kofeinas čia NE iš caff.py skaičiavimų: kur šaltinis skaičiaus nepateikia, rodoma „nerasta“, o ne spėjimas.
Kiekvienas teiginys turi šaltinį (SRC raktai, žr. tealib_gen.SRC)."""

IDS = ['rooibos', 'herbal', 'sencha', 'hojicha', 'yellow', 'earlgrey']

NAMES = {
    'rooibos': dict(slug={'lt': 'rooibos', 'en': 'rooibos', 'it': 'rooibos'},
                    nom={'lt': 'Rooibos', 'en': 'Rooibos', 'it': 'Rooibos'},
                    inn={'lt': 'rooibos arbatoje', 'en': 'rooibos', 'it': 'nel rooibos'},
                    gen={'lt': 'rooibos', 'en': 'rooibos', 'it': 'il rooibos'}),
    'herbal': dict(slug={'lt': 'zoleliu-arbata', 'en': 'herbal-tea', 'it': 'tisane'},
                   nom={'lt': 'Žolelių arbatos', 'en': 'Herbal teas', 'it': 'Tisane'},
                   inn={'lt': 'žolelių arbatose', 'en': 'herbal teas', 'it': 'nelle tisane'},
                   gen={'lt': 'žolelių arbatas', 'en': 'herbal tea', 'it': 'le tisane'}),
    'sencha': dict(slug={'lt': 'sencha', 'en': 'sencha', 'it': 'sencha'},
                   nom={'lt': 'Sencha', 'en': 'Sencha', 'it': 'Sencha'},
                   inn={'lt': 'sencha arbatoje', 'en': 'sencha', 'it': 'nel sencha'},
                   gen={'lt': 'sencha', 'en': 'sencha', 'it': 'il sencha'}),
    'hojicha': dict(slug={'lt': 'hojicha', 'en': 'hojicha', 'it': 'hojicha'},
                    nom={'lt': 'Hojicha', 'en': 'Hojicha', 'it': 'Hojicha'},
                    inn={'lt': 'hojicha arbatoje', 'en': 'hojicha', 'it': 'nell\'hojicha'},
                    gen={'lt': 'hojicha', 'en': 'hojicha', 'it': 'l\'hojicha'}),
    'yellow': dict(slug={'lt': 'geltonoji-arbata', 'en': 'yellow-tea', 'it': 'te-giallo'},
                   nom={'lt': 'Geltonoji arbata', 'en': 'Yellow tea', 'it': 'Tè giallo'},
                   inn={'lt': 'geltonojoje arbatoje', 'en': 'yellow tea', 'it': 'nel tè giallo'},
                   gen={'lt': 'geltonąją arbatą', 'en': 'yellow tea', 'it': 'il tè giallo'}),
    'earlgrey': dict(slug={'lt': 'earl-grey', 'en': 'earl-grey', 'it': 'earl-grey'},
                     nom={'lt': 'Earl Grey', 'en': 'Earl Grey', 'it': 'Earl Grey'},
                     inn={'lt': 'Earl Grey arbatoje', 'en': 'Earl Grey', 'it': 'nell\'Earl Grey'},
                     gen={'lt': 'Earl Grey', 'en': 'Earl Grey', 'it': 'l\'Earl Grey'}),
}

# kofeino vertės: kind 'zero' (0 mg), 'range' (lo-hi mg puodelyje, įvertis), 'per100' (mg/100 ml, gamintojo), 'none' (skaičiaus nerasta), 'base' (kaip juodosios arbatos pagrindas)
CAF = {
    'rooibos': dict(kind='zero'),
    'herbal': dict(kind='zero'),
    'sencha': dict(kind='range', lo=20, hi=30),
    'hojicha': dict(kind='per100', v=20),
    'yellow': dict(kind='none'),
    'earlgrey': dict(kind='base'),
}

# plikymas: (temperatūra °C arba None, laikas min. arba None)
BREW = {
    'rooibos': (None, None), 'herbal': (None, None), 'sencha': ('80', '1'),
    'hojicha': (None, None), 'yellow': (None, None), 'earlgrey': (None, '2–3'),
}

SRC = {
    'rooibos': ['wp_rooibos', 'ci_herbal'],
    'herbal': ['wp_herbal', 'ci_herbal'],
    'sencha': ['wp_sencha'],
    'hojicha': ['yama_hojicha'],
    'yellow': ['wp_yellow'],
    'earlgrey': ['wp_earlgrey', 'mayo'],
}

BRAND_TYPES = {'herbal': ('herbal',)}

# turinys: kind (trumpai), made, taste, brew, caf (kofeino paaiškinimas puslapyje), more (pastaba), f3q/f3a (trečias DUK)
X = {
 'lt': {
  'rooibos': dict(
    kind='Ne arbata, o žolelių užpilas be kofeino',
    made='Gaminamas iš Aspalathus linearis, pupinių šeimos krūmo. Jis auga Pietų Afrikoje, Vakarų Kyšulio provincijoje, dažniausiai Cederbergo kalnuose. Tai ne arbatmedis (Camellia sinensis), todėl rooibos priskiriamas žolelių užpilams. Lapai dažniausiai oksiduojami: dėl to užpilas būna rausvai rudas. Žalias (neoksiduotas) rooibos taip pat gaminamas, bet jo gamyba brangesnė.',
    taste='Oksidacija suteikia rausvai rudą spalvą ir sustiprina skonį, todėl oksiduotas ir žalias rooibos skiriasi. Konkretesnio skonio aprašo šaltiniuose neradome, todėl nerašome.',
    brew='Užpilamas karštu vandeniu, kaip juodoji arbata. Tikslios temperatūros ir laiko šaltiniuose neradome, todėl laikykis gamintojo nurodymų ant pakuotės.',
    caf='Šaltiniai aprašo rooibos kaip žolelių užpilą be kofeino: 0 mg puodelyje. Todėl jis neprisideda prie dienos kofeino sumos.',
    f3q='Ar rooibos skaičiuojasi į dienos kofeino ribą?',
    f3a='Ne. Rooibos aprašomas kaip kofeino neturintis užpilas, todėl jis nedidina dienos kofeino sumos (EFSA riba suaugusiajam: 400 mg per dieną).'),
  'herbal': dict(
    kind='Ne arbata: žolelių, gėlių, prieskonių ar vaisių užpilai',
    made='Žolelių arbatos (tisanes) gaminamos užpilant ar virinant žoleles, prieskonius ar kitas augalų dalis. Arbatos lapų jose nėra, todėl tai ne tikroji arbata: ji gaunama ne iš arbatmedžio (Camellia sinensis). Pavyzdžiai: ramunėlės ir pipirmėtės.',
    taste='Skonis priklauso nuo augalo. Šaltiniuose bendro skonio aprašo nėra.',
    brew='Augalo dalys užpilamos karštu ar verdančiu vandeniu ir paliekamos pritraukti. Temperatūra ir laikas priklauso nuo augalo dalies, todėl laikykis pakuotės nurodymų. Užpilant šaltu vandeniu, reikia kelių valandų.',
    caf='Dauguma žolelių užpilų kofeino neturi (apibendrinta vertė 0 mg puodelyje). Tačiau yra išimčių: guarana, yaupon ir yerba mate kofeino turi. Pakuotėse dar gali būti užteršimo kofeinu dėl bendros gamyklos, todėl patikrink sudėtį.',
    f3q='Ar visos žolelių arbatos be kofeino?',
    f3a='Ne visos. Dauguma jo neturi, bet guarana, yaupon ir yerba mate turi kofeino. Žiūrėk į sudėtį, ypač jei gėrimas pavadintas „energiniu“ ar „žvaliu“ mišiniu. Kai kurie augalai gali veikti su vaistais, todėl vartojantiems vaistus verta pasitarti su vaistininku ar gydytoju.'),
  'sencha': dict(
    kind='Japoniška garinta žalioji arbata',
    made='Sencha gaminama iš viršutinių Camellia sinensis lapų. Lapai 15–20 sekundžių garinami, kad sustotų oksidacija (kinų žaliosios arbatos vietoj to kepamos keptuvėje), tada formuojami į plonus cilindrus ir džiovinami. Sencha sudaro apie 80 % Japonijos arbatos gamybos.',
    taste='Šaltiniuose konkretaus skonio aprašo nėra. Žaliosios arbatos bendra taisyklė: per karštas vanduo ar per ilgas plikymas daro ją kartesnę.',
    brew='Apie 80 °C vanduo, apie 1 minutė.',
    caf='Wikipedia pateikia įvertį: apie 20–30 mg kofeino puodelyje. Pagal ten cituojamus matavimus sausuose lapuose yra apie 27–31 mg/g, o aukštesnė plikymo temperatūra išplauna daugiau kofeino.',
    f3q='Kodėl sencha plikoma vėsesniu vandeniu nei juodoji arbata?',
    f3a='Šaltiniai nurodo apie 80 °C ir apie 1 minutę. Be to, aukštesnė temperatūra išplauna daugiau kofeino, todėl vėsesnis vanduo tinka ir tiems, kurie nori mažiau kofeino.'),
  'hojicha': dict(
    kind='Skrudinta japoniška žalioji arbata',
    made='Hojicha gaminama skrudinant žaliąją arbatą, dažniausiai sencha ar bancha, aukšta temperatūra, kol ji paruduoja. Konkrečios skrudinimo temperatūros šaltinyje nėra.',
    taste='Konkretaus skonio aprašo šaltinyje nėra.',
    brew='Tikslios plikymo temperatūros ir laiko šaltiniuose neradome, todėl laikykis pakuotės nurodymų.',
    caf='Gamintojas Yamamotoyama nurodo apie 20 mg kofeino 100 ml užpilo, tiek pat kaip sencha. Palyginimui ten pat: juodoji arbata apie 30 mg, matcha apie 60 mg, bancha ir genmaicha po 10 mg. Gamintojas paaiškina, kad dalis kofeino skrudinant išgaruoja, o žaliava dažnai yra vėliau skinti lapai, iš kurių kofeinas sunkiau išsiplauna. Tai vieno gamintojo duomenys, ne nepriklausomas matavimas.',
    f3q='Ar hojicha turi mažiau kofeino nei kita žalioji arbata?',
    f3a='Pagal gamintojo duomenis hojicha ir sencha turi po apie 20 mg 100 ml, tad skirtumas nedidelis. Gamintojas teigia, kad giliau skrudinta hojicha gali turėti dar mažiau. Šių duomenų nepatikrino nepriklausomas šaltinis.'),
  'yellow': dict(
    kind='Šiek tiek oksiduota arbata iš Kinijos ir Korėjos',
    made='Geltonoji arbata gaminama kaip žalioji, tik papildomai atliekamas „tvyrinimas“ (angl. sweltering): šilti drėgni lapai uždaromi ir švelniai šildomi apie 6–8 val. maždaug kūno temperatūroje. Tai paverčia lapus geltonais ir padeda pašalinti žolinį žaliosios arbatos kvapą. Kinijoje gaminama Hunano, Anhui, Sičuano, Dzeziango, Gujdžou, Guangdongo ir Hubėjaus provincijose.',
    taste='Tvyrinimas keičia aminorūgštis ir polifenolius, todėl skonis gaunasi gaivus, bet švelnus. Kiniška versija duoda gelsvai žalią užpilą.',
    brew='Plikymo temperatūros šaltinyje nėra, todėl laikykis pakuotės nurodymų.',
    caf='Patikimo kofeino skaičiaus geltonajai arbatai neradome, todėl jo nerodome.',
    f3q='Kodėl geltonąją arbatą sunku rasti?',
    f3a='Kiniška geltonoji arbata aprašoma kaip vis rečiau gaminama ir brangi. Konkrečių kiekių šaltinis nenurodo.'),
  'earlgrey': dict(
    kind='Juodoji arbata su bergamotės aliejumi',
    made='Earl Grey yra arbatos mišinys, aromatizuotas bergamotės (citrusinio vaisiaus žievės) aliejumi. Tradiciškai pagrindas yra juodoji arbata, pavyzdžiui, kiniška keemun, kartais su lapsang souchong dūmų natoms. Egzistuoja ir žalios ar oolong arbatos variantai. Daug prekinių mišinių vietoj bergamotės aliejaus naudoja kitus natūralius ar dirbtinius aromatus.',
    taste='Pagrindinė skonio natą suteikia bergamotė. Variantai: Lady Grey (su rugiagėlių žiedais ar citrusais, Twinings prekės ženklas), Russian Earl Grey (su citrusų žievele ir citrinžole), French Earl Grey (su rožių žiedlapiais), Earl Grey Crème (su levandomis ir vanile).',
    brew='Apie 2–3 minutes; kai kas rekomenduoja iki 5 min. ryškesniam citrusų aromatui. Per ilgai palikta arbata tampa karti. Temperatūros šaltiniai nenurodo vienodai.',
    caf='Earl Grey dažniausiai yra juodoji arbata, todėl kofeiną lemia pagrindas. Mūsų duomenyse juodoji arbata turi {lo}–{hi} mg puodelyje. Variantai su žaliąja, balta ar oolong arbata skiriasi, o su rooibos pagrindu kofeino nėra. Šaltinyje atskiro Earl Grey kofeino skaičiaus nėra.',
    f3q='Ar Earl Grey turi daugiau kofeino nei juodoji arbata?',
    f3a='Atskiro Earl Grey skaičiaus šaltinis nenurodo. Kadangi tai dažniausiai juodoji arbata su aromatu, kofeiną lemia pagrindinė arbata. Pasižiūrėk į pakuotę: pagrindas gali būti ir žalioji, ir rooibos.'),
 },
 'en': {
  'rooibos': dict(
    kind='Not tea: a caffeine-free herbal infusion',
    made='Made from Aspalathus linearis, a broom-like legume that grows in South Africa\'s Western Cape, mostly in the Cederberg mountains. It is not the tea plant (Camellia sinensis), so rooibos counts as a herbal infusion. The leaves are usually oxidised, which gives the reddish-brown colour. Green (unoxidised) rooibos is also made, but it costs more to produce.',
    taste='Oxidation gives the red-brown colour and enhances the flavour, so oxidised and green rooibos differ. The sources give no more detailed taste description, so we do not write one.',
    brew='Steeped in hot water, like black tea. We found no exact temperature or time in the sources, so follow the packaging.',
    caf='The sources describe rooibos as a caffeine-free herbal infusion: 0 mg per cup. It therefore adds nothing to your daily caffeine total.',
    f3q='Does rooibos count towards the daily caffeine limit?',
    f3a='No. Rooibos is described as caffeine-free, so it does not add to your daily caffeine total (the EFSA limit for adults is 400 mg a day).'),
  'herbal': dict(
    kind='Not tea: infusions of herbs, flowers, spices or fruit',
    made='Herbal teas (tisanes) are made by steeping or simmering herbs, spices or other plant material in water. They contain no tea leaves, so they are not true tea: they do not come from the tea plant (Camellia sinensis). Examples are chamomile and peppermint.',
    taste='Taste depends on the plant. The sources give no general description.',
    brew='Hot or boiling water is poured over the plant parts and left to steep. Temperature and time vary with the plant part, so follow the packaging. Cold-water brewing takes several hours.',
    caf='Most herbal infusions contain no caffeine (the general figure is 0 mg per cup). There are exceptions: guarana, yaupon and yerba mate do contain caffeine. Products made in shared factories can also be contaminated slightly, so check the ingredients.',
    f3q='Are all herbal teas caffeine-free?',
    f3a='Not all. Most are, but guarana, yaupon and yerba mate contain caffeine. Check the ingredients, especially on blends sold as "energy" or "boost". Some herbs can interact with medicines, so if you take medication it is worth asking a pharmacist or doctor.'),
  'sencha': dict(
    kind='Japanese steamed green tea',
    made='Sencha is made from the upper leaves of Camellia sinensis. The leaves are steamed for 15–20 seconds to stop oxidation (Chinese green teas are pan-fired instead), then rolled into thin cylinders and dried. Sencha makes up about 80% of Japan\'s tea production.',
    taste='The sources give no specific taste description. A general rule for green tea: water that is too hot or steeping that is too long makes it more bitter.',
    brew='About 80 °C water for about 1 minute.',
    caf='Wikipedia gives an estimate of about 20–30 mg of caffeine per cup. In the measurements it cites, dry leaves hold roughly 27–31 mg/g, and a higher brewing temperature extracts more caffeine.',
    f3q='Why is sencha brewed with cooler water than black tea?',
    f3a='The sources give about 80 °C and about 1 minute. A higher temperature also extracts more caffeine, so cooler water suits people who want less.'),
  'hojicha': dict(
    kind='Roasted Japanese green tea',
    made='Hojicha is made by roasting green tea, usually sencha or bancha, over high heat until it turns brown. The source gives no specific roasting temperature.',
    taste='The source gives no specific taste description.',
    brew='We found no exact brewing temperature or time in the sources, so follow the packaging.',
    caf='The producer Yamamotoyama lists about 20 mg of caffeine per 100 ml, the same as sencha. For comparison, on the same page: black tea about 30 mg, matcha about 60 mg, bancha and genmaicha 10 mg each. The producer explains that some caffeine evaporates during roasting and that the raw material is often later-picked leaves, from which caffeine dissolves less. This is one producer\'s data, not an independent measurement.',
    f3q='Does hojicha have less caffeine than other green tea?',
    f3a='By the producer\'s figures hojicha and sencha both have about 20 mg per 100 ml, so the difference is small. The producer says deep-roasted hojicha may have even less. No independent source has checked these figures.'),
  'yellow': dict(
    kind='Lightly oxidised tea from China and Korea',
    made='Yellow tea follows the green tea process with one extra step, called "sweltering": warm, damp leaves are sealed in a container and gently heated for about 6–8 hours at close to body temperature. This turns them yellow and helps remove green tea\'s grassy smell. In China it is made in Hunan, Anhui, Sichuan, Zhejiang, Guizhou, Guangdong and Hubei.',
    taste='Sweltering changes the amino acids and polyphenols, giving a brisk yet mellow taste. Chinese yellow tea gives a yellowish-green liquor.',
    brew='The source gives no brewing temperature, so follow the packaging.',
    caf='We found no reliable caffeine figure for yellow tea, so we do not show one.',
    f3q='Why is yellow tea hard to find?',
    f3a='Chinese yellow tea is described as increasingly rare and expensive. The source gives no figures.'),
  'earlgrey': dict(
    kind='Black tea flavoured with bergamot oil',
    made='Earl Grey is a tea blend flavoured with oil of bergamot, a citrus oil from the bergamot orange rind. The base is traditionally black tea, such as Chinese keemun, sometimes with lapsang souchong for a smoky note. Green and oolong versions exist too. Many commercial blends use other natural or artificial flavours instead of bergamot oil.',
    taste='Bergamot gives the main flavour note. Variants: Lady Grey (with cornflower or citrus, a Twinings trademark), Russian Earl Grey (citrus peel and lemongrass), French Earl Grey (rose petals), Earl Grey Crème (lavender and vanilla).',
    brew='About 2–3 minutes; some recommend up to 5 minutes for more citrus aroma. Over-steeping makes it bitter. Sources do not agree on temperature.',
    caf='Earl Grey is usually black tea, so the base tea decides the caffeine. In our data black tea has {lo}–{hi} mg per cup. Versions on green, white or oolong tea differ, and a rooibos base has no caffeine. The source gives no separate Earl Grey caffeine figure.',
    f3q='Does Earl Grey have more caffeine than black tea?',
    f3a='The source gives no separate Earl Grey figure. Since it is usually black tea with flavouring, the base tea decides the caffeine. Check the packaging: the base can also be green tea or rooibos.'),
 },
 'it': {
  'rooibos': dict(
    kind='Non è tè: infuso d\'erbe senza caffeina',
    made='Si ricava dall\'Aspalathus linearis, un arbusto della famiglia delle leguminose che cresce in Sudafrica, nella Provincia del Capo Occidentale, soprattutto sulle montagne Cederberg. Non è la pianta del tè (Camellia sinensis), quindi il rooibos è un infuso d\'erbe. Le foglie di solito sono ossidate, e questo dà il colore rosso-bruno. Esiste anche il rooibos verde (non ossidato), ma costa di più.',
    taste='L\'ossidazione dà il colore rosso-bruno e rafforza il sapore, quindi il rooibos ossidato e quello verde sono diversi. Le fonti non danno una descrizione più precisa del gusto, quindi non ne scriviamo una.',
    brew='Si prepara in acqua calda, come il tè nero. Nelle fonti non abbiamo trovato temperatura e tempo precisi: segui la confezione.',
    caf='Le fonti descrivono il rooibos come un infuso d\'erbe senza caffeina: 0 mg per tazza. Quindi non aggiunge nulla al totale giornaliero di caffeina.',
    f3q='Il rooibos conta nel limite giornaliero di caffeina?',
    f3a='No. Il rooibos è descritto come privo di caffeina, quindi non aumenta il totale giornaliero (limite EFSA per gli adulti: 400 mg al giorno).'),
  'herbal': dict(
    kind='Non è tè: infusi di erbe, fiori, spezie o frutta',
    made='Le tisane si preparano mettendo in infusione o facendo bollire erbe, spezie o altre parti di piante in acqua. Non contengono foglie di tè, quindi non sono tè vero: non derivano dalla pianta del tè (Camellia sinensis). Esempi: camomilla e menta piperita.',
    taste='Il gusto dipende dalla pianta. Le fonti non danno una descrizione generale.',
    brew='Le parti della pianta si coprono con acqua calda o bollente e si lasciano in infusione. Temperatura e tempo variano secondo la parte della pianta: segui la confezione. In acqua fredda servono diverse ore.',
    caf='La maggior parte degli infusi d\'erbe non contiene caffeina (valore generale: 0 mg per tazza). Ci sono eccezioni: guaranà, yaupon e yerba mate contengono caffeina. I prodotti fatti in stabilimenti condivisi possono inoltre avere una lieve contaminazione, quindi controlla gli ingredienti.',
    f3q='Tutte le tisane sono senza caffeina?',
    f3a='Non tutte. La maggior parte lo è, ma guaranà, yaupon e yerba mate contengono caffeina. Controlla gli ingredienti, soprattutto nei miscugli venduti come "energia" o "carica". Alcune erbe possono interagire con i farmaci: se prendi farmaci, chiedi a un farmacista o al medico.'),
  'sencha': dict(
    kind='Tè verde giapponese cotto al vapore',
    made='Il sencha si ricava dalle foglie superiori della Camellia sinensis. Le foglie sono cotte al vapore per 15–20 secondi per fermare l\'ossidazione (i tè verdi cinesi sono invece tostati in padella), poi arrotolate in sottili cilindri ed essiccate. Il sencha è circa l\'80% della produzione di tè in Giappone.',
    taste='Le fonti non danno una descrizione precisa del gusto. Regola generale per il tè verde: acqua troppo calda o infusione troppo lunga lo rendono più amaro.',
    brew='Acqua a circa 80 °C per circa 1 minuto.',
    caf='Wikipedia riporta una stima di circa 20–30 mg di caffeina per tazza. Nelle misure citate le foglie secche contengono circa 27–31 mg/g, e una temperatura più alta estrae più caffeina.',
    f3q='Perché il sencha si prepara con acqua meno calda del tè nero?',
    f3a='Le fonti indicano circa 80 °C e circa 1 minuto. Inoltre una temperatura più alta estrae più caffeina, quindi l\'acqua meno calda va bene per chi ne vuole meno.'),
  'hojicha': dict(
    kind='Tè verde giapponese tostato',
    made='L\'hojicha si ottiene tostando a fuoco alto un tè verde, di solito sencha o bancha, finché diventa marrone. La fonte non indica una temperatura di tostatura.',
    taste='La fonte non dà una descrizione precisa del gusto.',
    brew='Nelle fonti non abbiamo trovato temperatura e tempo precisi: segui la confezione.',
    caf='Il produttore Yamamotoyama indica circa 20 mg di caffeina per 100 ml, come il sencha. Per confronto, nella stessa pagina: tè nero circa 30 mg, matcha circa 60 mg, bancha e genmaicha 10 mg ciascuno. Il produttore spiega che parte della caffeina evapora durante la tostatura e che la materia prima è spesso fatta di foglie raccolte più tardi, da cui la caffeina si scioglie meno. Sono dati di un solo produttore, non una misura indipendente.',
    f3q='L\'hojicha ha meno caffeina di altri tè verdi?',
    f3a='Secondo i dati del produttore hojicha e sencha hanno circa 20 mg per 100 ml, quindi la differenza è piccola. Il produttore dice che l\'hojicha tostato a fondo può averne ancora meno. Nessuna fonte indipendente ha verificato questi valori.'),
  'yellow': dict(
    kind='Tè leggermente ossidato di Cina e Corea',
    made='Il tè giallo segue il processo del tè verde con un passaggio in più, detto "sweltering": le foglie calde e umide vengono chiuse in un contenitore e riscaldate dolcemente per circa 6–8 ore a una temperatura vicina a quella corporea. Questo le fa ingiallire e aiuta a eliminare l\'odore erbaceo del tè verde. In Cina si produce in Hunan, Anhui, Sichuan, Zhejiang, Guizhou, Guangdong e Hubei.',
    taste='Il passaggio cambia amminoacidi e polifenoli e dà un gusto vivace ma morbido. Il tè giallo cinese dà un infuso verde-giallastro.',
    brew='La fonte non indica la temperatura: segui la confezione.',
    caf='Non abbiamo trovato un valore affidabile di caffeina per il tè giallo, quindi non ne mostriamo uno.',
    f3q='Perché il tè giallo è difficile da trovare?',
    f3a='Il tè giallo cinese è descritto come sempre più raro e costoso. La fonte non dà cifre.'),
  'earlgrey': dict(
    kind='Tè nero aromatizzato all\'olio di bergamotto',
    made='L\'Earl Grey è una miscela di tè aromatizzata con olio di bergamotto, un olio di agrumi ricavato dalla scorza. La base è tradizionalmente tè nero, come il keemun cinese, a volte con lapsang souchong per una nota affumicata. Esistono anche versioni con tè verde o oolong. Molte miscele commerciali usano altri aromi naturali o artificiali al posto dell\'olio di bergamotto.',
    taste='Il bergamotto dà la nota principale. Varianti: Lady Grey (con fiordaliso o agrumi, marchio Twinings), Russian Earl Grey (scorza di agrumi e citronella), French Earl Grey (petali di rosa), Earl Grey Crème (lavanda e vaniglia).',
    brew='Circa 2–3 minuti; alcuni consigliano fino a 5 minuti per un aroma più agrumato. Un\'infusione troppo lunga lo rende amaro. Le fonti non concordano sulla temperatura.',
    caf='L\'Earl Grey è di solito tè nero, quindi la caffeina dipende dalla base. Nei nostri dati il tè nero ha {lo}–{hi} mg per tazza. Le versioni con tè verde, bianco o oolong cambiano, e con base rooibos non c\'è caffeina. La fonte non dà un valore separato per l\'Earl Grey.',
    f3q='L\'Earl Grey ha più caffeina del tè nero?',
    f3a='La fonte non dà un valore separato. Poiché di solito è tè nero aromatizzato, la caffeina dipende dalla base. Controlla la confezione: la base può essere anche tè verde o rooibos.'),
 },
}
