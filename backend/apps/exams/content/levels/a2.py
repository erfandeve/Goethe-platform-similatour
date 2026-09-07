"""Goethe-Zertifikat A2 — original material in the official task shapes.

Lesen 30 min / 20 items · Hören 30 min / 20 items · Schreiben 30 min / 2 tasks.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/a2/hoeren"

LESEN = {
    "skill": "lesen",
    "duration": 30,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "چهار بخش، ۲۰ سؤال، ۳۰ دقیقه. از پیام کوتاه تا آگهی و مقاله کوتاه.",
        "Four parts, 20 items, 30 minutes — from short messages to adverts and a short article.",
        "Vier Teile, 20 Aufgaben, 30 Minuten — von kurzen Mitteilungen bis zu Anzeigen.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "یک مقاله کوتاه از مجله محلی می‌خوانید. گزینه درست را انتخاب کنید.",
                "You read a short article from a local magazine. Choose the correct answer.",
                "Sie lesen einen kurzen Artikel aus einer Stadtzeitung. Wählen Sie die richtige Antwort.",
            ),
            "stimulus_title": "Ein Garten für alle",
            "blocks": [
                ("paragraph", "", "",
                 "Seit zwei Jahren gibt es in Bremen-Nord einen Garten, der allen gehört. "
                 "Zwanzig Familien aus dem Stadtteil arbeiten dort zusammen. Angefangen hat "
                 "alles mit Frau Özdemir, einer Lehrerin aus der Nachbarschaft. Sie hatte die "
                 "Idee, weil viele Kinder im Viertel noch nie eine Kartoffel in der Erde "
                 "gesehen hatten.\n\n"
                 "Heute wachsen dort Tomaten, Salat, Kräuter und sogar Erdbeeren. Jeder darf "
                 "ernten, aber jeder muss auch helfen: zwei Stunden pro Monat sind Pflicht. "
                 "Wer keine Zeit hat, bezahlt stattdessen zehn Euro im Monat. Das Geld ist für "
                 "Samen und Werkzeug.\n\n"
                 "Im Sommer treffen sich die Familien jeden Freitagabend zum Essen. „Am Anfang "
                 "kannten wir uns gar nicht“, sagt Herr Bauer, der seit dreißig Jahren in der "
                 "Straße wohnt. „Jetzt weiß ich, wie meine Nachbarn heißen.“ Im Winter ruht "
                 "der Garten, aber die Treffen gehen weiter — dann im Gemeindehaus."),
            ],
            "items": [
                (1, "Die Idee für den Garten hatte …",
                 [("a", "die Stadt Bremen"), ("b", "eine Lehrerin"), ("c", "Herr Bauer")], "b",
                 ("در متن: «Angefangen hat alles mit Frau Özdemir, einer Lehrerin».",
                  "The text says it started with Frau Özdemir, a teacher.",
                  "Im Text: „Angefangen hat alles mit Frau Özdemir, einer Lehrerin.“")),
                (2, "Wer im Garten ernten will, …",
                 [("a", "muss auch mitarbeiten"), ("b", "muss dort wohnen"),
                  ("c", "braucht eigenes Werkzeug")], "a",
                 ("«jeder muss auch helfen: zwei Stunden pro Monat».",
                  "Everyone must help: two hours a month.",
                  "„Jeder muss auch helfen: zwei Stunden pro Monat.“")),
                (3, "Die zehn Euro im Monat bezahlt man, …",
                 [("a", "wenn man erntet"), ("b", "wenn man nicht helfen kann"),
                  ("c", "wenn man neu ist")], "b",
                 ("«Wer keine Zeit hat, bezahlt stattdessen zehn Euro».",
                  "Those without time pay ten euros instead.",
                  "„Wer keine Zeit hat, bezahlt stattdessen zehn Euro.“")),
                (4, "Herr Bauer findet gut, dass …",
                 [("a", "das Gemüse billig ist"), ("b", "er die Nachbarn kennt"),
                  ("c", "der Garten groß ist")], "b",
                 ("«Jetzt weiß ich, wie meine Nachbarn heißen».",
                  "\"Now I know my neighbours' names.\"",
                  "„Jetzt weiß ich, wie meine Nachbarn heißen.“")),
                (5, "Im Winter …",
                 [("a", "gibt es keine Treffen"), ("b", "treffen sich die Familien woanders"),
                  ("c", "arbeitet niemand mehr mit")], "b",
                 ("«dann im Gemeindehaus».", "They meet in the community hall.",
                  "„dann im Gemeindehaus“.")),
            ],
        },
        {
            "type": "match_person",
            "minutes": 8,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "چهار نفر درباره رفت‌وآمد روزانه‌شان نوشته‌اند. هر جمله به کدام نفر مربوط است؟ "
                "هر نفر می‌تواند چند بار انتخاب شود.",
                "Four people write about their daily commute. Which person does each statement "
                "fit? A person can be chosen more than once.",
                "Vier Personen schreiben über ihren Weg zur Arbeit. Auf wen trifft jede Aussage "
                "zu? Personen können mehrmals gewählt werden.",
            ),
            "stimulus_title": "Wie komme ich zur Arbeit?",
            "pool": [("a", "Selin"), ("b", "Jonas"), ("c", "Marta"), ("d", "Ferdi")],
            "blocks": [
                ("person", "a", "Selin",
                 "Ich fahre jeden Morgen mit dem Rad, auch im Winter. Vierzig Minuten, bei "
                 "jedem Wetter. Danach bin ich wach und brauche keinen Kaffee mehr. Ein Auto "
                 "habe ich nie gehabt und will auch keins."),
                ("person", "b", "Jonas",
                 "Ich arbeite drei Tage in der Woche zu Hause. An den anderen zwei Tagen nehme "
                 "ich den Zug, das dauert eine Stunde. Im Zug lese ich oder schlafe noch etwas. "
                 "Das Ticket bezahlt meine Firma."),
                ("person", "c", "Marta",
                 "Ich bringe morgens erst die Kinder in die Schule und fahre dann weiter ins "
                 "Büro. Ohne Auto geht das nicht. Der Weg ist kurz, aber der Verkehr ist "
                 "schrecklich. Am liebsten würde ich zu Fuß gehen."),
                ("person", "d", "Ferdi",
                 "Mein Weg dauert nur zehn Minuten zu Fuß. Ich habe extra eine Wohnung in der "
                 "Nähe gesucht, auch wenn die Miete höher ist. Zeit ist mir wichtiger als Geld."),
            ],
            "example_prompt": "Wer geht zu Fuß zur Arbeit?",
            "example_answer": "d",
            "items": [
                (6, "Wer fährt auch bei schlechtem Wetter mit dem Rad?", None, "a", None),
                (7, "Wer arbeitet manchmal von zu Hause?", None, "b", None),
                (8, "Wer bezahlt mehr Miete, um näher zu wohnen?", None, "d", None),
                (9, "Wer bringt vorher Kinder weg?", None, "c", None),
                (10, "Wer bekommt die Fahrkosten von der Firma?", None, "b", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "پنج آگهی و اطلاعیه را می‌خوانید. آیا جمله درست است یا غلط؟",
                "You read five adverts and notices. Is each statement true or false?",
                "Sie lesen fünf Anzeigen und Aushänge. Ist die Aussage richtig oder falsch?",
            ),
            "stimulus_title": "Anzeigen aus der Stadt",
            "blocks": [
                ("paragraph", "11", "Volkshochschule",
                 "Kochkurs „Vegetarisch für Anfänger“, sechs Abende ab 4. April, jeweils "
                 "Donnerstag 18–20:30 Uhr. 78 Euro inklusive Zutaten. Mindestens 8 Personen."),
                ("paragraph", "12", "Fitnessstudio Aktiv",
                 "Neu: Probetraining kostenlos, aber nur mit Termin. Anmeldung online. "
                 "Mitgliedschaft ab 29 Euro im Monat, Mindestlaufzeit 12 Monate."),
                ("paragraph", "13", "Umzug — Möbel abzugeben",
                 "Sofa, Tisch und vier Stühle. Alles gut erhalten. Abholung bis 20. Juni, "
                 "danach kommt der Sperrmüll. Kostenlos, aber Sie brauchen ein Auto."),
                ("paragraph", "14", "Stadtbücherei",
                 "Ab Juli neue Öffnungszeiten: Dienstag bis Samstag 11–18 Uhr. Montags "
                 "geschlossen. Ausleihe weiterhin kostenlos für Kinder und Jugendliche."),
                ("paragraph", "15", "Nachhilfe",
                 "Studentin (Mathematik, 6. Semester) gibt Nachhilfe für Klasse 5 bis 10. "
                 "15 Euro pro Stunde, bei Ihnen zu Hause. Auch in den Ferien."),
            ],
            "items": [
                (11, "Der Kochkurs findet einmal pro Woche statt.", TRUE_FALSE, "richtig",
                 ("«jeweils Donnerstag» یعنی هفته‌ای یک بار.",
                  "\"Jeweils Donnerstag\" means once a week.",
                  "„Jeweils Donnerstag“ heißt einmal pro Woche.")),
                (12, "Das Probetraining kann man ohne Anmeldung machen.", TRUE_FALSE, "falsch",
                 ("«nur mit Termin».", "Only with an appointment.", "„Nur mit Termin.“")),
                (13, "Die Möbel kosten nichts.", TRUE_FALSE, "richtig",
                 ("«Kostenlos, aber Sie brauchen ein Auto».",
                  "Free, but you need a car.", "„Kostenlos, aber Sie brauchen ein Auto.“")),
                (14, "Die Bücherei ist ab Juli auch montags offen.", TRUE_FALSE, "falsch",
                 ("«Montags geschlossen».", "Closed on Mondays.", "„Montags geschlossen.“")),
                (15, "Die Studentin kommt zu den Schülern nach Hause.", TRUE_FALSE, "richtig",
                 ("«bei Ihnen zu Hause».", "\"At your home.\"", "„Bei Ihnen zu Hause.“")),
            ],
        },
        {
            "type": "match_heading",
            "minutes": 7,
            "title": ("لزن ۴", "Lesen 4", "Lesen 4"),
            "instructions": (
                "پنج ایمیل کوتاه می‌خوانید. برای هر ایمیل موضوع مناسب را از فهرست a تا h انتخاب "
                "کنید. دو موضوع اضافه است.",
                "You read five short emails. Choose the matching subject from a–h for each. "
                "Two subjects are extra.",
                "Sie lesen fünf kurze E-Mails. Wählen Sie für jede den passenden Betreff aus "
                "a–h. Zwei Betreffs bleiben übrig.",
            ),
            "stimulus_title": "Fünf E-Mails",
            "pool": [
                ("a", "Termin verschieben"),
                ("b", "Rechnung stimmt nicht"),
                ("c", "Einladung zum Fest"),
                ("d", "Wohnung gesucht"),
                ("e", "Paket nicht angekommen"),
                ("f", "Urlaub beantragen"),
                ("g", "Kurs absagen"),
                ("h", "Nach dem Weg fragen"),
            ],
            "blocks": [
                ("paragraph", "16", "",
                 "Hallo Frau Kern, leider bin ich am Mittwoch auf einer Fortbildung. Können "
                 "wir uns stattdessen am Freitag um 14 Uhr sehen? Viele Grüße, M. Ricci"),
                ("paragraph", "17", "",
                 "Sehr geehrte Damen und Herren, ich habe am 3. Mai bestellt und die "
                 "Sendungsnummer bekommen. Bis heute ist nichts angekommen. Können Sie "
                 "nachsehen, wo die Sendung ist?"),
                ("paragraph", "18", "",
                 "Liebe Kolleginnen und Kollegen, am 12. Juli werde ich 40 und möchte das "
                 "gern mit euch feiern. Ab 18 Uhr im Garten, für Essen ist gesorgt. Sagt mir "
                 "bitte bis Freitag Bescheid."),
                ("paragraph", "19", "",
                 "Sehr geehrter Herr Lang, auf der letzten Abrechnung stehen 180 Euro für "
                 "Strom. Im Vertrag steht aber 120 Euro pro Quartal. Bitte prüfen Sie das."),
                ("paragraph", "20", "",
                 "Hallo, ich bin ab September für ein Praktikum in Leipzig und suche ein "
                 "Zimmer oder eine kleine Wohnung für vier Monate. Möbliert wäre ideal."),
            ],
            "items": [
                (16, "E-Mail 16", None, "a", None),
                (17, "E-Mail 17", None, "e", None),
                (18, "E-Mail 18", None, "c", None),
                (19, "E-Mail 19", None, "b", None),
                (20, "E-Mail 20", None, "d", None),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 30,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "چهار بخش، ۲۰ سؤال، ۳۰ دقیقه. بخش دوم فقط یک بار پخش می‌شود.",
        "Four parts, 20 items, 30 minutes. Part two plays only once.",
        "Vier Teile, 20 Aufgaben, 30 Minuten. Teil zwei hören Sie nur einmal.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "پنج گفتگوی کوتاه می‌شنوید، هرکدام دو بار. گزینه درست را انتخاب کنید.",
                "You hear five short conversations, each twice. Choose the right answer.",
                "Sie hören fünf kurze Gespräche, jedes zweimal. Wählen Sie die richtige Antwort.",
            ),
            "tracks": [("Teil 1", f"{AUDIO}/teil1.m4a", 2, 20, [1, 2, 3, 4, 5])],
            "items": [
                (1, "Was hat die Frau vergessen?",
                 [("a", "den Schlüssel"), ("b", "das Handy"), ("c", "die Tasche")], "b", None),
                (2, "Wo findet das Treffen statt?",
                 [("a", "im Büro"), ("b", "im Restaurant"), ("c", "online")], "c", None),
                (3, "Wie lange dauert die Fahrt?",
                 [("a", "eine halbe Stunde"), ("b", "eine Stunde"), ("c", "zwei Stunden")], "a", None),
                (4, "Was möchte der Mann kaufen?",
                 [("a", "eine Jacke"), ("b", "Schuhe"), ("c", "eine Hose")], "c", None),
                (5, "Warum kommt Lena nicht mit?",
                 [("a", "Sie muss arbeiten."), ("b", "Sie ist müde."), ("c", "Sie hat Besuch.")],
                 "a", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "یک گفتگو در رادیو می‌شنوید، فقط یک بار. درست یا غلط؟",
                "You hear a radio interview once only. True or false?",
                "Sie hören ein Radiointerview, nur einmal. Richtig oder falsch?",
            ),
            "tracks": [("Teil 2", f"{AUDIO}/teil2.m4a", 1, 20, [6, 7, 8, 9, 10])],
            "items": [
                (6, "Herr Nowak arbeitet seit zehn Jahren als Bäcker.", TRUE_FALSE, "falsch", None),
                (7, "Er steht jeden Tag um drei Uhr auf.", TRUE_FALSE, "richtig", None),
                (8, "Am Wochenende hat die Bäckerei geschlossen.", TRUE_FALSE, "falsch", None),
                (9, "Sein Lieblingsbrot ist das Roggenbrot.", TRUE_FALSE, "richtig", None),
                (10, "Er möchte den Beruf wechseln.", TRUE_FALSE, "falsch", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 8,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "پنج پیام و اعلان می‌شنوید، هرکدام دو بار.",
                "You hear five messages and announcements, each twice.",
                "Sie hören fünf Nachrichten und Durchsagen, jede zweimal.",
            ),
            "tracks": [("Teil 3", f"{AUDIO}/teil3.m4a", 2, 20, [11, 12, 13, 14, 15])],
            "items": [
                (11, "Der Deutschkurs beginnt …",
                 [("a", "am 2. September"), ("b", "am 12. September"), ("c", "am 20. September")],
                 "b", None),
                (12, "Das Konzert ist …",
                 [("a", "abgesagt"), ("b", "verschoben"), ("c", "ausverkauft")], "b", None),
                (13, "Der Anrufer möchte …",
                 [("a", "einen Termin"), ("b", "eine Auskunft"), ("c", "eine Reklamation")],
                 "a", None),
                (14, "Die Bahn fährt heute …",
                 [("a", "pünktlich"), ("b", "von Gleis 5"), ("c", "gar nicht")], "b", None),
                (15, "Das Paket liegt …",
                 [("a", "beim Nachbarn"), ("b", "in der Filiale"), ("c", "vor der Tür")], "a", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 7,
            "title": ("هؤرن ۴", "Hören 4", "Hören 4"),
            "instructions": (
                "یک گفتگوی طولانی‌تر بین دو نفر می‌شنوید، دو بار.",
                "You hear a longer conversation between two people, twice.",
                "Sie hören ein längeres Gespräch zwischen zwei Personen, zweimal.",
            ),
            "tracks": [("Teil 4", f"{AUDIO}/teil4.m4a", 2, 20, [16, 17, 18, 19, 20])],
            "items": [
                (16, "Die beiden planen …",
                 [("a", "einen Umzug"), ("b", "eine Reise"), ("c", "eine Party")], "b", None),
                (17, "Sie fahren …",
                 [("a", "mit dem Auto"), ("b", "mit dem Zug"), ("c", "mit dem Flugzeug")], "b", None),
                (18, "Das Hotel ist …",
                 [("a", "im Zentrum"), ("b", "am See"), ("c", "am Bahnhof")], "b", None),
                (19, "Sie bleiben …",
                 [("a", "drei Tage"), ("b", "fünf Tage"), ("c", "eine Woche")], "a", None),
                (20, "Was nehmen sie auf keinen Fall mit?",
                 [("a", "den Laptop"), ("b", "die Wanderschuhe"), ("c", "den Regenschirm")],
                 "a", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 30,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "دو تکلیف، ۳۰ دقیقه: یک پیام کوتاه و یک ایمیل نیمه‌رسمی.",
        "Two tasks, 30 minutes: a short message and a semi-formal email.",
        "Zwei Aufgaben, 30 Minuten: eine kurze Mitteilung und eine halbformelle E-Mail.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 12,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "به دوستتان یک پیام بنویسید، حدود ۴۰ کلمه. هر سه نکته را پوشش دهید.",
                "Write a message to a friend, about 40 words, covering all three points.",
                "Schreiben Sie eine Mitteilung an eine Freundin, etwa 40 Wörter, zu allen drei "
                "Punkten.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Sie haben zwei Karten für ein Konzert am Samstag. Schreiben Sie an Ihre "
                "Freundin Dilan.",
            "blocks": [
                ("bullet", "", "", "Laden Sie Dilan ein."),
                ("bullet", "", "", "Schreiben Sie, wann und wo Sie sich treffen."),
                ("bullet", "", "", "Fragen Sie, ob sie danach noch essen gehen möchte."),
            ],
            "items": [(1, "Schreiben Sie die Mitteilung.", None, "", None)],
            "min_words": 40,
        },
        {
            "type": "writing",
            "minutes": 18,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "یک ایمیل نیمه‌رسمی بنویسید، حدود ۵۰ کلمه. مؤدبانه بنویسید و هر سه نکته را "
                "پوشش دهید.",
                "Write a semi-formal email, about 50 words. Be polite and cover all three points.",
                "Schreiben Sie eine halbformelle E-Mail, etwa 50 Wörter. Bleiben Sie höflich und "
                "behandeln Sie alle drei Punkte.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Sie haben einen Sprachkurs gebucht, können aber am ersten Abend nicht kommen. "
                "Schreiben Sie an die Kursleitung, Frau Dr. Hoffmann.",
            "blocks": [
                ("bullet", "", "", "Entschuldigen Sie sich."),
                ("bullet", "", "", "Nennen Sie einen Grund."),
                ("bullet", "", "", "Fragen Sie nach dem Material der ersten Stunde."),
            ],
            "items": [(2, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 50,
        },
    ],
}
