"""Goethe-Zertifikat A2 — the official task shapes, in-house material.

Structure taken from the published Modellsatz Erwachsene (2016, Vs5.1):

    Lesen   30 min · 4 Teile · 20 items
            Teil 1  items 1–5    three options on a newspaper portrait       8 min
            Teil 2  items 6–10   department-store directory: which floor?    7 min
                                 two floors or "anderer Stock"
            Teil 3  items 11–15  three options on a personal email           7 min
            Teil 4  items 16–20  six people → adverts a–f; one has none (X),
                                 the example's advert is used up             8 min
    Hören   30 min · 4 Teile · 20 items
            Teil 1  items 1–5    five short texts (radio, answerphone,
                                 announcements), each heard twice, a/b/c
            Teil 2  items 6–10   one conversation, heard once: which picture
                                 a–i goes with which day; each letter once
            Teil 3  items 11–15  five short conversations, each heard once,
                                 three pictures a/b/c
            Teil 4  items 16–20  a radio interview, heard twice, Ja/Nein
    Schreiben 30 min · 2 Teile
            Teil 1  an SMS to a friend, 20–30 words, three points           12 min
            Teil 2  a semi-formal email, 30–40 words, three points          18 min

Worked examples (Beispiel 0) appear where the paper prints them: Lesen 1, 2
and 4, Hören 2 and 4. The wording is Lexora's own; only the format follows
the model set. `manage.py make_a2_bilder` draws the Hören pictures and
`manage.py make_hoeren_audio --only a2` renders the recordings.
"""

AUDIO = "/media/exams/a2/hoeren"
BILD = "/media/exams/a2/bilder"

ABC = "abc"
YES_NO = [("ja", "Ja"), ("nein", "Nein")]


def abc(*texts):
    """Three written options, keyed a/b/c."""
    return [(key, text) for key, text in zip(ABC, texts)]


def bilder(*rows):
    """Three picture options: `(caption, file stem)` → a/b/c with an image."""
    return [(key, caption, f"{BILD}/{stem}.svg") for key, (caption, stem) in zip(ABC, rows)]


def floors(first, second):
    """Lesen 2 always offers two floors and "anderer Stock"."""
    return abc(first, second, "anderer Stock")


