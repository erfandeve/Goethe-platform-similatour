"""Start Deutsch 1 (A1) — original material in the official task shapes.

Lesen 25 min / 15 items · Hören 20 min / 15 items · Schreiben 20 min / 2 tasks.
The wording is written for Lexora; only the task formats follow the Goethe
model set, so nothing here reproduces Goethe-Institut text.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/a1/hoeren"

LESEN = {
    "skill": "lesen",
    "duration": 25,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "سه بخش، ۱۵ سؤال، ۲۵ دقیقه. متن‌ها کوتاه‌اند: ایمیل، آگهی و تابلوهای عمومی.",
        "Three parts, 15 items, 25 minutes. The texts are short: emails, adverts and public signs.",
        "Drei Teile, 15 Aufgaben, 25 Minuten. Die Texte sind kurz: E-Mails, Anzeigen und Schilder.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "دو ایمیل کوتاه را می‌خوانید. آیا جمله‌ها درست‌اند یا غلط؟",
                "You read two short emails. Are the statements true or false?",
                "Sie lesen zwei kurze E-Mails. Sind die Aussagen richtig oder falsch?",
            ),
            "stimulus_title": "Zwei E-Mails",
            "blocks": [
                ("paragraph", "1", "Von: nina@webmail.de · Betreff: Samstag",
                 "Hallo Tom,\n\nam Samstag habe ich frei. Wollen wir zusammen ins Schwimmbad "
                 "gehen? Das Wasser ist jetzt warm. Wir treffen uns um zehn Uhr am Bahnhof. "
                 "Der Bus fährt um Viertel nach zehn. Bitte bring dein Handtuch mit. Ich "
                 "kaufe die Tickets.\n\nViele Grüße\nNina"),
                ("paragraph", "2", "Von: kurs@sprachschule-nord.de · Betreff: Ihr Deutschkurs",
                 "Sehr geehrte Frau Yilmaz,\n\nIhr Deutschkurs A1 beginnt am Montag, dem "
                 "3. März, um 18 Uhr in Raum 12. Der Kurs ist zweimal pro Woche, montags und "
                 "mittwochs. Das Buch kostet 24 Euro und Sie bekommen es am ersten Tag. "
                 "Bitte kommen Sie zehn Minuten früher.\n\nMit freundlichen Grüßen\n"
                 "Sprachschule Nord"),
            ],
            "example_prompt": "Nina schreibt an Tom.",
            "example_answer": "richtig",
            "items": [
                (1, "Nina und Tom treffen sich um zehn Uhr.", TRUE_FALSE, "richtig",
                 ("در ایمیل نوشته «Wir treffen uns um zehn Uhr am Bahnhof».",
                  "The email says they meet at ten at the station.",
                  "In der E-Mail steht: „Wir treffen uns um zehn Uhr am Bahnhof.“")),
                (2, "Tom soll die Tickets kaufen.", TRUE_FALSE, "falsch",
                 ("نینا می‌نویسد «Ich kaufe die Tickets» — یعنی خودش می‌خرد.",
                  "Nina writes \"Ich kaufe die Tickets\" — she buys them.",
                  "Nina schreibt „Ich kaufe die Tickets“ — sie kauft sie.")),
                (3, "Der Deutschkurs beginnt am Abend.", TRUE_FALSE, "richtig",
                 ("ساعت ۱۸ یعنی عصر.", "18:00 is the evening.", "18 Uhr ist am Abend.")),
                (4, "Der Kurs findet jeden Tag statt.", TRUE_FALSE, "falsch",
                 ("دو بار در هفته: دوشنبه و چهارشنبه.",
                  "Twice a week: Monday and Wednesday.",
                  "Zweimal pro Woche: montags und mittwochs.")),
                (5, "Das Buch bekommt Frau Yilmaz am ersten Kurstag.", TRUE_FALSE, "richtig",
                 ("«Sie bekommen es am ersten Tag».",
                  "\"Sie bekommen es am ersten Tag.\"",
                  "„Sie bekommen es am ersten Tag.“")),
            ],
        },
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "برای هر موقعیت، آگهی مناسب را انتخاب کنید: a یا b.",
                "For each situation, choose the suitable advert: a or b.",
                "Wählen Sie für jede Situation die passende Anzeige: a oder b.",
            ),
            "stimulus_title": "Anzeigen",
            "blocks": [
                ("paragraph", "6a", "Fahrrad Meier",
                 "Fahrräder für Kinder und Erwachsene. Reparatur in 24 Stunden. "
                 "Montag bis Freitag 9–18 Uhr, Samstag 9–13 Uhr. Bahnhofstraße 4."),
                ("paragraph", "6b", "Rad & Tour",
                 "Wir vermieten Fahrräder pro Tag oder pro Woche. Auch E-Bikes. "
                 "Täglich 8–20 Uhr, auch am Sonntag. Am Seeweg 11."),
                ("paragraph", "7a", "Café Sonne",
                 "Frühstück von 7 bis 11 Uhr. Kaffee, Brötchen, Ei. Kein Mittagessen."),
                ("paragraph", "7b", "Restaurant Anna",
                 "Mittagsmenü von 12 bis 15 Uhr, ab 8,50 Euro. Sonntags geschlossen."),
                ("paragraph", "8a", "Sprachcafé",
                 "Jeden Donnerstag 19 Uhr Deutsch sprechen mit anderen. Kostenlos, ohne Anmeldung."),
                ("paragraph", "8b", "Institut Lingua",
                 "Deutschkurse A1 bis C1, mit Prüfung. Anmeldung im Büro, Kursgebühr 320 Euro."),
                ("paragraph", "9a", "Wohnung Nord",
                 "2 Zimmer, 55 m², 3. Stock, kein Aufzug. 640 Euro. Frei ab 1. Mai."),
                ("paragraph", "9b", "Zimmer im Studentenhaus",
                 "Einzelzimmer möbliert, 18 m², Küche und Bad zusammen. 320 Euro. Sofort frei."),
                ("paragraph", "10a", "Praxis Dr. Weber",
                 "Zahnarzt. Sprechstunde Mo–Fr 8–12 Uhr, Di und Do auch 15–18 Uhr."),
                ("paragraph", "10b", "Apotheke am Markt",
                 "Notdienst heute Nacht bis 8 Uhr. Rezepte und Beratung."),
            ],
            "items": [
                (6, "Sie möchten am Sonntag ein Fahrrad mieten.",
                 [("a", "Anzeige a"), ("b", "Anzeige b")], "b",
                 ("فقط Rad & Tour یکشنبه‌ها هم باز است و دوچرخه کرایه می‌دهد.",
                  "Only Rad & Tour opens on Sunday and rents bikes.",
                  "Nur Rad & Tour hat sonntags offen und vermietet Räder.")),
                (7, "Sie möchten um 13 Uhr warm essen.",
                 [("a", "Anzeige a"), ("b", "Anzeige b")], "b",
                 ("منوی ظهر از ۱۲ تا ۱۵ است؛ کافه فقط صبحانه دارد.",
                  "The lunch menu runs 12–15; the café serves only breakfast.",
                  "Das Mittagsmenü läuft 12–15 Uhr; das Café hat nur Frühstück.")),
                (8, "Sie wollen ohne Geld Deutsch sprechen üben.",
                 [("a", "Anzeige a"), ("b", "Anzeige b")], "a",
                 ("Sprachcafé رایگان و بدون ثبت‌نام است.",
                  "The Sprachcafé is free and needs no registration.",
                  "Das Sprachcafé ist kostenlos und ohne Anmeldung.")),
                (9, "Sie suchen ein möbliertes Zimmer für sofort.",
                 [("a", "Anzeige a"), ("b", "Anzeige b")], "b",
                 ("اتاق مبله و «sofort frei» است.",
                  "The room is furnished and available immediately.",
                  "Das Zimmer ist möbliert und sofort frei.")),
                (10, "Sie brauchen am Abend Medikamente.",
                 [("a", "Anzeige a"), ("b", "Anzeige b")], "b",
                 ("داروخانه شب‌کار است؛ مطب دندان‌پزشکی نه.",
                  "The pharmacy is on night duty; the dentist is not.",
                  "Die Apotheke hat Notdienst; die Zahnarztpraxis nicht.")),
            ],
        },
        {
            "type": "mcq",
            "minutes": 9,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "تابلوها و اطلاعیه‌های عمومی را می‌خوانید. آیا جمله درست است یا غلط؟",
                "You read public signs and notices. Is each statement true or false?",
                "Sie lesen Schilder und Aushänge. Ist die Aussage richtig oder falsch?",
            ),
            "stimulus_title": "Schilder und Aushänge",
            "blocks": [
                ("paragraph", "11", "Am Eingang der Bibliothek",
                 "Bibliothek — Mo bis Fr 10–19 Uhr, Sa 10–14 Uhr. Sonntag geschlossen. "
                 "Essen und Trinken sind im Lesesaal nicht erlaubt."),
                ("paragraph", "12", "Im Bus",
                 "Fahrkarten bitte vor der Fahrt kaufen. Beim Fahrer gibt es keine Tickets. "
                 "Automat am Bahnsteig."),
                ("paragraph", "13", "Im Supermarkt",
                 "Heute frisches Brot ab 15 Uhr. Nur solange der Vorrat reicht."),
                ("paragraph", "14", "An der Haustür",
                 "Liebe Nachbarn, am Dienstag von 9 bis 12 Uhr kommt der Elektriker. "
                 "In dieser Zeit gibt es keinen Strom im Haus."),
                ("paragraph", "15", "Im Schwimmbad",
                 "Kinder unter 8 Jahren nur mit Erwachsenen. Duschen vor dem Schwimmen."),
            ],
            "items": [
                (11, "Am Sonntag kann man in die Bibliothek gehen.", TRUE_FALSE, "falsch",
                 ("«Sonntag geschlossen».", "It says Sunday closed.", "Dort steht „Sonntag geschlossen“.")),
                (12, "Man kann die Fahrkarte im Bus beim Fahrer kaufen.", TRUE_FALSE, "falsch",
                 ("«Beim Fahrer gibt es keine Tickets».",
                  "\"Beim Fahrer gibt es keine Tickets.\"",
                  "„Beim Fahrer gibt es keine Tickets.“")),
                (13, "Das frische Brot gibt es am Nachmittag.", TRUE_FALSE, "richtig",
                 ("ساعت ۱۵ بعدازظهر است.", "15:00 is the afternoon.", "15 Uhr ist am Nachmittag.")),
                (14, "Am Dienstagvormittag funktioniert der Strom nicht.", TRUE_FALSE, "richtig",
                 ("از ۹ تا ۱۲ برق قطع است.", "No power from 9 to 12.", "Von 9 bis 12 Uhr gibt es keinen Strom.")),
                (15, "Kinder unter 8 Jahren dürfen allein schwimmen.", TRUE_FALSE, "falsch",
                 ("«nur mit Erwachsenen».", "Only with adults.", "„Nur mit Erwachsenen.“")),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 20,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "سه بخش، ۱۵ سؤال، ۲۰ دقیقه. بعضی فایل‌ها دو بار و بعضی یک بار پخش می‌شوند.",
        "Three parts, 15 items, 20 minutes. Some tracks play twice, some only once.",
        "Drei Teile, 15 Aufgaben, 20 Minuten. Manche Texte hören Sie zweimal, manche einmal.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "شش گفتگوی کوتاه می‌شنوید. هر متن را دو بار می‌شنوید. گزینه درست را انتخاب کنید.",
                "You hear six short conversations, each twice. Choose the right answer.",
                "Sie hören sechs kurze Gespräche, jedes zweimal. Wählen Sie die richtige Antwort.",
            ),
            "tracks": [("Teil 1", f"{AUDIO}/teil1.m4a", 2, 20, [1, 2, 3, 4, 5, 6])],
            "items": [
                (1, "Wann fährt der Zug nach Hamburg?",
                 [("a", "um 9:15"), ("b", "um 9:50"), ("c", "um 10:15")], "b", None),
                (2, "Was kostet das Ticket?",
                 [("a", "12 Euro"), ("b", "20 Euro"), ("c", "22 Euro")], "c", None),
                (3, "Wo ist die Apotheke?",
                 [("a", "neben der Bank"), ("b", "hinter dem Bahnhof"), ("c", "gegenüber der Post")],
                 "c", None),
                (4, "Was möchte die Frau trinken?",
                 [("a", "Tee"), ("b", "Kaffee"), ("c", "Wasser")], "a", None),
                (5, "Wie ist das Wetter am Sonntag?",
                 [("a", "Es regnet."), ("b", "Es schneit."), ("c", "Die Sonne scheint.")], "a", None),
                (6, "Wie viele Personen kommen zum Essen?",
                 [("a", "drei"), ("b", "vier"), ("c", "sechs")], "b", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 6,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "چهار اعلان عمومی می‌شنوید. هر متن را فقط یک بار می‌شنوید. درست یا غلط؟",
                "You hear four public announcements, each only once. True or false?",
                "Sie hören vier Durchsagen, jede nur einmal. Richtig oder falsch?",
            ),
            "tracks": [("Teil 2", f"{AUDIO}/teil2.m4a", 1, 15, [7, 8, 9, 10])],
            "items": [
                (7, "Der Zug nach Köln hat Verspätung.", TRUE_FALSE, "richtig", None),
                (8, "Das Schwimmbad schließt heute früher.", TRUE_FALSE, "richtig", None),
                (9, "Der Supermarkt hat morgen geschlossen.", TRUE_FALSE, "falsch", None),
                (10, "Die Führung im Museum beginnt um 14 Uhr.", TRUE_FALSE, "falsch", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "پنج پیام تلفنی می‌شنوید. هر پیام را دو بار می‌شنوید. گزینه درست را انتخاب کنید.",
                "You hear five phone messages, each twice. Choose the right answer.",
                "Sie hören fünf Nachrichten auf dem Anrufbeantworter, jede zweimal.",
            ),
            "tracks": [("Teil 3", f"{AUDIO}/teil3.m4a", 2, 20, [11, 12, 13, 14, 15])],
            "items": [
                (11, "Wann kommt der Handwerker?",
                 [("a", "am Montag"), ("b", "am Dienstag"), ("c", "am Mittwoch")], "b", None),
                (12, "Was soll Herr Klein mitbringen?",
                 [("a", "seinen Pass"), ("b", "ein Foto"), ("c", "Geld")], "a", None),
                (13, "Wo treffen sich die Freunde?",
                 [("a", "im Kino"), ("b", "im Café"), ("c", "im Park")], "c", None),
                (14, "Der Termin beim Arzt ist …",
                 [("a", "um 8:30"), ("b", "um 9:30"), ("c", "um 10:30")], "b", None),
                (15, "Warum ruft Frau Berg an?",
                 [("a", "Sie ist krank."), ("b", "Sie kommt später."), ("c", "Sie hat den Schlüssel.")],
                 "c", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 20,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "دو تکلیف، ۲۰ دقیقه. اول یک فرم را کامل می‌کنید، بعد یک پیام کوتاه می‌نویسید.",
        "Two tasks, 20 minutes: complete a form, then write a short message.",
        "Zwei Aufgaben, 20 Minuten: ein Formular ausfüllen und eine kurze Mitteilung schreiben.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 8,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "دوستتان Karim می‌خواهد در کتابخانه کارت عضویت بگیرد. فرم را از روی اطلاعات زیر پر کنید.",
                "Your friend Karim wants a library card. Complete the form from the information below.",
                "Ihr Freund Karim möchte einen Bibliotheksausweis. Füllen Sie das Formular aus.",
            ),
            "stimulus_title": "Anmeldung Stadtbibliothek",
            "stimulus_intro":
                "Karim Osmani ist 24 Jahre alt und kommt aus Isfahan. Er wohnt seit einem Jahr in "
                "der Lindenstraße 8 in 30159 Hannover. Er studiert Informatik. Seine "
                "Telefonnummer ist 0176 4432110.",
            "blocks": [
                ("paragraph", "", "Formular",
                 "Familienname: ______\nVorname: ______\nGeburtsland: ______\n"
                 "Straße und Hausnummer: ______\nPostleitzahl und Ort: ______\n"
                 "Beruf: ______\nTelefon: ______"),
            ],
            "items": [(1, "Füllen Sie das Formular aus.", None, "", None)],
            "min_words": 20,
        },
        {
            "type": "writing",
            "minutes": 12,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "به همکارتان یک پیام کوتاه بنویسید. حدود ۳۰ کلمه. هر سه نکته را بنویسید.",
                "Write a short message to a colleague, about 30 words, covering all three points.",
                "Schreiben Sie eine kurze Mitteilung an eine Kollegin, etwa 30 Wörter, zu allen "
                "drei Punkten.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Sie sind krank und können morgen nicht zur Arbeit kommen. Schreiben Sie an Ihre "
                "Kollegin Frau Sommer.",
            "blocks": [
                ("bullet", "", "", "Sagen Sie, warum Sie nicht kommen."),
                ("bullet", "", "", "Schreiben Sie, wann Sie wieder da sind."),
                ("bullet", "", "", "Bitten Sie um etwas (zum Beispiel eine Information)."),
            ],
            "items": [(2, "Schreiben Sie die Mitteilung.", None, "", None)],
            "min_words": 30,
        },
    ],
}
