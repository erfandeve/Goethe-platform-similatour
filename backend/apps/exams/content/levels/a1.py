"""Start Deutsch 1 (A1) — the official task shapes, filled with in-house material.

Structure taken from the published Modellsatz (8. Auflage, 2024):

    Hören   ca. 20 min · 3 Teile · 15 items
            Teil 1  items 1–6   three options a/b/c, each text heard twice
            Teil 2  items 7–10  Richtig/Falsch, each text heard once
            Teil 3  items 11–15 three options a/b/c, each text heard twice
    Lesen   ca. 25 min · 3 Teile · 15 items
            Teil 1  items 1–5   Richtig/Falsch on two short messages
            Teil 2  items 6–10  which of two adverts answers the need, a or b
            Teil 3  items 11–15 Richtig/Falsch on public signs
    Schreiben ca. 20 min · 2 Teile
            Teil 1  items 1–5   five missing fields in a form
            Teil 2             ~30 words with a greeting and three points

Every Teil opens with a worked example numbered 0, as the real paper does. The
wording is Lexora's own; only the format follows the Goethe model set.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/a1/hoeren"
# Teil 1 answers with three pictures per question, as the paper prints it.
# `manage.py make_a1_bilder` draws them.
BILD = "/media/exams/a1/bilder"

# Lesen 2 shows small adverts; Lesen 3 shows signs. Both are pictures in the
# real paper, and the back office can attach one to any block.
AB = [("a", "a"), ("b", "b")]

LESEN = {
    "skill": "lesen",
    "duration": 25,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "سه بخش، ۱۵ سؤال، حدود ۲۵ دقیقه. پیام‌های کوتاه، آگهی‌ها و تابلوهای عمومی.",
        "Three parts, 15 items, about 25 minutes: short messages, adverts and public signs.",
        "Drei Teile, 15 Aufgaben, circa 25 Minuten: kurze Mitteilungen, Anzeigen und Schilder.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "دو متن و سؤال‌های ۱ تا ۵ را بخوانید. علامت بزنید: Richtig یا Falsch.",
                "Read the two texts and items 1–5. Tick Richtig or Falsch.",
                "Lesen Sie die beiden Texte und die Aufgaben 1 bis 5. "
                "Kreuzen Sie an: Richtig oder Falsch.",
            ),
            "stimulus_title": "Zwei Nachrichten",
            "blocks": [
                ("paragraph", "", "E-Mail von Karin",
                 "Hallo Li,\n\ndanke für deine Nachricht. Dein Zug kommt hier in Bremen um "
                 "12.36 Uhr an. Ich bin ab 12.15 Uhr im Hauptbahnhof und warte auf dich vor "
                 "der Auskunft.\n\nDu kannst mich den ganzen Vormittag auf meinem Handy "
                 "erreichen.\n\nDeine Karin"),
                ("paragraph", "", "Einladung von Ralf",
                 "Liebe Carmen,\n\nam kommenden Sonntag habe ich Geburtstag. Feiern möchte "
                 "ich aber schon am Samstagabend. Wir fangen um 21 Uhr an. Es kommen viele "
                 "Leute, die du auch kennst. Bringst du bitte einen Salat mit? Und vergiss "
                 "keine Jacke — wir sitzen im Garten.\n\nBis Samstag!\nRalf"),
            ],
            "example_prompt": "Lis Zug kommt nach halb eins an.",
            "example_answer": "falsch",
            "items": [
                (1, "Karin wartet vor der Auskunft.", TRUE_FALSE, "richtig",
                 ("در متن: «warte auf dich vor der Auskunft».",
                  "The text says she waits in front of the information desk.",
                  "Im Text: „warte auf dich vor der Auskunft“.")),
                (2, "Li kann Karin am Vormittag anrufen.", TRUE_FALSE, "richtig",
                 ("«den ganzen Vormittag auf meinem Handy erreichen».",
                  "She can be reached all morning on her mobile.",
                  "„Den ganzen Vormittag auf meinem Handy erreichen.“")),
                (3, "Ralf feiert am Sonntag.", TRUE_FALSE, "falsch",
                 ("تولدش یکشنبه است ولی جشن شنبه شب است.",
                  "His birthday is Sunday but the party is Saturday evening.",
                  "Geburtstag ist Sonntag, gefeiert wird Samstagabend.")),
                (4, "Carmen soll etwas zu essen mitbringen.", TRUE_FALSE, "richtig",
                 ("«Bringst du bitte einen Salat mit?»",
                  "She is asked to bring a salad.",
                  "„Bringst du bitte einen Salat mit?“")),
                (5, "Die Party ist in der Wohnung.", TRUE_FALSE, "falsch",
                 ("«wir sitzen im Garten».", "They sit in the garden.",
                  "„Wir sitzen im Garten.“")),
            ],
        },
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "متن‌ها و سؤال‌های ۶ تا ۱۰ را بخوانید. اطلاعات را کجا پیدا می‌کنید؟ "
                "علامت بزنید: a یا b.",
                "Read the texts and items 6–10. Where do you find the information? Tick a or b.",
                "Lesen Sie die Texte und die Aufgaben 6 bis 10. Wo finden Sie Informationen? "
                "Kreuzen Sie an: a oder b.",
            ),
            "stimulus_title": "Anzeigen im Internet",
            "blocks": [
                ("heading", "6a", "www.wetter-heute.de",
                 "Wetter aktuell · Warnungen · Umweltinfos · Klimadaten für ganz Deutschland."),
                ("heading", "6b", "www.openair-park.de",
                 "Open-Air-Konzert am 30. Mai. Bei Regen in der Stadthalle. Tickets online."),
                ("heading", "7a", "www.sprachschule-nord.de",
                 "Deutschkurse in Bremen · A1 bis C1 · Die Schule · Die Kurse · Die Preise."),
                ("heading", "7b", "www.idiomas-mar.com",
                 "Sprachkurse für Deutsche: Spanisch auf Mallorca, Englisch auf Malta."),
                ("heading", "8a", "www.bahn-tickets.de",
                 "Fahrkarten für alle Züge online kaufen · Reservierungen · 24-Stunden-Service."),
                ("heading", "8b", "www.buehne-ticket.de",
                 "Ticketservice für Theater, Konzerte und Busreisen nach Polen und Ungarn."),
                ("heading", "9a", "www.ferienhaus-weber.de",
                 "Ferienwohnungen am Bodensee · Häuser · Preise · Kontakt."),
                ("heading", "9b", "www.bodensee-info.de",
                 "Touristeninformation Bodensee · Urlaubsorte · Hotelservice · Rundreisen."),
                ("heading", "10a", "www.zugauskunft.de",
                 "ab Wiesbaden 08.09 · an Hamburg 12.40 · Dauer 4:31 · 1× umsteigen."),
                ("heading", "10b", "www.zugauskunft.de",
                 "ab Hamburg 12.18 · an Wiesbaden 16.52 · Dauer 4:34 · 1× umsteigen."),
            ],
            "example_prompt": "Sie wollen wissen: Regnet es morgen? → a",
            "example_answer": "a",
            "items": [
                (6, "Sie wollen wissen, wie das Wetter am Wochenende wird.", AB, "a",
                 ("سایت هواشناسی، نه کنسرت.", "The weather site, not the concert one.",
                  "Die Wetterseite, nicht die Konzertseite.")),
                (7, "Sie möchten in Deutschland Deutsch lernen.", AB, "a",
                 ("مدرسه در برمن است؛ گزینه b برای آلمانی‌زبان‌هاست.",
                  "The school is in Bremen; b is for German speakers abroad.",
                  "Die Schule ist in Bremen; b ist für Deutsche im Ausland.")),
                (8, "Sie möchten eine Zugfahrkarte im Internet kaufen.", AB, "a",
                 ("b فقط بلیت تئاتر و اتوبوس می‌فروشد.",
                  "b sells only theatre and coach tickets.",
                  "b verkauft nur Theater- und Bustickets.")),
                (9, "Sie möchten allgemeine Informationen über den Bodensee.", AB, "b",
                 ("a فقط خانه اجاره‌ای دارد.", "a only rents holiday flats.",
                  "a vermietet nur Ferienwohnungen.")),
                (10, "Sie sind in Wiesbaden und wollen mittags in Hamburg sein.", AB, "a",
                 ("رسیدن ساعت ۱۲:۴۰ است؛ b جهت برعکس دارد.",
                  "Arrival 12.40; b runs the other way.",
                  "Ankunft 12.40 Uhr; b fährt in die Gegenrichtung.")),
            ],
        },
        {
            "type": "mcq",
            "minutes": 9,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "تابلوها و سؤال‌های ۱۱ تا ۱۵ را بخوانید. علامت بزنید: Richtig یا Falsch.",
                "Read the signs and items 11–15. Tick Richtig or Falsch.",
                "Lesen Sie die Texte und die Aufgaben 11 bis 15. "
                "Kreuzen Sie an: Richtig oder Falsch.",
            ),
            "stimulus_title": "Schilder und Aushänge",
            "blocks": [
                ("heading", "11", "In der Sprachschule",
                 "In der 10-Uhr-Pause bekommen Sie an der Rezeption ein Frühstückspaket: "
                 "belegte Brötchen und Getränke für 2 Euro."),
                ("heading", "12", "An der Post",
                 "Öffnungszeiten: montags bis freitags 8.00–12.00 und 13.00–18.00, "
                 "samstags 8.00–12.00."),
                ("heading", "13", "Am Bahnhof",
                 "Auf dem gesamten Bahnhof ist das Rauchen verboten."),
                ("heading", "14", "Eingang Restaurant",
                 "Heute im Bavaria: Bayerischer Abend. Brezeln, Weißwürste, Sauerkraut. "
                 "Volksmusik, ab 20 Uhr Tanz."),
                ("heading", "15", "An der Haltestelle",
                 "In der Neujahrsnacht: Busverkehr bis 23.00 Uhr und von 1.00 Uhr bis "
                 "5.00 Uhr alle 30 Minuten."),
            ],
            "example_prompt": "Zum Deutschlernen gehen Sie in die Beethovenstraße 23.",
            "example_answer": "richtig",
            "items": [
                (11, "In der Sprachschule können Sie etwas zu essen kaufen.", TRUE_FALSE,
                 "richtig",
                 ("بستهٔ صبحانه ۲ یورو می‌فروشند.", "They sell a breakfast pack for 2 euros.",
                  "Es gibt ein Frühstückspaket für 2 Euro.")),
                (12, "Es ist Samstagnachmittag. Sie können jetzt Briefmarken kaufen.",
                 TRUE_FALSE, "falsch",
                 ("شنبه فقط تا ساعت ۱۲ باز است.", "Saturday closes at 12.",
                  "Samstags nur bis 12.00 Uhr.")),
                (13, "Sie können auf dem Bahnhof rauchen.", TRUE_FALSE, "falsch",
                 ("«Rauchen verboten».", "Smoking is forbidden.", "„Rauchen verboten.“")),
                (14, "Heute Abend können Sie in diesem Restaurant tanzen.", TRUE_FALSE,
                 "richtig",
                 ("«ab 20 Uhr Tanz».", "Dancing from 8 pm.", "„Ab 20 Uhr Tanz.“")),
                (15, "Von 23 Uhr bis 1 Uhr fährt kein Bus.", TRUE_FALSE, "richtig",
                 ("سرویس تا ۲۳ و از ۱ بامداد است.", "Service runs to 23.00 and from 1.00.",
                  "Verkehr bis 23.00 Uhr und ab 1.00 Uhr.")),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 20,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "سه بخش، ۱۵ سؤال، حدود ۲۰ دقیقه. بخش ۲ فقط یک بار پخش می‌شود.",
        "Three parts, 15 items, about 20 minutes. Part 2 plays only once.",
        "Drei Teile, 15 Aufgaben, circa 20 Minuten. Teil 2 hören Sie nur einmal.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "چه چیزی درست است؟ علامت بزنید: a، b یا c. هر متن را دو بار می‌شنوید.",
                "What is correct? Tick a, b or c. You hear each text twice.",
                "Was ist richtig? Kreuzen Sie an: a, b oder c. Sie hören jeden Text zweimal.",
            ),
            "tracks": [("Teil 1", f"{AUDIO}/teil1.m4a", 2, 20, [1, 2, 3, 4, 5, 6])],
            "example_prompt": "Welche Zimmernummer hat Herr Schneider? → Zimmer 254.",
            "example_answer": "b",
            "items": [
                (1, "Wann fährt der Zug nach Hamburg?",
                 [("a", "Um 9.15 Uhr.", f"{BILD}/zug-0915.svg"),
                  ("b", "Um 9.50 Uhr.", f"{BILD}/zug-0950.svg"),
                  ("c", "Um 10.15 Uhr.", f"{BILD}/zug-1015.svg")], "b", None),
                (2, "Was kostet die Fahrkarte hin und zurück?",
                 [("a", "Zwölf Euro.", f"{BILD}/preis-12.svg"),
                  ("b", "Zwanzig Euro.", f"{BILD}/preis-20.svg"),
                  ("c", "Zweiundzwanzig Euro.", f"{BILD}/preis-22.svg")], "c", None),
                (3, "Wo ist die Apotheke?",
                 [("a", "Neben der Bank.", f"{BILD}/apo-bank.svg"),
                  ("b", "Hinter dem Bahnhof.", f"{BILD}/apo-bahnhof.svg"),
                  ("c", "Gegenüber der Post.", f"{BILD}/apo-post.svg")], "c", None),
                (4, "Was möchte die Frau trinken?",
                 [("a", "Tee.", f"{BILD}/trinken-tee.svg"),
                  ("b", "Kaffee.", f"{BILD}/trinken-kaffee.svg"),
                  ("c", "Wasser.", f"{BILD}/trinken-wasser.svg")], "a", None),
                (5, "Wie wird das Wetter am Sonntag?",
                 [("a", "Es regnet.", f"{BILD}/wetter-regen.svg"),
                  ("b", "Es schneit.", f"{BILD}/wetter-schnee.svg"),
                  ("c", "Die Sonne scheint.", f"{BILD}/wetter-sonne.svg")], "a", None),
                (6, "Wie viele Personen kommen zum Essen?",
                 [("a", "Drei.", f"{BILD}/leute-3.svg"),
                  ("b", "Vier.", f"{BILD}/leute-4.svg"),
                  ("c", "Sechs.", f"{BILD}/leute-6.svg")], "b", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 5,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "علامت بزنید: Richtig یا Falsch. هر متن را فقط یک بار می‌شنوید.",
                "Tick Richtig or Falsch. You hear each text only once.",
                "Kreuzen Sie an: Richtig oder Falsch. Sie hören jeden Text einmal.",
            ),
            "tracks": [("Teil 2", f"{AUDIO}/teil2.m4a", 1, 15, [7, 8, 9, 10])],
            "example_prompt": "Die Reisende soll zur Information in Halle C kommen.",
            "example_answer": "richtig",
            "items": [
                (7, "Der Zug nach Köln hat Verspätung.", TRUE_FALSE, "richtig", None),
                (8, "Das Schwimmbad schließt heute früher.", TRUE_FALSE, "richtig", None),
                (9, "Der Supermarkt ist morgen geschlossen.", TRUE_FALSE, "falsch", None),
                (10, "Die Führung im Museum beginnt um 14 Uhr.", TRUE_FALSE, "falsch", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "چه چیزی درست است؟ علامت بزنید: a، b یا c. هر متن را دو بار می‌شنوید.",
                "What is correct? Tick a, b or c. You hear each text twice.",
                "Was ist richtig? Kreuzen Sie an: a, b oder c. Sie hören jeden Text zweimal.",
            ),
            "tracks": [("Teil 3", f"{AUDIO}/teil3.m4a", 2, 20, [11, 12, 13, 14, 15])],
            "items": [
                (11, "An welchem Tag kommt der Handwerker?",
                 [("a", "Am Montag."), ("b", "Am Dienstag."), ("c", "Am Mittwoch.")], "b", None),
                (12, "Was soll Herr Klein mitbringen?",
                 [("a", "Seinen Pass."), ("b", "Ein Foto."), ("c", "Geld.")], "a", None),
                (13, "Wo treffen sich die Freunde?",
                 [("a", "Im Kino."), ("b", "Im Café."), ("c", "Im Park.")], "c", None),
                (14, "Wann ist der Termin beim Arzt?",
                 [("a", "Um 8.30 Uhr."), ("b", "Um 9.30 Uhr."), ("c", "Um 10.30 Uhr.")],
                 "b", None),
                (15, "Warum ruft Frau Berg an?",
                 [("a", "Sie ist krank."), ("b", "Sie kommt später."),
                  ("c", "Sie hat den Schlüssel.")], "c", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 20,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "دو بخش، حدود ۲۰ دقیقه: پنج جای خالی یک فرم، و یک پیام کوتاه حدود ۳۰ کلمه.",
        "Two parts, about 20 minutes: five gaps in a form, then a short message of ~30 words.",
        "Zwei Teile, circa 20 Minuten: fünf Lücken in einem Formular und eine kurze "
        "Mitteilung von etwa 30 Wörtern.",
    ),
    # Teil 1 is auto-scored; Teil 2 goes to a teacher.
    "max_points": 5,
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "در فرم پنج اطلاعات جا افتاده است. برای هر شماره گزینه درست را انتخاب کنید.",
                "Five pieces of information are missing from the form. Choose the right one "
                "for each number.",
                "In dem Formular fehlen fünf Informationen. Wählen Sie für jede Nummer die "
                "richtige Angabe.",
            ),
            "stimulus_title": "Anmeldung — Busfahrt um den Bodensee",
            "stimulus_intro":
                "Ihre Freundin Eva Kadavy macht mit ihrem Mann und ihren beiden Söhnen "
                "(8 und 11 Jahre alt) Urlaub in Seeheim. Im Reisebüro bucht sie für den "
                "nächsten Sonntag, den 14. Juli, eine Busfahrt um den Bodensee. Sie wohnt "
                "im Hotel Schönblick, Burgstraße 34, 78014 Seeheim. Frau Kadavy hat keine "
                "Kreditkarte.",
            "blocks": [
                ("section", "", "Anmeldung",
                 "Familienname, Vorname: Kadavy, Eva\n"
                 "Anzahl der Personen: (1)\n"
                 "Davon Kinder: (2)\n"
                 "Urlaubsadresse: Hotel Schönblick\n"
                 "Straße, Hausnummer: (3)\n"
                 "PLZ, Urlaubsort: 78014 (4)\n"
                 "Reisetermin: 14. Juli\n"
                 "Zahlungsweise: (5)"),
            ],
            "example_prompt": "Familienname, Vorname → Kadavy, Eva",
            "example_answer": "",
            "items": [
                (1, "(1) Anzahl der Personen",
                 [("a", "2"), ("b", "3"), ("c", "4")], "c",
                 ("زن، شوهر و دو پسر می‌شود چهار نفر.",
                  "Wife, husband and two sons make four.",
                  "Frau, Mann und zwei Söhne sind vier Personen.")),
                (2, "(2) Davon Kinder",
                 [("a", "1"), ("b", "2"), ("c", "0")], "b",
                 ("دو پسر ۸ و ۱۱ ساله.", "Two sons, aged 8 and 11.",
                  "Zwei Söhne, 8 und 11 Jahre alt.")),
                (3, "(3) Straße, Hausnummer",
                 [("a", "Burgstraße 34"), ("b", "Seestraße 34"), ("c", "Burgweg 43")], "a", None),
                (4, "(4) PLZ, Urlaubsort",
                 [("a", "Bodensee"), ("b", "Seeheim"), ("c", "Schönblick")], "b",
                 ("۷۸۰۱۴ کد پستی Seeheim است.", "78014 is the postcode of Seeheim.",
                  "78014 ist die Postleitzahl von Seeheim.")),
                (5, "(5) Zahlungsweise",
                 [("a", "Kreditkarte"), ("b", "Bar"), ("c", "Rechnung")], "b",
                 ("کارت اعتباری ندارد، پس نقدی.", "She has no credit card, so cash.",
                  "Sie hat keine Kreditkarte, also bar.")),
            ],
        },
        {
            "type": "writing",
            "minutes": 12,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "به هر سه نکته یک یا دو جمله بنویسید (حدود ۳۰ کلمه). سلام و خداحافظی هم "
                "بنویسید.",
                "Write one or two sentences on each point (about 30 words). Include a "
                "greeting and a closing.",
                "Schreiben Sie zu jedem Punkt ein bis zwei Sätze (circa 30 Wörter). "
                "Schreiben Sie auch eine Anrede und einen Gruß.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Sie möchten im August Dresden besuchen. Schreiben Sie an die "
                "Touristeninformation.",
            "blocks": [
                ("bullet", "", "", "Warum schreiben Sie?"),
                ("bullet", "", "", "Bitten Sie um Informationen über das Kulturprogramm "
                                   "(Filme, Museen usw.)."),
                ("bullet", "", "", "Fragen Sie nach Hoteladressen."),
            ],
            "items": [(6, "Schreiben Sie die Mitteilung.", None, "", None)],
            "min_words": 30,
        },
    ],
}