LESEN = {
    "skill": "lesen",
    "duration": 30,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "چهار بخش، ۲۰ سؤال، ۳۰ دقیقه: یک مقاله روزنامه، تابلوی راهنمای فروشگاه، یک ایمیل و "
        "آگهی‌های اینترنتی. هر سؤال فقط یک جواب درست دارد.",
        "Four parts, 20 items, 30 minutes: a newspaper article, a store directory, an email "
        "and internet adverts. Every item has exactly one correct answer.",
        "Dieser Prüfungsteil hat vier Teile: Sie lesen eine E-Mail, Informationen und Artikel "
        "aus der Zeitung und dem Internet. Für jede Aufgabe gibt es nur eine richtige Lösung.",
    ),
    "parts": [
        # ---------------------------------------------------------- Teil 1
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "این متن را در یک روزنامه می‌خوانید. برای سؤال‌های ۱ تا ۵ جواب درست a، b یا c "
                "را انتخاب کنید.",
                "You read this text in a newspaper. Choose the right answer a, b or c for "
                "items 1 to 5.",
                "Sie lesen in einer Zeitung diesen Text. "
                "Wählen Sie für die Aufgaben 1 bis 5 die richtige Lösung a, b oder c.",
            ),
            "stimulus_title": "Die Fahrrad-Ärztin kommt vor die Haustür",
            "stimulus_subtitle": "»Ich arbeite lieber auf der Straße als in einem Laden.« "
                                 "Die Mechanikerin Aylin Kaya",
            "blocks": [
                ("paragraph", "", "",
                 "Wenn bei Aylin Kaya das Telefon klingelt, hat meistens jemand einen Platten. "
                 "Die 34-Jährige repariert Fahrräder – aber nicht in einer Werkstatt. Sie fährt "
                 "mit ihrem Lastenrad direkt zu den Kunden, vor die Haustür oder ins Büro. "
                 "Einen Termin bekommt man nur über ihre Internetseite, und oft ist die Woche "
                 "schon voll. Ein eigenes Geschäft möchte sie trotzdem nicht aufmachen. „Dann "
                 "sitze ich den ganzen Tag drinnen. Ich bin gern draußen und lerne jeden Tag "
                 "neue Leute kennen.“\n\n"
                 "Aylin Kaya ist in Dresden aufgewachsen. Nach dem Abitur hat sie zuerst "
                 "Informatik studiert, aber nach zwei Semestern aufgehört. „Das war nichts "
                 "für mich. Ich wollte etwas mit den Händen machen.“ Sie hat dann eine "
                 "Ausbildung als Zweiradmechanikerin gemacht und danach sechs Jahre in einer "
                 "großen Werkstatt in Leipzig gearbeitet.\n\n"
                 "Die Idee mit dem Lastenrad hatte sie bei dieser Arbeit: Viele Kunden hatten "
                 "keine Zeit, ihr Rad in die Werkstatt zu bringen. Seit drei Jahren ist sie "
                 "nun selbstständig.\n\n"
                 "Die meisten Menschen kennen sie aber durch ihre Videos im Internet. Dort "
                 "zeigt sie jede Woche, wie man kleine Reparaturen selbst machen kann. Über "
                 "200 000 Menschen sehen regelmäßig zu."),
            ],
            "example_prompt": "Aylin Kaya repariert Fahrräder … → b) direkt bei den Kunden.",
            "example_answer": "b",
            "items": [
                (1, "Einen Termin bei Aylin Kaya …",
                 abc("bekommt man immer sofort.", "macht man im Internet.",
                     "macht man am Telefon."), "b",
                 ("«Einen Termin bekommt man nur über ihre Internetseite» — تلفن فقط برای شروع "
                  "متن آمده است.",
                  "Appointments are only made through her website; the phone is a distractor.",
                  "„Einen Termin bekommt man nur über ihre Internetseite.“")),
                (2, "Aylin Kaya möchte …",
                 abc("bald ein Geschäft eröffnen.", "lieber draußen arbeiten.",
                     "weniger Kunden haben."), "b",
                 ("«Ich bin gern draußen» و مغازه نمی‌خواهد.",
                  "She wants no shop: \"Ich bin gern draußen.\"",
                  "„Ein eigenes Geschäft möchte sie trotzdem nicht aufmachen … Ich bin gern "
                  "draußen.“")),
                (3, "Nach dem Abitur …",
                 abc("hat sie sofort eine Ausbildung gemacht.",
                     "hat sie in einer Werkstatt gearbeitet.",
                     "war sie kurz an der Universität."), "c",
                 ("اول دو ترم انفورماتیک خواند، بعد آموزش فنی دید.",
                  "She first studied computer science for two semesters.",
                  "„Nach dem Abitur hat sie zuerst Informatik studiert, aber nach zwei "
                  "Semestern aufgehört.“")),
                (4, "Viele Menschen kennen Aylin Kaya durch …",
                 abc("ihre Videos.", "ihre Werkstatt in Leipzig.", "ein Buch über Fahrräder."),
                 "a",
                 ("«Die meisten Menschen kennen sie aber durch ihre Videos im Internet».",
                  "Most people know her from her online videos.",
                  "„Die meisten Menschen kennen sie aber durch ihre Videos im Internet.“")),
                (5, "Dieser Text informiert über …",
                 abc("eine neue Ausbildung.", "den Berufsweg einer Mechanikerin.",
                     "das Fahrradfahren in Leipzig."), "b",
                 ("متن از تحصیل تا کار مستقل او را تعریف می‌کند.",
                  "The text follows her career from school to self-employment.",
                  "Der Text erzählt ihren Weg von der Schule bis zur Selbstständigkeit.")),
            ],
        },
        # ---------------------------------------------------------- Teil 2
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "تابلوی راهنمای یک فروشگاه بزرگ را می‌خوانید. سؤال‌های ۶ تا ۱۰ و متن را "
                "بخوانید. به کدام طبقه می‌روید؟ جواب درست a، b یا c را انتخاب کنید.",
                "You read the directory in a department store. Read items 6 to 10 and the "
                "text. Which floor do you go to? Choose a, b or c.",
                "Sie lesen die Informationstafel in einem Kaufhaus. "
                "Lesen Sie die Aufgaben 6 bis 10 und den Text. In welchen Stock gehen Sie? "
                "Wählen Sie die richtige Lösung a, b oder c.",
            ),
            "stimulus_title": "Kaufhaus Brenner",
            "stimulus_subtitle": "Wegweiser",
            "blocks": [
                ("row", "4. Stock", "",
                 "Restaurant mit Dachterrasse, Friseur, Kundenservice und Umtausch, "
                 "Geschenkverpackung, Kunden-WC"),
                ("row", "3. Stock", "",
                 "Computer, Handys, Tablets, Fernseher, Kameras, Drucker, Videospiele, Musik "
                 "und Filme, Handyreparatur"),
                ("row", "2. Stock", "",
                 "Möbel, Betten, Lampen, Teppiche, Bettwäsche, Handtücher, Küchengeräte, "
                 "Geschirr und Gläser"),
                ("row", "1. Stock", "",
                 "Damenmode, Herrenmode, Kindermode, Sportbekleidung, Sportschuhe, Koffer "
                 "und Reisetaschen"),
                ("row", "EG", "",
                 "Information, Parfümerie, Kosmetik, Schmuck, Uhren, Handtaschen, Bücher, "
                 "Zeitschriften, Schreibwaren, Glückwunschkarten"),
                ("row", "UG", "",
                 "Supermarkt, Bäckerei, Getränke, Drogerie, Blumen, Schlüsseldienst, "
                 "Schuhreparatur, Fotoservice, Geldautomat"),
            ],
            "example_prompt": "Sie suchen eine Lampe für Ihr Wohnzimmer. → b) 2. Stock",
            "example_answer": "b",
            "items": [
                (6, "Ihre Mutter hat Geburtstag. Sie möchten ihr einen Blumenstrauß schenken.",
                 floors("EG", "4. Stock"), "c",
                 ("گل در UG است؛ EG فقط کارت تبریک دارد.",
                  "Flowers are in the basement (UG); the ground floor only has cards.",
                  "Blumen gibt es im UG, also in einem anderen Stock.")),
                (7, "Ihr Handy ist heruntergefallen und funktioniert nicht mehr.",
                 floors("3. Stock", "4. Stock"), "a",
                 ("«Handyreparatur» در طبقه ۳.",
                  "Phone repairs are on the 3rd floor.",
                  "„Handyreparatur“ steht im 3. Stock.")),
                (8, "Sie möchten mit einer Freundin zu Mittag essen.",
                 floors("UG", "1. Stock"), "c",
                 ("رستوران در طبقه ۴ است؛ نانوایی UG برای ناهار نیست.",
                  "The restaurant is on the 4th floor, which is not offered.",
                  "Das Restaurant ist im 4. Stock — ein anderer Stock.")),
                (9, "Sie fahren nächste Woche in Urlaub und brauchen einen neuen Koffer.",
                 floors("1. Stock", "EG"), "a",
                 ("«Koffer und Reisetaschen» در طبقه ۱؛ EG فقط کیف دستی دارد.",
                  "Suitcases are on the 1st floor; the ground floor only has handbags.",
                  "„Koffer und Reisetaschen“ im 1. Stock.")),
                (10, "Sie haben gestern eine Hose gekauft. Sie ist kaputt und Sie möchten Ihr "
                     "Geld zurück.",
                 floors("1. Stock", "4. Stock"), "b",
                 ("برای پس دادن جنس: «Kundenservice und Umtausch» در طبقه ۴.",
                  "Returns go to customer service on the 4th floor.",
                  "„Kundenservice und Umtausch“ im 4. Stock.")),
            ],
        },
        # ---------------------------------------------------------- Teil 3
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "یک ایمیل می‌خوانید. برای سؤال‌های ۱۱ تا ۱۵ جواب درست a، b یا c را انتخاب کنید.",
                "You read an email. Choose the right answer a, b or c for items 11 to 15.",
                "Sie lesen eine E-Mail. "
                "Wählen Sie für die Aufgaben 11 bis 15 die richtige Lösung a, b oder c.",
            ),
            "blocks": [
                ("statement", "", "",
                 "Liebe Lea,\n\n"
                 "jetzt bin ich schon drei Wochen in Freiburg und endlich habe ich Zeit, dir "
                 "zu schreiben. Die neue Arbeit im Hotel gefällt mir sehr gut, auch wenn ich "
                 "oft am Wochenende arbeiten muss. Meine Kollegen sind nett und haben mir am "
                 "Anfang viel geholfen. Nur mit ihrem Dialekt habe ich noch Probleme – "
                 "manchmal verstehe ich die Gäste besser als die Kollegen! :-)\n\n"
                 "Eine Wohnung habe ich noch nicht gefunden. Im Moment wohne ich bei meiner "
                 "Tante. Das ist praktisch und billig, aber ihre Wohnung liegt ziemlich weit "
                 "draußen. Ich brauche jeden Morgen fast eine Stunde mit dem Bus. Am Samstag "
                 "sehe ich mir eine kleine Wohnung in der Altstadt an. Drück mir die Daumen!\n\n"
                 "In meiner Freizeit gehe ich viel wandern. Der Schwarzwald ist direkt vor der "
                 "Tür, und jeden Sonntag mache ich mit ein paar Leuten aus dem Hotel eine Tour. "
                 "Letzte Woche waren wir sogar auf dem Feldberg.\n\n"
                 "Kommst du mich im Juni besuchen? Dann habe ich zwei Wochen Urlaub. Wir "
                 "könnten zusammen an den Bodensee fahren. Wenn ich bis dahin eine Wohnung "
                 "habe, kannst du natürlich bei mir schlafen. Sonst suchen wir ein günstiges "
                 "Hotel.\n\n"
                 "Schreib mir bald!\n"
                 "Viele Grüße\n"
                 "Tobias"),
            ],
            "items": [
                (11, "Tobias schreibt, dass …",
                 abc("ihm die Arbeit im Hotel gefällt.", "er nie am Wochenende arbeitet.",
                     "er seine Kollegen nicht mag."), "a",
                 ("«Die neue Arbeit im Hotel gefällt mir sehr gut».",
                  "He likes the new job at the hotel.",
                  "„Die neue Arbeit im Hotel gefällt mir sehr gut.“")),
                (12, "Probleme hat Tobias mit …",
                 abc("den Gästen im Hotel.", "der Sprache seiner Kollegen.", "seinem Chef."),
                 "b",
                 ("«Nur mit ihrem Dialekt habe ich noch Probleme».",
                  "Only his colleagues' dialect is a problem.",
                  "„Nur mit ihrem Dialekt habe ich noch Probleme.“")),
                (13, "Zurzeit wohnt Tobias …",
                 abc("in der Altstadt.", "in einem Hotel.", "bei einer Verwandten."), "c",
                 ("«Im Moment wohne ich bei meiner Tante» — خانه قدیمی شهر را شنبه می‌بیند.",
                  "He lives with his aunt; the old-town flat is only a viewing on Saturday.",
                  "„Im Moment wohne ich bei meiner Tante.“")),
                (14, "Am Sonntag …",
                 abc("arbeitet Tobias immer im Hotel.", "wandert Tobias mit anderen Leuten.",
                     "sieht Tobias sich eine Wohnung an."), "b",
                 ("«jeden Sonntag mache ich mit ein paar Leuten aus dem Hotel eine Tour».",
                  "Every Sunday he hikes with people from the hotel.",
                  "„Jeden Sonntag mache ich mit ein paar Leuten aus dem Hotel eine Tour.“")),
                (15, "Im Juni …",
                 abc("fährt Tobias zu Lea.", "schläft Lea auf jeden Fall in einem Hotel.",
                     "möchte Tobias mit Lea an einen See fahren."), "c",
                 ("«Wir könnten zusammen an den Bodensee fahren» — محل خواب هنوز معلوم نیست.",
                  "He suggests a trip to Lake Constance; where Lea sleeps is still open.",
                  "„Wir könnten zusammen an den Bodensee fahren.“")),
            ],
        },
        # ---------------------------------------------------------- Teil 4
        {
            "type": "match_heading",
            "minutes": 8,
            "title": ("لزن ۴", "Lesen 4", "Lesen 4"),
            "instructions": (
                "شش نفر در اینترنت دنبال کلاس و برنامه تفریحی می‌گردند. سؤال‌های ۱۶ تا ۲۰ و "
                "آگهی‌های a تا f را بخوانید. کدام آگهی به کدام نفر می‌خورد؟ یک سؤال جواب ندارد؛ "
                "آنجا X بزنید. آگهی مثال دیگر قابل انتخاب نیست.",
                "Six people are looking online for courses and leisure activities. Read items "
                "16 to 20 and adverts a to f. Which advert fits which person? One item has no "
                "answer — mark X. The example's advert cannot be chosen again.",
                "Sechs Personen suchen im Internet nach Kursen und Freizeitangeboten. "
                "Lesen Sie die Aufgaben 16 bis 20 und die Anzeigen a bis f. Welche Anzeige "
                "passt zu welcher Person? Für eine Aufgabe gibt es keine Lösung. Markieren Sie "
                "so: X. Die Anzeige aus dem Beispiel können Sie nicht mehr wählen.",
            ),
            "pool": [(key, key) for key in "abcdef"] + [("x", "x")],
            "blocks": [
                ("heading", "a", "www.tanzschule-rhythmus.de",
                 "Salsa, Tango, Walzer – Kurse für Paare und Singles. Anfängerkurse jeden "
                 "Dienstag und Donnerstag ab 19 Uhr. Auch Privatstunden – perfekt vor Ihrer "
                 "Hochzeit!"),
                ("heading", "b", "www.kochwerkstatt-mitte.de",
                 "Kochen wie in Italien, Thailand oder Marokko. Abendkurse in kleinen Gruppen, "
                 "maximal 10 Personen. Auch für Firmen und Teams. Nach dem Kurs essen alle "
                 "zusammen."),
                ("heading", "c", "www.radtouren-elbe.de",
                 "Geführte Radtouren an der Elbe, 30 bis 60 km. Jeden Samstag und Sonntag, "
                 "Start 9 Uhr am Hauptbahnhof. Leihräder für nur 8 € am Tag."),
                ("heading", "d", "www.stadtbad-nord.de",
                 "Hallenbad mit Sauna und Kinderbecken. Samstag und Sonntag ist Familientag: "
                 "Kinder unter 12 Jahren schwimmen gratis. Täglich 7–22 Uhr."),
                ("heading", "e", "www.sprachtreff-online.de",
                 "Englisch, Spanisch, Französisch – Abendkurse für Anfänger und "
                 "Fortgeschrittene. Online oder im Kursraum. Jeden Monat beginnen neue Kurse."),
                ("heading", "f", "www.kletterhalle-gipfel.de",
                 "Klettern für Kinder ab 6 Jahren! Kindergeburtstage mit Trainer, Kuchen und "
                 "Getränken. Montag bis Freitag 14–20 Uhr. Einfach anrufen und reservieren."),
            ],
            "example_prompt": "Nina möchte am Wochenende mit ihren Kindern schwimmen gehen. → d",
            "example_answer": "d",
            "items": [
                (16, "Paul möchte mit seinen Kollegen am Abend etwas Besonderes machen und dabei "
                     "zusammen essen.", None, "b",
                 ("کلاس آشپزی برای تیم‌ها و بعد همه با هم غذا می‌خورند.",
                  "The cooking class takes teams and everyone eats together afterwards.",
                  "„Auch für Firmen und Teams. Nach dem Kurs essen alle zusammen.“")),
                (17, "Ines heiratet im Sommer und möchte vorher mit ihrem Freund für das Fest "
                     "üben.", None, "a",
                 ("رقص با «Privatstunden – perfekt vor Ihrer Hochzeit».",
                  "Dance lessons, \"perfect before your wedding\".",
                  "„Auch Privatstunden – perfekt vor Ihrer Hochzeit!“")),
                (18, "Jan möchte am Sonntag einen Ausflug in der Natur machen, hat aber kein "
                     "eigenes Fahrrad.", None, "c",
                 ("تور دوچرخه یکشنبه‌ها با دوچرخه کرایه‌ای.",
                  "Sunday bike tours with rental bikes.",
                  "„Jeden Samstag und Sonntag … Leihräder für nur 8 € am Tag.“")),
                (19, "Frau Weber sucht für ihren zehnjährigen Sohn einen Kurs, in dem er "
                     "Gitarre lernen kann.", None, "x",
                 ("هیچ آگهی کلاس موسیقی ندارد؛ کلاس زبان (e) و کوهنوردی (f) دام هستند.",
                  "No advert offers music lessons; e and f are distractors.",
                  "Keine Anzeige bietet Musikunterricht an.")),
                (20, "Tim wird acht Jahre alt und möchte mit seinen Freunden an einem Nachmittag "
                     "unter der Woche feiern.", None, "f",
                 ("جشن تولد کودکان، دوشنبه تا جمعه ۱۴ تا ۲۰.",
                  "Children's birthday parties on weekday afternoons.",
                  "„Kindergeburtstage … Montag bis Freitag 14–20 Uhr.“")),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 30,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "چهار بخش، ۲۰ سؤال، حدود ۳۰ دقیقه: رادیو، پیغام تلفنی، اعلان‌ها و گفتگو. اول "
        "سؤال‌ها را بخوانید، بعد متن را بشنوید.",
        "Four parts, 20 items, about 30 minutes: radio, answerphone messages, "
        "announcements and conversations. Read the items first, then listen.",
        "Dieser Prüfungsteil hat vier Teile: Sie hören Sendungen aus dem Radio, Gespräche, "
        "Nachrichten auf dem Anrufbeantworter und Durchsagen. Lesen Sie zuerst die "
        "Aufgaben. Hören Sie dann den Text dazu.",
    ),
    "parts": [
        # ---------------------------------------------------------- Teil 1
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "پنج متن کوتاه می‌شنوید. هر متن را دو بار می‌شنوید. برای سؤال‌های ۱ تا ۵ "
                "جواب درست a، b یا c را انتخاب کنید.",
                "You hear five short texts, each twice. Choose a, b or c for items 1 to 5.",
                "Sie hören fünf kurze Texte. Sie hören jeden Text zweimal. "
                "Wählen Sie für die Aufgaben 1 bis 5 die richtige Lösung a, b oder c.",
            ),
            "tracks": [
                (f"Text {n}", f"{AUDIO}/teil1-{n}.m4a", 2, 10, [n]) for n in range(1, 6)
            ],
            "items": [
                (1, "Wo fährt der Zug nach München heute ab?",
                 abc("Von Gleis 3.", "Von Gleis 7.", "Von Gleis 12."), "b",
                 ("قطار این بار از سکوی ۷ می‌رود؛ ۱۲ برای قطار آگسبورگ است.",
                  "Today it leaves from platform 7; 12 is the Augsburg train.",
                  "„… fährt heute nicht von Gleis drei, sondern von Gleis sieben ab.“")),
                (2, "Was soll Jonas mitbringen?",
                 abc("Einen Salat.", "Getränke.", "Brot."), "a",
                 ("نوشیدنی خریده شده و نان را خواهرش می‌آورد.",
                  "Drinks are bought and her sister brings bread.",
                  "„Kannst du vielleicht einen Salat machen?“")),
                (3, "Wann ist der neue Termin?",
                 abc("Am Dienstag um 9 Uhr.", "Am Mittwoch um 9 Uhr.",
                     "Am Mittwoch um 11 Uhr."), "c",
                 ("ساعت ۹ چهارشنبه پر است؛ ساعت ۱۱ آزاد است.",
                  "Wednesday at nine is taken; eleven is free.",
                  "„Um neun ist schon besetzt, aber um elf Uhr ist noch frei.“")),
                (4, "Wie wird das Wetter am Samstag?",
                 abc("Sonnig und warm.", "Regnerisch und kühl.", "Windig mit Schnee."), "a",
                 ("باران برای جمعه است و برف برای یکشنبه.",
                  "Rain is Friday's weather, snow Sunday's.",
                  "„Am Samstag scheint dann überall die Sonne, bei Temperaturen bis "
                  "dreiundzwanzig Grad.“")),
                (5, "Was ist für Kinder beim Stadtfest kostenlos?",
                 abc("Ein Eis.", "Eine Fahrt mit dem Riesenrad.", "Ein T-Shirt."), "b",
                 ("بستنی نصف قیمت است و تی‌شرت فقط برای بلیت آنلاین.",
                  "Ice cream is half price; T-shirts need an online ticket.",
                  "„Für alle Kinder unter zehn Jahren ist die Fahrt mit dem Riesenrad "
                  "kostenlos.“")),
            ],
        },
        # ---------------------------------------------------------- Teil 2
        {
            "type": "mcq",
            "minutes": 6,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "یک گفتگو می‌شنوید. متن را یک بار می‌شنوید. یانا و برادرش فلیکس در این هفته "
                "چه کار می‌کنند؟ برای سؤال‌های ۶ تا ۱۰ یک تصویر از a تا i انتخاب کنید. هر حرف "
                "را فقط یک بار انتخاب کنید.",
                "You hear a conversation once. What do Jana and her brother Felix do this "
                "week? Choose a picture a–i for items 6 to 10. Use each letter only once.",
                "Sie hören ein Gespräch. Sie hören den Text einmal. "
                "Was machen Jana und ihr Bruder Felix in der Woche? Wählen Sie für die "
                "Aufgaben 6 bis 10 ein passendes Bild aus a bis i. Wählen Sie jeden "
                "Buchstaben nur einmal. Sehen Sie sich jetzt die Bilder an.",
            ),
            "tracks": [("Gespräch", f"{AUDIO}/teil2.m4a", 1, 30, [6, 7, 8, 9, 10])],
            "pool": [(key, "") for key in "abcdefghi"],
            "blocks": [
                ("picture", "a", "Schwimmbad", "", "", f"{BILD}/schwimmbad.svg"),
                ("picture", "b", "Museum", "", "", f"{BILD}/museum.svg"),
                ("picture", "c", "Radtour", "", "", f"{BILD}/radtour.svg"),
                ("picture", "d", "Konzert", "", "", f"{BILD}/konzert.svg"),
                ("picture", "e", "Kochen", "", "", f"{BILD}/kochen.svg"),
                ("picture", "f", "Kino", "", "", f"{BILD}/kino.svg"),
                ("picture", "g", "Wandern", "", "", f"{BILD}/wandern.svg"),
                ("picture", "h", "Markt", "", "", f"{BILD}/markt.svg"),
                ("picture", "i", "Fußball", "", "", f"{BILD}/fussball.svg"),
            ],
            "example_prompt": "Montag → b",
            "example_answer": "b",
            "items": [
                (6, "Dienstag", None, "c",
                 ("استخر سه‌شنبه بسته است؛ دوچرخه‌سواری تا دریاچه.",
                  "The pool is closed on Tuesday; they cycle to the lake.",
                  "„Am Dienstag … eine Radtour an den See machen.“")),
                (7, "Mittwoch", None, "e",
                 ("یانا تا عصر سر کار است و شب آشپزی می‌کند.",
                  "Jana works late and cooks in the evening.",
                  "„Aber abends koche ich für uns.“")),
                (8, "Donnerstag", None, "d",
                 ("فوتبال را نمی‌بینند؛ به کنسرت گروه محبوب یانا می‌روند.",
                  "They skip the football match and go to the concert.",
                  "„Am Donnerstag spielt meine Lieblingsband im Park.“")),
                (9, "Freitag", None, "a",
                 ("جمعه بالاخره استخر؛ سینما را رد می‌کنند.",
                  "Friday is finally the pool; the cinema is turned down.",
                  "„Okay, am Freitag gehen wir ins Schwimmbad. Versprochen.“")),
                (10, "Samstag", None, "h",
                 ("صبح بازار؛ برای کوه‌پیمایی وقت نیست.",
                  "The market in the morning; no time for a hike.",
                  "„Am Samstag ist morgens Markt auf dem Domplatz.“")),
            ],
        },
        # ---------------------------------------------------------- Teil 3
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "پنج گفتگوی کوتاه می‌شنوید. هر متن را یک بار می‌شنوید. برای سؤال‌های ۱۱ تا ۱۵ "
                "جواب درست a، b یا c را انتخاب کنید.",
                "You hear five short conversations, each once. Choose a, b or c for items "
                "11 to 15.",
                "Sie hören fünf kurze Gespräche. Sie hören jeden Text einmal. "
                "Wählen Sie für die Aufgaben 11 bis 15 die richtige Lösung a, b oder c.",
            ),
            "tracks": [
                (f"Gespräch {n - 10}", f"{AUDIO}/teil3-{n - 10}.m4a", 1, 10, [n])
                for n in range(11, 16)
            ],
            "items": [
                (11, "Was isst der Mann heute in der Kantine?",
                 bilder(("Pizza", "pizza"), ("Salat", "salat"), ("Suppe", "suppe")), "c",
                 ("سالاد تمام شده و پیتزا را نمی‌خواهد.",
                  "The salad has run out and he doesn't want pizza.",
                  "„Dann nehme ich eben die Suppe.“")),
                (12, "Welche Tasche kauft die Frau?",
                 bilder(("Handtasche", "handtasche"), ("Rucksack", "rucksack"),
                        ("Koffer", "koffer")), "a",
                 ("کوله برای کار بزرگ است و چمدان را دارد.",
                  "The backpack is too big for work and she already has a suitcase.",
                  "„Haben Sie die schwarze Handtasche auch in Braun? … Die nehme ich.“")),
                (13, "Was hat die Frau im Zug vergessen?",
                 bilder(("Schlüssel", "schluessel"), ("Brille", "brille"),
                        ("Regenschirm", "regenschirm")), "b",
                 ("چتر همراهش است و کلید را پیدا کرده؛ عینکش را جا گذاشته.",
                  "She has her umbrella and found her keys; she left her glasses.",
                  "„Es ist meine Brille, in einem blauen Etui.“")),
                (14, "Wann treffen sich die beiden?",
                 bilder(("Um halb sieben.", "uhr-1830"), ("Um sieben.", "uhr-1900"),
                        ("Um halb acht.", "uhr-1930")), "c",
                 ("ساعت هفت نمی‌رسد؛ هفت و نیم قرار می‌گذارند.",
                  "Seven is too early for her, so they settle on half past seven.",
                  "„Sagen wir halb acht?“ — „Gut, halb acht.“")),
                (15, "Wie fährt der Mann jetzt zur Arbeit?",
                 bilder(("Mit dem Auto.", "auto"), ("Mit dem Fahrrad.", "fahrrad"),
                        ("Mit dem Bus.", "bus")), "b",
                 ("ماشین گران است و اتوبوس را کنار گذاشته.",
                  "The car is too expensive and he has stopped taking the bus.",
                  "„Jetzt nehme ich das Fahrrad – das ist sogar schneller.“")),
            ],
        },
        # ---------------------------------------------------------- Teil 4
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۴", "Hören 4", "Hören 4"),
            "instructions": (
                "یک مصاحبه می‌شنوید. متن را دو بار می‌شنوید. برای سؤال‌های ۱۶ تا ۲۰ Ja یا "
                "Nein را انتخاب کنید. حالا سؤال‌ها را بخوانید.",
                "You hear an interview twice. Choose Ja or Nein for items 16 to 20. Read the "
                "items now.",
                "Sie hören ein Interview. Sie hören den Text zweimal. "
                "Wählen Sie für die Aufgaben 16 bis 20 Ja oder Nein. Lesen Sie jetzt die "
                "Aufgaben.",
            ),
            "tracks": [("Interview", f"{AUDIO}/teil4.m4a", 2, 30, [16, 17, 18, 19, 20])],
            "example_prompt": "Lina ist in Korea geboren. → Nein",
            "example_answer": "nein",
            "items": [
                (16, "Lina hatte als Kind Tiere zu Hause.", YES_NO, "ja",
                 ("«Wir hatten zu Hause immer Tiere».",
                  "\"We always had animals at home.\"",
                  "„Wir hatten zu Hause immer Tiere, zwei Katzen und einen Hund.“")),
                (17, "Lina hat ihr Studium abgeschlossen.", YES_NO, "nein",
                 ("بعد از یک سال رشته زیست‌شناسی را رها کرد.",
                  "She gave up biology after a year.",
                  "„Nach einem Jahr habe ich aufgehört.“")),
                (18, "Lina hat durch einen Bekannten von der Ausbildung gehört.", YES_NO, "ja",
                 ("«Ein Freund hat mir dann von der Ausbildung im Tierpark erzählt».",
                  "A friend told her about the training.",
                  "„Ein Freund hat mir dann von der Ausbildung im Tierpark erzählt.“")),
                (19, "Am liebsten füttert Lina die Tiere.", YES_NO, "nein",
                 ("کار محبوبش توضیح دادن برای کلاس‌های مدرسه است.",
                  "What she likes best is explaining things to school classes.",
                  "„Am Nachmittag erkläre ich Schulklassen … Das mache ich am liebsten.“")),
                (20, "Lina muss manchmal auch am Wochenende arbeiten.", YES_NO, "ja",
                 ("«jedes zweite Wochenende».", "Every other weekend.",
                  "„Ja, jedes zweite Wochenende.“")),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 30,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "دو بخش، ۳۰ دقیقه: یک پیامک به دوست و یک ایمیل نیمه‌رسمی. در هر دو، به هر سه نکته "
        "بپردازید.",
        "Two parts, 30 minutes: an SMS to a friend and a semi-formal email. Cover all "
        "three points in both.",
        "Dieser Prüfungsteil hat zwei Teile: Sie schreiben eine SMS und eine E-Mail.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 12,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "یک پیامک بنویسید (۲۰ تا ۳۰ کلمه). درباره هر سه نکته بنویسید.",
                "Write an SMS (20–30 words). Write about all three points.",
                "Schreiben Sie eine SMS (20–30 Wörter). Schreiben Sie zu allen drei Punkten.",
            ),
            "stimulus_intro":
                "Sie sind im Supermarkt und kaufen für das Abendessen mit Ihrem Mitbewohner "
                "Jonas ein. Schreiben Sie Jonas eine SMS.",
            "blocks": [
                ("bullet", "", "", "Fragen Sie, was er essen möchte."),
                ("bullet", "", "", "Schreiben Sie, was Sie schon gekauft haben."),
                ("bullet", "", "", "Bitten Sie ihn, zu Hause etwas vorzubereiten."),
            ],
            "items": [(1, "Schreiben Sie die SMS.", None, "", None)],
            "min_words": 20,
        },
        {
            "type": "writing",
            "minutes": 18,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "یک ایمیل بنویسید (۳۰ تا ۴۰ کلمه). درباره هر سه نکته بنویسید و سلام و "
                "خداحافظی را فراموش نکنید.",
                "Write an email (30–40 words). Cover all three points and remember the "
                "greeting and closing.",
                "Schreiben Sie eine E-Mail (30–40 Wörter). Schreiben Sie zu allen drei "
                "Punkten. Vergessen Sie die Anrede und den Gruß nicht.",
            ),
            "stimulus_intro":
                "Die Waschmaschine im Keller Ihres Hauses ist seit einer Woche kaputt. "
                "Schreiben Sie Ihrer Hausverwaltung, Frau Krüger, eine E-Mail.",
            "blocks": [
                ("bullet", "", "", "Beschreiben Sie das Problem."),
                ("bullet", "", "", "Fragen Sie, wann jemand kommt."),
                ("bullet", "", "", "Sagen Sie, warum das für Sie wichtig ist."),
            ],
            "items": [(2, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 30,
        },
    ],
}
