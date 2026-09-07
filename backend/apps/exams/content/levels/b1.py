"""Goethe-Zertifikat B1 — original material in the official task shapes.

Lesen 65 min / 30 items · Hören 40 min / 30 items · Schreiben 60 min / 3 tasks.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/b1/hoeren"

LESEN = {
    "skill": "lesen",
    "duration": 65,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "پنج بخش، ۳۰ سؤال، ۶۵ دقیقه. بلاگ، آگهی، مقاله و متن رسمی.",
        "Five parts, 30 items, 65 minutes: a blog, adverts, an article and an official text.",
        "Fünf Teile, 30 Aufgaben, 65 Minuten: Blog, Anzeigen, Artikel und ein amtlicher Text.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 12,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "یک مطلب وبلاگی می‌خوانید. آیا جمله‌ها درست‌اند یا غلط؟",
                "You read a blog post. Are the statements true or false?",
                "Sie lesen einen Blogbeitrag. Sind die Aussagen richtig oder falsch?",
            ),
            "stimulus_title": "Ein Jahr ohne Auto — mein Fazit",
            "blocks": [
                ("paragraph", "", "",
                 "Vor genau einem Jahr habe ich mein Auto verkauft. Nicht aus Überzeugung, "
                 "sondern weil die Reparatur teurer gewesen wäre als der Wagen wert war. Ich "
                 "dachte, ich halte das höchstens zwei Monate durch.\n\n"
                 "Die ersten Wochen waren tatsächlich anstrengend. Ich habe unterschätzt, wie "
                 "viel Zeit man mit Warten verbringt, wenn man auf Busse angewiesen ist. Zweimal "
                 "bin ich zu spät zur Arbeit gekommen, einmal musste ich einen Zahnarzttermin "
                 "absagen. Meine Kollegin hat mir dann geraten, alles eine Viertelstunde früher "
                 "zu planen. Das klingt banal, hat aber fast alle Probleme gelöst.\n\n"
                 "Was mich überrascht hat, ist das Geld. Ich hatte mit Ersparnissen gerechnet, "
                 "aber nicht mit so vielen: Versicherung, Steuer, Werkstatt, Benzin und Parken "
                 "zusammen waren deutlich mehr als die Monatskarte und die paar Mietwagen im "
                 "Jahr. Am Ende bleiben mir gut zweitausend Euro mehr.\n\n"
                 "Trotzdem würde ich nicht sagen, dass ein Leben ohne Auto für jeden passt. Wer "
                 "auf dem Land wohnt oder kleine Kinder zu drei verschiedenen Orten bringen "
                 "muss, hat es deutlich schwerer als ich in der Stadt. Und im Winter, wenn ich "
                 "im Regen auf den Bus warte, denke ich schon manchmal wehmütig an die Heizung "
                 "im Auto. Aber kaufen werde ich mir keins mehr."),
            ],
            "items": [
                (1, "Der Autor hat sein Auto aus Umweltgründen verkauft.", TRUE_FALSE, "falsch",
                 ("«Nicht aus Überzeugung, sondern weil die Reparatur teurer gewesen wäre».",
                  "He sold it because the repair cost more than the car was worth.",
                  "„Nicht aus Überzeugung, sondern weil die Reparatur teurer gewesen wäre.“")),
                (2, "Am Anfang hatte er Probleme mit der Pünktlichkeit.", TRUE_FALSE, "richtig",
                 ("دو بار دیر به سر کار رسیده.", "He was late for work twice.",
                  "Er kam zweimal zu spät zur Arbeit.")),
                (3, "Der Tipp seiner Kollegin hat wenig geholfen.", TRUE_FALSE, "falsch",
                 ("«hat aber fast alle Probleme gelöst».", "It solved almost all the problems.",
                  "„Hat aber fast alle Probleme gelöst.“")),
                (4, "Er spart mehr Geld als erwartet.", TRUE_FALSE, "richtig",
                 ("«nicht mit so vielen» — بیشتر از انتظارش بوده.",
                  "More than he had expected.", "Mehr, als er erwartet hatte.")),
                (5, "Er empfiehlt allen Menschen, das Auto abzuschaffen.", TRUE_FALSE, "falsch",
                 ("می‌گوید برای همه مناسب نیست.", "He says it does not suit everyone.",
                  "Er sagt, es passe nicht für jeden.")),
                (6, "Er möchte später wieder ein Auto kaufen.", TRUE_FALSE, "falsch",
                 ("«Aber kaufen werde ich mir keins mehr».",
                  "\"But I will not buy one again.\"", "„Aber kaufen werde ich mir keins mehr.“")),
            ],
        },
        {
            "type": "mcq",
            "minutes": 12,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "دو متن از یک مجله می‌خوانید. برای هر متن سه سؤال چهارگزینه‌ای هست.",
                "You read two magazine texts, each with three multiple-choice questions.",
                "Sie lesen zwei Zeitschriftentexte mit je drei Multiple-Choice-Fragen.",
            ),
            "stimulus_title": "Zwei Texte",
            "blocks": [
                ("paragraph", "Text 1", "Warum wir schlecht schätzen",
                 "Wenn Menschen raten sollen, wie lange eine Aufgabe dauert, liegen sie fast "
                 "immer daneben — und zwar systematisch zu optimistisch. Forscher nennen das "
                 "den Planungsfehler. Studierende, die ihre Abschlussarbeit planen, brauchen im "
                 "Schnitt die Hälfte länger als gedacht, selbst wenn sie schon einmal eine "
                 "Arbeit geschrieben haben. Interessant ist: Dieselben Personen schätzen die "
                 "Dauer bei anderen ziemlich genau ein. Das Problem entsteht also nicht aus "
                 "Unwissen, sondern aus der eigenen Beteiligung. Wer plant, denkt an den "
                 "idealen Ablauf und blendet Störungen aus, die er bei Fremden selbstverständlich "
                 "einrechnet. Eine einfache Gegenmaßnahme hilft erstaunlich gut: die eigene "
                 "Schätzung aufschreiben und mit dem letzten vergleichbaren Projekt vergleichen."),
                ("paragraph", "Text 2", "Der lange Weg zum Handwerk",
                 "Betriebe suchen händeringend Auszubildende, gleichzeitig bleiben viele "
                 "Jugendliche unentschlossen. Eine Untersuchung aus Nordrhein-Westfalen zeigt, "
                 "dass es weniger am Gehalt liegt als am Bild des Berufs: Handwerk gilt vielen "
                 "als körperlich hart und wenig zukunftssicher. Dabei verdienen Gesellen in "
                 "einigen Gewerken nach wenigen Jahren mehr als Berufsanfänger mit Studium, und "
                 "die Übernahmequote liegt bei über neunzig Prozent. Betriebe, die Schülern "
                 "früh ein Praktikum anbieten, finden deutlich leichter Nachwuchs — nicht weil "
                 "sie besser zahlen, sondern weil ein Tag in der Werkstatt mehr erklärt als jede "
                 "Broschüre."),
            ],
            "items": [
                (7, "Der Planungsfehler bedeutet, dass Menschen …",
                 [("a", "die Dauer zu kurz einschätzen"),
                  ("b", "Aufgaben gar nicht planen"),
                  ("c", "zu viel Zeit einplanen")], "a", None),
                (8, "Bei anderen Personen schätzen dieselben Menschen …",
                 [("a", "noch schlechter"), ("b", "ziemlich genau"), ("c", "gar nicht")], "b", None),
                (9, "Als Gegenmittel empfiehlt der Text …",
                 [("a", "mehr Erfahrung zu sammeln"),
                  ("b", "die Schätzung mit früheren Projekten zu vergleichen"),
                  ("c", "Aufgaben abzugeben")], "b", None),
                (10, "Junge Leute entscheiden sich laut Text vor allem deshalb gegen das "
                     "Handwerk, weil …",
                 [("a", "die Bezahlung schlecht ist"),
                  ("b", "das Bild des Berufs sie abschreckt"),
                  ("c", "es zu wenige Stellen gibt")], "b", None),
                (11, "Die Übernahmequote nach der Ausbildung ist …",
                 [("a", "sehr hoch"), ("b", "etwa die Hälfte"), ("c", "unbekannt")], "a", None),
                (12, "Praktika helfen den Betrieben, weil sie …",
                 [("a", "billiger sind als Werbung"),
                  ("b", "den Beruf konkret zeigen"),
                  ("c", "gesetzlich vorgeschrieben sind")], "b", None),
            ],
        },
        {
            "type": "match_heading",
            "minutes": 13,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "برای هر موقعیت، آگهی مناسب را از a تا j انتخاب کنید. برای دو موقعیت آگهی "
                "مناسبی وجود ندارد؛ در آن صورت گزینه x را انتخاب کنید.",
                "For each situation choose the fitting advert from a–j. For two situations "
                "there is none; choose x then.",
                "Wählen Sie für jede Situation die passende Anzeige aus a–j. Für zwei "
                "Situationen gibt es keine; wählen Sie dann x.",
            ),
            "stimulus_title": "Anzeigen",
            "blocks": [
                ("heading", "a", "Möbelmarkt Lehmann",
                 "Lieferung und Aufbau, auch abends nach 18 Uhr. Wir bringen Ihre Möbel bis in "
                 "die Wohnung."),
                ("heading", "b", "Sprachtandem Uni Jena",
                 "Kostenlos Deutsch sprechen — Sie bringen Ihre Sprache mit. Wöchentliche "
                 "Treffen, keine Anmeldung nötig."),
                ("heading", "c", "Hundebetreuung Pfote",
                 "Stundenweise oder über Nacht, auch für mehrere Wochen. Erfahrene Betreuung "
                 "mit großem Garten."),
                ("heading", "d", "Fahrschule Ost",
                 "Intensivkurs in zwei Wochen: Theorie und Praxis am Stück, Prüfung am Ende "
                 "des Kurses."),
                ("heading", "e", "Nähwerkstatt",
                 "Reparaturen und Änderungen aller Art, fertig innerhalb von 48 Stunden. "
                 "Hosen kürzen ab 12 Euro."),
                ("heading", "f", "Wanderverein Harz",
                 "Geführte Touren jeden zweiten Sonntag, für Anfänger und Geübte. Mitglieder "
                 "zahlen nichts."),
                ("heading", "g", "Umzugshilfe Studenten",
                 "Stundenweise buchbar, mit Transporter und zwei kräftigen Helfern. Auch "
                 "kurzfristig."),
                ("heading", "h", "Musikschule Kadenz",
                 "Klavierunterricht ab 6 Jahren, Einzel- und Gruppenstunden, Probestunde "
                 "kostenlos."),
                ("heading", "i", "Reparaturcafé",
                 "Bringen Sie Ihr defektes Gerät mit — wir reparieren gemeinsam statt "
                 "wegzuwerfen. Jeden Samstag."),
                ("heading", "j", "Bürogemeinschaft Mitte",
                 "Schreibtisch tageweise mieten, mit Internet und Küche. Keine Mindestlaufzeit."),
            ],
            "pool": [
                ("a", "Möbelmarkt Lehmann — Lieferung und Aufbau, auch abends"),
                ("b", "Sprachtandem Uni Jena — kostenlos Deutsch gegen Ihre Sprache"),
                ("c", "Hundebetreuung Pfote — stundenweise oder über Nacht"),
                ("d", "Fahrschule Ost — Intensivkurs in zwei Wochen"),
                ("e", "Nähwerkstatt — Reparaturen und Änderungen, 48 Stunden"),
                ("f", "Wanderverein Harz — geführte Touren, jeden zweiten Sonntag"),
                ("g", "Umzugshilfe Studenten — stundenweise, mit Transporter"),
                ("h", "Musikschule Kadenz — Klavier ab 6 Jahren"),
                ("i", "Reparaturcafé — bringen Sie Ihr defektes Gerät mit"),
                ("j", "Bürogemeinschaft Mitte — Schreibtisch tageweise mieten"),
                ("x", "keine passende Anzeige"),
            ],
            "items": [
                (13, "Ihr Wasserkocher ist kaputt, wegwerfen möchten Sie ihn nicht.", None, "i", None),
                (14, "Sie sind neu in der Stadt und möchten Ihr Deutsch üben, ohne zu bezahlen.",
                 None, "b", None),
                (15, "Sie ziehen um und brauchen für einen Nachmittag zwei starke Helfer.",
                 None, "g", None),
                (16, "Ihre Hose ist zu lang und soll bis Freitag fertig sein.", None, "e", None),
                (17, "Sie arbeiten als Freiberuflerin und brauchen nur an zwei Tagen pro Woche "
                     "einen Arbeitsplatz.", None, "j", None),
                (18, "Sie suchen einen Zahnarzt, der auch am Samstag Sprechstunde hat.",
                 None, "x", None),
                (19, "Sie fahren zwei Wochen weg und brauchen jemanden für Ihren Hund.",
                 None, "c", None),
                (20, "Sie möchten Ihren Führerschein möglichst schnell machen.", None, "d", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 13,
            "title": ("لزن ۴", "Lesen 4", "Lesen 4"),
            "instructions": (
                "نظرهای خوانندگان درباره یک موضوع را می‌خوانید. آیا نویسنده موافق است یا مخالف؟",
                "You read readers' comments on a topic. Is the writer for or against?",
                "Sie lesen Leserkommentare zu einem Thema. Ist die Person dafür oder dagegen?",
            ),
            "stimulus_title": "Sollen Handys in der Schule verboten werden?",
            "blocks": [
                ("statement", "21", "Bilal, 34",
                 "Ich unterrichte seit acht Jahren. In der Pause reden die Kinder nicht mehr "
                 "miteinander, sie sitzen nebeneinander und schauen auf ihre Bildschirme. Seit "
                 "wir die Geräte morgens einsammeln, ist der Schulhof wieder laut — im besten "
                 "Sinne."),
                ("statement", "22", "Regina, 41",
                 "Ein Verbot löst gar nichts. Die Kinder lernen dann eben nicht, verantwortlich "
                 "mit dem Gerät umzugehen, sondern nur, es zu verstecken. Besser wäre "
                 "Medienunterricht ab der fünften Klasse."),
                ("statement", "23", "Tarek, 19",
                 "Ich habe mein Abitur letztes Jahr gemacht. Ohne Handy hätte ich die Hälfte "
                 "der Hausaufgaben nicht geschafft — Termine, Gruppenchats, Fotos von der "
                 "Tafel. Wer das verbietet, macht Schule schwieriger, nicht besser."),
                ("statement", "24", "Heike, 52",
                 "Meine Tochter ist in der siebten Klasse und war nach jedem Schultag völlig "
                 "erschöpft. Seit dem Verbot an ihrer Schule schläft sie besser und die Noten "
                 "sind gestiegen. Ich hätte nicht gedacht, dass das so viel ausmacht."),
                ("statement", "25", "Milan, 28",
                 "Im Notfall muss ein Kind seine Eltern erreichen können. Diesen Punkt hört man "
                 "in der Debatte fast nie, und für mich wiegt er schwerer als ein bisschen "
                 "Ablenkung im Unterricht."),
                ("statement", "26", "Anke, 45",
                 "Wir haben es an unserer Schule ein Jahr lang ausprobiert. Die Ergebnisse "
                 "waren eindeutig: weniger Streit, weniger Mobbing, ruhigere Klassen. Ich war "
                 "vorher skeptisch und bin es heute nicht mehr."),
            ],
            "items": [
                (21, "Bilal", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dafuer", None),
                (22, "Regina", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dagegen", None),
                (23, "Tarek", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dagegen", None),
                (24, "Heike", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dafuer", None),
                (25, "Milan", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dagegen", None),
                (26, "Anke", [("dafuer", "dafür"), ("dagegen", "dagegen")], "dafuer", None),
            ],
        },
        {
            "type": "gap_drag",
            "minutes": 15,
            "title": ("لزن ۵", "Lesen 5", "Lesen 5"),
            "instructions": (
                "یک متن رسمی می‌خوانید. جای خالی را با گزینه مناسب پر کنید.",
                "You read an official text. Fill each gap with the right option.",
                "Sie lesen einen amtlichen Text. Füllen Sie die Lücken mit der passenden Option.",
            ),
            "stimulus_title": "Benutzungsordnung der Stadtbibliothek",
            "blocks": [
                ("section", "", "",
                 "§ 1 Die Benutzung der Bibliothek ist kostenlos. Für die Ausleihe ist "
                 "[[27]] ein gültiger Ausweis erforderlich."),
                ("section", "", "",
                 "§ 2 Medien werden für vier Wochen ausgeliehen. Eine Verlängerung ist zweimal "
                 "möglich, [[28]] das Medium nicht von einer anderen Person vorgemerkt wurde."),
                ("section", "", "",
                 "§ 3 Wird die Leihfrist überschritten, [[29]] eine Gebühr von 0,20 Euro pro Tag "
                 "und Medium erhoben."),
                ("section", "", "",
                 "§ 4 Beschädigte Medien sind zu ersetzen. [[30]] ein Ersatz nicht möglich ist, "
                 "wird der Zeitwert berechnet."),
            ],
            "pool": [
                ("a", "jedoch"), ("b", "sofern"), ("c", "wird"), ("d", "Falls"),
                ("e", "trotzdem"), ("f", "obwohl"), ("g", "werden"), ("h", "damit"),
            ],
            "items": [
                (27, "Lücke 27", None, "a", None),
                (28, "Lücke 28", None, "b", None),
                (29, "Lücke 29", None, "c", None),
                (30, "Lücke 30", None, "d", None),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 40,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "چهار بخش، ۳۰ سؤال، ۴۰ دقیقه. بخش‌های ۱ و ۳ فقط یک بار پخش می‌شوند.",
        "Four parts, 30 items, 40 minutes. Parts 1 and 3 play only once.",
        "Vier Teile, 30 Aufgaben, 40 Minuten. Teil 1 und 3 hören Sie nur einmal.",
    ),
    "parts": [
        {
            "type": "listening_mixed",
            "minutes": 10,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "پنج پیام کوتاه می‌شنوید، هرکدام یک بار. برای هر پیام یک سؤال درست/غلط و یک "
                "سؤال سه‌گزینه‌ای هست.",
                "You hear five short messages, once each. Each has a true/false item and a "
                "three-option item.",
                "Sie hören fünf kurze Texte, jeweils einmal. Zu jedem gibt es eine "
                "Richtig/Falsch-Aufgabe und eine Aufgabe mit drei Optionen.",
            ),
            "tracks": [("Teil 1", f"{AUDIO}/teil1.m4a", 1, 25, list(range(1, 11)))],
            "items": [
                (1, "Der Anruf kommt von der Werkstatt.", TRUE_FALSE, "richtig", None),
                (2, "Das Auto ist fertig …",
                 [("a", "heute"), ("b", "morgen"), ("c", "übermorgen")], "b", None),
                (3, "Die Veranstaltung findet draußen statt.", TRUE_FALSE, "falsch", None),
                (4, "Der neue Ort ist …",
                 [("a", "die Turnhalle"), ("b", "das Rathaus"), ("c", "die Aula")], "c", None),
                (5, "Frau Ritter sucht eine Wohnung.", TRUE_FALSE, "falsch", None),
                (6, "Sie ruft an wegen …",
                 [("a", "eines Termins"), ("b", "einer Rechnung"), ("c", "eines Praktikums")],
                 "c", None),
                (7, "Der Kurs ist schon ausgebucht.", TRUE_FALSE, "richtig", None),
                (8, "Man kann sich …",
                 [("a", "auf eine Warteliste setzen lassen"), ("b", "später anmelden"),
                  ("c", "das Geld zurückholen")], "a", None),
                (9, "Die Straße ist wegen einer Baustelle gesperrt.", TRUE_FALSE, "richtig", None),
                (10, "Die Sperrung dauert …",
                 [("a", "bis Freitag"), ("b", "zwei Wochen"), ("c", "einen Monat")], "b", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "یک سخنرانی کوتاه در یک بازدید می‌شنوید، دو بار.",
                "You hear a short talk during a guided tour, twice.",
                "Sie hören einen kurzen Vortrag bei einer Führung, zweimal.",
            ),
            "tracks": [("Teil 2", f"{AUDIO}/teil2.m4a", 2, 25, list(range(11, 16)))],
            "items": [
                (11, "Das Gebäude war früher …",
                 [("a", "eine Fabrik"), ("b", "eine Schule"), ("c", "ein Krankenhaus")], "a", None),
                (12, "Die Renovierung dauerte …",
                 [("a", "zwei Jahre"), ("b", "vier Jahre"), ("c", "sieben Jahre")], "b", None),
                (13, "Heute wird das Haus genutzt für …",
                 [("a", "Wohnungen"), ("b", "Büros und Ateliers"), ("c", "ein Museum")], "b", None),
                (14, "Die Führung dauert insgesamt …",
                 [("a", "45 Minuten"), ("b", "eine Stunde"), ("c", "90 Minuten")], "c", None),
                (15, "Fotografieren ist …",
                 [("a", "überall erlaubt"), ("b", "nur im Hof erlaubt"), ("c", "verboten")],
                 "b", None),
            ],
        },
        {
            "type": "listening_mixed",
            "minutes": 10,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "یک گفتگوی روزمره می‌شنوید، فقط یک بار.",
                "You hear an everyday conversation, only once.",
                "Sie hören ein Alltagsgespräch, nur einmal.",
            ),
            "tracks": [("Teil 3", f"{AUDIO}/teil3.m4a", 1, 25, list(range(16, 23)))],
            "items": [
                (16, "Die beiden kennen sich von der Arbeit.", TRUE_FALSE, "falsch", None),
                (17, "Lena hat gerade eine neue Stelle.", TRUE_FALSE, "richtig", None),
                (18, "Sie arbeitet jetzt näher an ihrer Wohnung.", TRUE_FALSE, "richtig", None),
                (19, "Sie verdient weniger als vorher.", TRUE_FALSE, "falsch", None),
                (20, "Ihr Chef ist unfreundlich.", TRUE_FALSE, "falsch", None),
                (21, "Sie möchte nebenbei weiterstudieren.", TRUE_FALSE, "richtig", None),
                (22, "Die beiden verabreden sich für nächste Woche.", TRUE_FALSE, "richtig", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۴", "Hören 4", "Hören 4"),
            "instructions": (
                "یک بحث رادیویی بین دو مهمان می‌شنوید، دو بار. هر نظر مال کیست؟",
                "You hear a radio discussion between two guests, twice. Who says what?",
                "Sie hören eine Radiodiskussion mit zwei Gästen, zweimal. Wer sagt was?",
            ),
            "tracks": [("Teil 4", f"{AUDIO}/teil4.m4a", 2, 25, list(range(23, 31)))],
            "items": [
                (23, "Hausaufgaben helfen beim Wiederholen.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "a", None),
                (24, "Kinder brauchen nachmittags mehr freie Zeit.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "b", None),
                (25, "Eltern können bei Hausaufgaben zu viel helfen.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "c", None),
                (26, "Ohne Übung zu Hause vergisst man den Stoff schnell.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "a", None),
                (27, "Ganztagsschulen wären die bessere Lösung.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "b", None),
                (28, "Die Menge der Aufgaben ist wichtiger als das Ob.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "c", None),
                (29, "Lehrkräfte müssten sich besser absprechen.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "c", None),
                (30, "Ein völliges Verbot wäre falsch.",
                 [("a", "Frau Klein"), ("b", "Herr Adler"), ("c", "beide")], "a", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 60,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "سه تکلیف، ۶۰ دقیقه: یک ایمیل خصوصی، یک نظر در انجمن و یک ایمیل رسمی.",
        "Three tasks, 60 minutes: a private email, a forum comment and a formal email.",
        "Drei Aufgaben, 60 Minuten: eine private E-Mail, ein Forumsbeitrag und eine formelle "
        "E-Mail.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 20,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "به دوستتان ایمیل بنویسید، حدود ۸۰ کلمه. هر سه نکته را پوشش دهید.",
                "Write an email to a friend, about 80 words, covering all three points.",
                "Schreiben Sie eine E-Mail an eine Freundin, etwa 80 Wörter, zu allen drei Punkten.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Ihre Freundin Mira zieht in eine andere Stadt. Sie können bei ihrem Umzug am "
                "Samstag nicht helfen.",
            "blocks": [
                ("bullet", "", "", "Erklären Sie, warum Sie nicht kommen können."),
                ("bullet", "", "", "Machen Sie einen anderen Vorschlag, wie Sie helfen können."),
                ("bullet", "", "", "Fragen Sie nach der neuen Wohnung."),
            ],
            "items": [(1, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 80,
        },
        {
            "type": "writing",
            "minutes": 25,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "در یک انجمن اینترنتی نظر بنویسید، حدود ۸۰ کلمه. نظر خود را با دلیل بیان کنید.",
                "Write a forum comment of about 80 words. Give your opinion with reasons.",
                "Schreiben Sie einen Forumsbeitrag von etwa 80 Wörtern. Begründen Sie Ihre "
                "Meinung.",
            ),
            "stimulus_title": "Forum: Sollen Supermärkte sonntags öffnen?",
            "stimulus_intro":
                "In einem Online-Forum wird diskutiert, ob Supermärkte auch am Sonntag öffnen "
                "sollen. Schreiben Sie Ihre Meinung.",
            "blocks": [
                ("bullet", "", "", "Sagen Sie, was Sie davon halten."),
                ("bullet", "", "", "Nennen Sie mindestens zwei Gründe."),
                ("bullet", "", "", "Gehen Sie auf ein Gegenargument ein."),
            ],
            "items": [(2, "Schreiben Sie den Forumsbeitrag.", None, "", None)],
            "min_words": 80,
        },
        {
            "type": "writing",
            "minutes": 15,
            "title": ("شرایبن ۳", "Schreiben 3", "Schreiben 3"),
            "instructions": (
                "یک ایمیل رسمی بنویسید، حدود ۴۰ کلمه. لحن رسمی را رعایت کنید.",
                "Write a formal email of about 40 words. Keep the register formal.",
                "Schreiben Sie eine formelle E-Mail von etwa 40 Wörtern. Achten Sie auf den Ton.",
            ),
            "stimulus_title": "Situation",
            "stimulus_intro":
                "Sie haben einen Termin bei Frau Dr. Sanders am Donnerstag um 15 Uhr und können "
                "nicht kommen.",
            "blocks": [
                ("bullet", "", "", "Entschuldigen Sie sich."),
                ("bullet", "", "", "Sagen Sie ab und schlagen Sie einen neuen Termin vor."),
            ],
            "items": [(3, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 40,
        },
    ],
}
