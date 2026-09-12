"""Goethe-/ÖSD-Zertifikat B1 — the official task shapes, in-house material.

Structure taken from the published Modellsatz Erwachsene (2. Auflage, 2015):

    Lesen   65 min · 5 Teile · 30 items
            Teil 1  items 1–6    Richtig/Falsch on a blog post            10 min
            Teil 2  items 7–12   three options, two press texts (3 + 3)    20 min
            Teil 3  items 13–19  situations → adverts a–j, one has none (0) 10 min
            Teil 4  items 20–26  reader comments: for a ban? Ja/Nein        15 min
            Teil 5  items 27–30  three options on a set of house rules      10 min
    Hören   40 min · 4 Teile · 30 items
            Teil 1  items 1–10   five short texts, each heard twice,
                                 one Richtig/Falsch and one a/b/c per text
            Teil 2  items 11–15  a guided tour, heard once, a/b/c
            Teil 3  items 16–22  a conversation, heard once, Richtig/Falsch
            Teil 4  items 23–30  a radio discussion, heard twice:
                                 who says it — the moderator or one of two guests
    Schreiben 60 min · 3 Aufgaben
            1  an email to a friend, ~80 words, three points           20 min
            2  a reply in an online discussion, ~80 words              25 min
            3  a polite email to a teacher, ~40 words                  15 min

Every Teil carries its worked example (Beispiel 0), as the paper does. The
wording is Lexora's own; only the format follows the model set.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/b1/hoeren"

ABC = "abc"
YES_NO = [("ja", "Ja"), ("nein", "Nein")]
SPEAKERS = [("a", "Moderator"), ("b", "Frau Klein"), ("c", "Herr Adler")]


def abc(*texts):
    """Three written options, keyed a/b/c."""
    return [(key, text) for key, text in zip(ABC, texts)]


LESEN = {
    "skill": "lesen",
    "duration": 65,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "پنج بخش، ۳۰ سؤال، ۶۵ دقیقه. از هر بخش می‌توانید شروع کنید؛ هر سؤال فقط یک جواب درست دارد.",
        "Five parts, 30 items, 65 minutes. You may start with any part; every item has one answer.",
        "Das Modul Lesen hat fünf Teile. Sie können mit jeder Aufgabe beginnen. Für jede "
        "Aufgabe gibt es nur eine richtige Lösung.",
    ),
    "parts": [
        # ---------------------------------------------------------- Teil 1
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "متن و سؤال‌های ۱ تا ۶ را بخوانید. آیا جمله‌ها Richtig هستند یا Falsch؟",
                "Read the text and items 1–6. Are the statements Richtig or Falsch?",
                "Lesen Sie den Text und die Aufgaben 1 bis 6 dazu. "
                "Wählen Sie: Sind die Aussagen Richtig oder Falsch?",
            ),
            "stimulus_title": "Ohne-Auto-Blog.de",
            "stimulus_subtitle": "Mein Alltag, meine Wege, meine Erfahrungen …",
            "blocks": [
                ("paragraph", "", "Samstag, den 14. März",
                 "Vor genau einem Jahr habe ich mein Auto verkauft. Nicht aus Überzeugung, "
                 "sondern weil die Reparatur teurer gewesen wäre, als der Wagen noch wert war. "
                 "Ehrlich gesagt dachte ich, dass ich das höchstens zwei Monate durchhalte.\n\n"
                 "Die ersten Wochen waren tatsächlich anstrengend. Ich hatte unterschätzt, wie "
                 "viel Zeit man mit Warten verbringt, wenn man auf Busse angewiesen ist. Zweimal "
                 "bin ich zu spät zur Arbeit gekommen, einmal musste ich sogar einen "
                 "Zahnarzttermin absagen. Meine Kollegin hat mir dann geraten, alles eine "
                 "Viertelstunde früher zu planen. Das klingt banal, hat aber fast alle Probleme "
                 "gelöst.\n\n"
                 "Was mich wirklich überrascht hat, ist das Geld. Mit ein paar Ersparnissen hatte "
                 "ich gerechnet, aber nicht mit so vielen: Versicherung, Steuer, Werkstatt, "
                 "Benzin und Parken zusammen kosteten deutlich mehr als meine Monatskarte und "
                 "die paar Mietwagen im Jahr. Am Ende bleiben mir gut zweitausend Euro übrig.\n\n"
                 "Trotzdem würde ich nicht sagen, dass ein Leben ohne Auto für jeden passt. Wer "
                 "auf dem Land wohnt oder kleine Kinder zu drei verschiedenen Orten bringen "
                 "muss, hat es deutlich schwerer als ich in der Stadt. Und wenn ich im Winter im "
                 "Regen auf den Bus warte, denke ich schon manchmal an die Heizung im Auto. "
                 "Kaufen werde ich mir aber keins mehr.\n\n"
                 "Bis bald\neuer Jonas"),
            ],
            "example_prompt": "Jonas hat sein Auto vor einem Jahr verkauft. → Richtig",
            "example_answer": "richtig",
            "items": [
                (1, "Jonas hat sein Auto aus Umweltgründen verkauft.", TRUE_FALSE, "falsch",
                 ("«Nicht aus Überzeugung, sondern weil die Reparatur teurer gewesen wäre».",
                  "He sold it because the repair would have cost more than the car was worth.",
                  "„Nicht aus Überzeugung, sondern weil die Reparatur teurer gewesen wäre.“")),
                (2, "Am Anfang kam Jonas manchmal zu spät.", TRUE_FALSE, "richtig",
                 ("دو بار دیر به سر کار رسیده.", "He was late for work twice.",
                  "Er kam zweimal zu spät zur Arbeit.")),
                (3, "Der Rat seiner Kollegin hat kaum geholfen.", TRUE_FALSE, "falsch",
                 ("«hat aber fast alle Probleme gelöst».", "It solved almost all the problems.",
                  "„Hat aber fast alle Probleme gelöst.“")),
                (4, "Jonas spart mehr Geld, als er gedacht hatte.", TRUE_FALSE, "richtig",
                 ("«nicht mit so vielen» — بیشتر از انتظارش.",
                  "More than he had expected.", "Mehr, als er erwartet hatte.")),
                (5, "Jonas findet, dass jeder ohne Auto leben kann.", TRUE_FALSE, "falsch",
                 ("می‌گوید برای همه مناسب نیست.", "He says it does not suit everyone.",
                  "Er sagt, es passe nicht für jeden.")),
                (6, "Jonas möchte sich bald wieder ein Auto kaufen.", TRUE_FALSE, "falsch",
                 ("«Kaufen werde ich mir aber keins mehr».", "\"I won't buy one again.\"",
                  "„Kaufen werde ich mir aber keins mehr.“")),
            ],
        },
        # ---------------------------------------------------------- Teil 2
        {
            "type": "mcq",
            "minutes": 20,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "دو متن مطبوعاتی و سؤال‌های ۷ تا ۱۲ را بخوانید. برای هر سؤال a، b یا c را "
                "انتخاب کنید.",
                "Read the two press texts and items 7–12. Choose a, b or c for each item.",
                "Lesen Sie die Texte aus der Presse und die Aufgaben 7 bis 12 dazu. "
                "Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
            ),
            "stimulus_title": "Zwei Texte aus der Presse",
            "blocks": [
                ("paragraph", "Text 1 (Aufgaben 7–9)", "Warum wir die Zeit falsch schätzen",
                 "Wenn Menschen sagen sollen, wie lange eine Aufgabe dauert, liegen sie fast "
                 "immer daneben – und zwar zu optimistisch. Forscher nennen das den "
                 "„Planungsfehler“. Studierende, die ihre Abschlussarbeit planen, brauchen im "
                 "Durchschnitt die Hälfte länger als gedacht, selbst wenn sie schon einmal eine "
                 "solche Arbeit geschrieben haben.\n\n"
                 "Interessant ist: Dieselben Personen schätzen die Dauer bei anderen ziemlich "
                 "genau. Das Problem entsteht also nicht aus Unwissen, sondern daraus, dass man "
                 "selbst beteiligt ist. Wer plant, denkt an den idealen Ablauf und vergisst die "
                 "Störungen, die er bei Fremden ganz selbstverständlich einrechnet.\n\n"
                 "Eine einfache Methode hilft erstaunlich gut: die eigene Schätzung "
                 "aufschreiben und mit dem letzten ähnlichen Projekt vergleichen."),
                ("paragraph", "Text 2 (Aufgaben 10–12)", "Der lange Weg ins Handwerk",
                 "Viele Betriebe suchen dringend Auszubildende, gleichzeitig bleiben viele "
                 "Jugendliche unentschlossen. Eine Untersuchung aus Nordrhein-Westfalen zeigt, "
                 "dass es weniger am Gehalt liegt als am Bild des Berufs: Das Handwerk gilt "
                 "vielen als körperlich hart und wenig zukunftssicher.\n\n"
                 "Dabei verdienen Gesellen in einigen Berufen nach wenigen Jahren mehr als "
                 "Berufsanfänger mit Studium, und über neunzig Prozent der Auszubildenden werden "
                 "nach der Lehre übernommen.\n\n"
                 "Betriebe, die Schülerinnen und Schülern früh ein Praktikum anbieten, finden "
                 "deutlich leichter Nachwuchs – nicht weil sie besser bezahlen, sondern weil ein "
                 "Tag in der Werkstatt mehr erklärt als jede Broschüre."),
            ],
            "example_prompt": "0  Der erste Text handelt davon, … → b) wie Menschen Zeit einschätzen.",
            "example_answer": "b",
            "items": [
                (7, "Der „Planungsfehler“ bedeutet, dass Menschen …",
                 abc("die Dauer zu kurz einschätzen.", "Aufgaben gar nicht planen.",
                     "zu viel Zeit einplanen."), "a", None),
                (8, "Bei anderen Personen schätzen dieselben Menschen die Dauer …",
                 abc("noch schlechter.", "ziemlich genau.", "gar nicht."), "b", None),
                (9, "Als Hilfe empfiehlt der Text, …",
                 abc("mehr Erfahrung zu sammeln.",
                     "die Schätzung mit früheren Projekten zu vergleichen.",
                     "Aufgaben an andere abzugeben."), "b", None),
                (10, "Viele Jugendliche entscheiden sich gegen das Handwerk, weil …",
                 abc("die Bezahlung schlecht ist.", "sie ein falsches Bild vom Beruf haben.",
                     "es zu wenige Stellen gibt."), "b", None),
                (11, "Nach der Ausbildung …",
                 abc("werden fast alle Azubis übernommen.", "verdient man weniger als mit Studium.",
                     "muss man sich neu bewerben."), "a", None),
                (12, "Praktika helfen den Betrieben, weil sie …",
                 abc("billiger sind als Werbung.", "den Beruf direkt zeigen.",
                     "gesetzlich vorgeschrieben sind."), "b", None),
            ],
        },
        # ---------------------------------------------------------- Teil 3
        {
            "type": "match_heading",
            "minutes": 10,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "موقعیت‌های ۱۳ تا ۱۹ و آگهی‌های a تا j را بخوانید. کدام آگهی به کدام موقعیت "
                "می‌خورد؟ هر آگهی فقط یک بار. آگهی مثال دیگر قابل استفاده نیست. برای یک "
                "موقعیت آگهی مناسبی وجود ندارد؛ آن‌جا 0 را انتخاب کنید.",
                "Read situations 13–19 and adverts a–j. Which advert fits which situation? "
                "Each advert once; the example's advert is used up. One situation has no "
                "matching advert — choose 0 for it.",
                "Lesen Sie die Situationen 13 bis 19 und die Anzeigen a bis j. Welche Anzeige "
                "passt zu welcher Situation? Sie können jede Anzeige nur einmal verwenden. Die "
                "Anzeige aus dem Beispiel können Sie nicht mehr verwenden. Für eine Situation "
                "gibt es keine passende Anzeige. In diesem Fall wählen Sie 0.",
            ),
            "stimulus_title": "Anzeigen",
            "stimulus_intro":
                "Sie sind neu in der Stadt. Einige Bekannte aus Ihrem Deutschkurs suchen "
                "Hilfe und Angebote für den Alltag.",
            "blocks": [
                ("heading", "a", "Möbelmarkt Lehmann",
                 "Lieferung und Aufbau, auch abends nach 18 Uhr. Wir bringen Ihre Möbel bis "
                 "in die Wohnung."),
                ("heading", "b", "Sprachtandem Uni Jena",
                 "Kostenlos Deutsch sprechen – Sie bringen Ihre Sprache mit. Wöchentliche "
                 "Treffen, keine Anmeldung nötig."),
                ("heading", "c", "Hundebetreuung Pfote",
                 "Stundenweise oder über Nacht, auch für mehrere Wochen. Erfahrene Betreuung "
                 "mit großem Garten."),
                ("heading", "d", "Fahrschule Ost",
                 "Intensivkurs in zwei Wochen: Theorie und Praxis am Stück, Prüfung am Ende "
                 "des Kurses."),
                ("heading", "e", "Nähwerkstatt",
                 "Reparaturen und Änderungen aller Art, fertig in 48 Stunden. Hosen kürzen "
                 "ab 12 Euro."),
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
                 "Bringen Sie Ihr kaputtes Gerät mit – wir reparieren gemeinsam, statt "
                 "wegzuwerfen. Jeden Samstag."),
                ("heading", "j", "Bürogemeinschaft Mitte",
                 "Schreibtisch tageweise mieten, mit Internet und Küche. Keine "
                 "Mindestlaufzeit."),
            ],
            "pool": [
                ("a", "a"), ("b", "b"), ("c", "c"), ("d", "d"), ("e", "e"),
                ("f", "f"), ("g", "g"), ("h", "h"), ("i", "i"), ("j", "j"),
                ("0", "0"),
            ],
            "example_prompt": "0  Karim möchte möglichst schnell seinen Führerschein machen. → d",
            "example_answer": "d",
            "items": [
                (13, "Olga ist der Wasserkocher kaputtgegangen, wegwerfen möchte sie ihn "
                     "aber nicht.", None, "i", None),
                (14, "Ahmed möchte Deutsch sprechen üben, ohne dafür zu bezahlen.", None, "b",
                 None),
                (15, "Lena zieht am Samstag um und braucht für einen Nachmittag Hilfe.", None,
                 "g", None),
                (16, "Tomás' neue Hose ist zu lang und soll bis Freitag fertig sein.", None,
                 "e", None),
                (17, "Mei arbeitet selbstständig und braucht nur an zwei Tagen pro Woche "
                     "einen Arbeitsplatz.", None, "j", None),
                (18, "Sandra sucht einen Zahnarzt, der auch am Samstag Sprechstunde hat.",
                 None, "0", ("هیچ آگهی‌ای دربارهٔ دندان‌پزشک نیست.",
                             "No advert offers a dentist.",
                             "Keine Anzeige bietet einen Zahnarzt an.")),
                (19, "Pavel fährt drei Wochen in Urlaub und braucht jemanden für seinen Hund.",
                 None, "c", None),
            ],
        },
        # ---------------------------------------------------------- Teil 4
        {
            "type": "mcq",
            "minutes": 15,
            "title": ("لزن ۴", "Lesen 4", "Lesen 4"),
            "instructions": (
                "نظرهای ۲۰ تا ۲۶ را بخوانید. آیا نویسنده موافق ممنوعیت است؟ Ja یا Nein.",
                "Read comments 20–26. Is the person in favour of a ban? Ja or Nein.",
                "Lesen Sie die Texte 20 bis 26. Wählen Sie: Ist die Person für ein Verbot?",
            ),
            "stimulus_title": "Sollen Handys an Schulen verboten werden?",
            "stimulus_intro":
                "In einer Zeitschrift lesen Sie Kommentare zu einem Artikel über ein "
                "Handyverbot an Schulen.",
            "blocks": [
                ("statement", "Beispiel", "Lothar, 58, Kassel",
                 "Seit an der Schule meines Enkels Handys im Unterricht verboten sind, redet er "
                 "wieder mit seinen Freunden in der Pause. Für mich ist die Sache klar: Die "
                 "Geräte gehören morgens in den Schrank."),
                ("statement", "20", "Bilal, 34, Hannover",
                 "Ich unterrichte seit acht Jahren. In der Pause reden die Kinder nicht mehr "
                 "miteinander, sie sitzen nebeneinander und schauen auf ihre Bildschirme. Seit "
                 "wir die Geräte morgens einsammeln, ist der Schulhof wieder laut – im besten "
                 "Sinne."),
                ("statement", "21", "Regina, 41, Graz",
                 "Ein Verbot löst gar nichts. Die Kinder lernen dann nicht, verantwortlich mit "
                 "dem Gerät umzugehen, sondern nur, es zu verstecken. Besser wäre "
                 "Medienunterricht ab der fünften Klasse."),
                ("statement", "22", "Tarek, 19, Zürich",
                 "Ich habe letztes Jahr Abitur gemacht. Ohne Handy hätte ich die Hälfte der "
                 "Hausaufgaben nicht geschafft – Termine, Gruppenchats, Fotos von der Tafel. "
                 "Wer das verbietet, macht die Schule schwieriger, nicht besser."),
                ("statement", "23", "Heike, 52, Rostock",
                 "Meine Tochter war nach jedem Schultag völlig erschöpft. Seit dem Verbot an "
                 "ihrer Schule schläft sie besser und ihre Noten sind gestiegen. Ich hätte nie "
                 "gedacht, dass das so viel ausmacht."),
                ("statement", "24", "Milan, 28, Wien",
                 "Im Notfall muss ein Kind seine Eltern erreichen können. Dieser Punkt fehlt in "
                 "der Diskussion fast immer, und für mich ist er wichtiger als ein bisschen "
                 "Ablenkung im Unterricht."),
                ("statement", "25", "Anke, 45, Bremen",
                 "Wir haben es an unserer Schule ein Jahr lang ausprobiert: weniger Streit, "
                 "weniger Mobbing, ruhigere Klassen. Ich war vorher skeptisch und bin es heute "
                 "nicht mehr."),
                ("statement", "26", "Sophie, 23, Basel",
                 "Statt zu verbieten, sollten Schulen das Handy sinnvoll im Unterricht nutzen – "
                 "zum Recherchieren, für Wörterbücher, für Umfragen. Verbote machen die Geräte "
                 "nur noch interessanter."),
            ],
            "example_prompt": "Beispiel: Lothar → Ja",
            "example_answer": "ja",
            "items": [
                (20, "Bilal", YES_NO, "ja", None),
                (21, "Regina", YES_NO, "nein", None),
                (22, "Tarek", YES_NO, "nein", None),
                (23, "Heike", YES_NO, "ja", None),
                (24, "Milan", YES_NO, "nein", None),
                (25, "Anke", YES_NO, "ja", None),
                (26, "Sophie", YES_NO, "nein", None),
            ],
        },
        # ---------------------------------------------------------- Teil 5
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("لزن ۵", "Lesen 5", "Lesen 5"),
            "instructions": (
                "سؤال‌های ۲۷ تا ۳۰ و متن را بخوانید. برای هر سؤال a، b یا c را انتخاب کنید.",
                "Read items 27–30 and the text. Choose a, b or c for each item.",
                "Lesen Sie die Aufgaben 27 bis 30 und den Text dazu. Wählen Sie bei jeder "
                "Aufgabe die richtige Lösung a, b oder c.",
            ),
            "stimulus_title": "HAUSORDNUNG",
            "stimulus_intro":
                "Sie informieren sich über die Hausordnung der Volkshochschule Leipzig, in der "
                "Sie einen Kurs gebucht haben.",
            "blocks": [
                ("section", "", "Unterrichtszeiten",
                 "Die vereinbarten Kurszeiten sind verbindlich. Ist die Kursleitung fünfzehn "
                 "Minuten nach Beginn nicht da, informiert die Kurssprecherin oder der "
                 "Kurssprecher das Büro."),
                ("section", "", "Räume",
                 "Alle Räume sind sauber und ordentlich zu verlassen. Nach Kursende dürfen sich "
                 "Teilnehmende nicht mehr in den Kursräumen aufhalten. Plakate und Aushänge "
                 "sind nur an den Pinnwänden im Flur erlaubt."),
                ("section", "", "Essen und Trinken",
                 "In den Kursräumen ist nur Wasser erlaubt. Speisen und andere Getränke bitte "
                 "in der Cafeteria im Erdgeschoss. Für Veranstaltungen kann die Leitung "
                 "Ausnahmen genehmigen."),
                ("section", "", "Schließfächer",
                 "Teilnehmende und Mitarbeitende können kostenlos ein Schließfach nutzen. Den "
                 "Schlüssel erhalten Sie gegen Vorlage des Kursausweises im Büro. Für einen "
                 "verlorenen Schlüssel berechnen wir 30 Euro."),
                ("section", "", "Fahrräder und Parken",
                 "Für Autos gibt es auf dem Gelände keine Parkplätze. Fahrräder bitte im "
                 "Fahrradkeller abstellen und abschließen."),
            ],
            "items": [
                (27, "Fahrräder …",
                 abc("darf man nicht mitbringen.", "kann man auf den Hof stellen.",
                     "gehören in einen besonderen Raum."), "c", None),
                (28, "In den Kursräumen …",
                 abc("darf man keine Plakate aufhängen.", "muss man selbst die Tafel putzen.",
                     "kann man nach dem Kurs weiterlernen."), "a", None),
                (29, "Für ein Schließfach muss man …",
                 abc("30 Euro Pfand bezahlen.", "den Kursausweis zeigen.",
                     "einen Antrag schreiben."), "b", None),
                (30, "Kaffee in den Kursräumen …",
                 abc("ist ohne Ausnahme verboten.", "kann die Leitung für Veranstaltungen "
                     "erlauben.", "ist erlaubt, wenn man ihn in der Cafeteria kauft."), "b",
                 None),
            ],
        },
    ],
}

HOEREN = {
    "skill": "hoeren",
    "duration": 40,
    "title": ("هؤرن — درک شنیداری", "Hören — Listening", "Hören"),
    "intro": (
        "چهار بخش، ۳۰ سؤال، ۴۰ دقیقه. اول سؤال‌ها را بخوانید، بعد متن را بشنوید.",
        "Four parts, 30 items, 40 minutes. Read the items first, then listen.",
        "Das Modul Hören besteht aus vier Teilen. Lesen Sie jeweils zuerst die Aufgaben "
        "und hören Sie dann den Text dazu.",
    ),
    "parts": [
        # ---------------------------------------------------------- Teil 1
        {
            "type": "listening_mixed",
            "minutes": 10,
            "title": ("هؤرن ۱", "Hören 1", "Hören 1"),
            "instructions": (
                "پنج متن کوتاه می‌شنوید، هرکدام را دو بار. برای هر متن دو سؤال هست.",
                "You hear five short texts, each twice. Each text has two items.",
                "Sie hören nun fünf kurze Texte. Sie hören jeden Text zweimal. Zu jedem Text "
                "lösen Sie zwei Aufgaben. Wählen Sie bei jeder Aufgabe die richtige Lösung.",
            ),
            # one track per text, so each can be replayed on its own
            "tracks": [
                ("Text 1", f"{AUDIO}/teil1-1.m4a", 2, 10, [1, 2]),
                ("Text 2", f"{AUDIO}/teil1-2.m4a", 2, 10, [3, 4]),
                ("Text 3", f"{AUDIO}/teil1-3.m4a", 2, 10, [5, 6]),
                ("Text 4", f"{AUDIO}/teil1-4.m4a", 2, 10, [7, 8]),
                ("Text 5", f"{AUDIO}/teil1-5.m4a", 2, 10, [9, 10]),
            ],
            "example_prompt": "01  Die Anruferin lädt zu einer Grillparty ein. → Richtig",
            "example_answer": "richtig",
            "items": [
                (1, "Der Anruf kommt von der Autowerkstatt.", TRUE_FALSE, "richtig", None),
                (2, "Herr Baum kann sein Auto …",
                 abc("heute abholen.", "morgen abholen.", "übermorgen abholen."), "b", None),
                (3, "Das Sommerfest findet im Park statt.", TRUE_FALSE, "falsch", None),
                (4, "Das Fest ist jetzt …",
                 abc("in der Turnhalle.", "im Rathaus.", "in der Aula."), "c", None),
                (5, "Frau Ritter sucht eine Wohnung.", TRUE_FALSE, "falsch", None),
                (6, "Frau Ritter ruft an wegen …",
                 abc("eines Termins.", "einer Rechnung.", "eines Praktikums."), "c", None),
                (7, "Der Fotokurs ist schon voll.", TRUE_FALSE, "richtig", None),
                (8, "Man kann sich …",
                 abc("auf eine Warteliste setzen lassen.", "für den nächsten Monat anmelden.",
                     "das Geld zurückholen."), "a", None),
                (9, "Die Ringstraße ist wegen einer Baustelle gesperrt.", TRUE_FALSE, "richtig",
                 None),
                (10, "Die Sperrung dauert …",
                 abc("bis Freitag.", "zwei Wochen.", "einen Monat."), "b", None),
            ],
        },
        # ---------------------------------------------------------- Teil 2
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "یک متن را فقط یک بار می‌شنوید و به پنج سؤال جواب می‌دهید. ۶۰ ثانیه وقت دارید "
                "سؤال‌ها را بخوانید.",
                "You hear one text once and answer five items. You have 60 seconds to read them.",
                "Sie hören nun einen Text. Sie hören den Text einmal. Dazu lösen Sie fünf "
                "Aufgaben. Lesen Sie jetzt die Aufgaben 11 bis 15. Dazu haben Sie 60 Sekunden "
                "Zeit.",
            ),
            "stimulus_intro": "Sie nehmen an einer Führung durch die Alte Tuchfabrik teil.",
            "tracks": [("Führung", f"{AUDIO}/teil2.m4a", 1, 60, [11, 12, 13, 14, 15])],
            "items": [
                (11, "Das Gebäude war früher …",
                 abc("eine Fabrik.", "eine Schule.", "ein Krankenhaus."), "a", None),
                (12, "Die Renovierung dauerte …",
                 abc("zwei Jahre.", "vier Jahre.", "sieben Jahre."), "b", None),
                (13, "Heute gibt es in dem Haus …",
                 abc("Wohnungen.", "Büros und Ateliers.", "ein Museum."), "b", None),
                (14, "Die Führung dauert insgesamt …",
                 abc("45 Minuten.", "eine Stunde.", "90 Minuten."), "c", None),
                (15, "Fotografieren ist …",
                 abc("überall erlaubt.", "nur im Innenhof erlaubt.", "ganz verboten."), "b",
                 None),
            ],
        },
        # ---------------------------------------------------------- Teil 3
        {
            "type": "listening_mixed",
            "minutes": 10,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "یک گفتگو را فقط یک بار می‌شنوید و به هفت سؤال جواب می‌دهید: Richtig یا Falsch.",
                "You hear a conversation once and answer seven items: Richtig or Falsch.",
                "Sie hören nun ein Gespräch. Sie hören das Gespräch einmal. Dazu lösen Sie "
                "sieben Aufgaben. Wählen Sie: Sind die Aussagen Richtig oder Falsch? Lesen Sie "
                "jetzt die Aufgaben 16 bis 22. Dazu haben Sie 60 Sekunden Zeit.",
            ),
            "stimulus_intro":
                "Sie sitzen in der Straßenbahn und hören, wie sich eine Frau und ein Mann "
                "unterhalten.",
            "tracks": [("Gespräch", f"{AUDIO}/teil3.m4a", 1, 60,
                        [16, 17, 18, 19, 20, 21, 22])],
            "items": [
                (16, "Lena und Markus kennen sich von der Arbeit.", TRUE_FALSE, "falsch", None),
                (17, "Lena hat seit Kurzem eine neue Stelle.", TRUE_FALSE, "richtig", None),
                (18, "Lena braucht jetzt weniger Zeit für den Weg zur Arbeit.", TRUE_FALSE,
                 "richtig", None),
                (19, "Lena verdient weniger als früher.", TRUE_FALSE, "falsch", None),
                (20, "Lena findet ihren Chef unfreundlich.", TRUE_FALSE, "falsch", None),
                (21, "Lena möchte neben der Arbeit studieren.", TRUE_FALSE, "richtig", None),
                (22, "Lena und Markus treffen sich nächste Woche.", TRUE_FALSE, "richtig", None),
            ],
        },
        # ---------------------------------------------------------- Teil 4
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۴", "Hören 4", "Hören 4"),
            "instructions": (
                "یک بحث رادیویی را دو بار می‌شنوید. هر جمله را چه کسی می‌گوید؟",
                "You hear a radio discussion twice. Who says what?",
                "Sie hören nun eine Diskussion. Sie hören die Diskussion zweimal. Dazu lösen "
                "Sie acht Aufgaben. Ordnen Sie die Aussagen zu: Wer sagt was? Lesen Sie jetzt "
                "die Aussagen 23 bis 30. Dazu haben Sie 60 Sekunden Zeit.",
            ),
            "stimulus_intro":
                "Der Moderator der Radiosendung „Thema am Abend“ diskutiert mit der Lehrerin "
                "Sabine Klein und dem Vater Jonas Adler über die Frage: „Brauchen Kinder "
                "Hausaufgaben?“",
            "tracks": [("Diskussion", f"{AUDIO}/teil4.m4a", 2, 60,
                        [23, 24, 25, 26, 27, 28, 29, 30])],
            # one shared list of speakers, so their names are entered once
            "pool": SPEAKERS,
            "example_prompt": "0  Das Thema betrifft fast alle Familien. → a) Moderator",
            "example_answer": "a",
            "items": [
                (23, "Hausaufgaben helfen den Kindern, den Stoff zu wiederholen.", None, "b",
                 None),
                (24, "Kinder brauchen am Nachmittag mehr freie Zeit.", None, "c", None),
                (25, "Viele Eltern helfen zu viel bei den Hausaufgaben.", None, "b", None),
                (26, "In manchen Ländern gibt es kaum Hausaufgaben.", None, "a", None),
                (27, "Ganztagsschulen wären die bessere Lösung.", None, "c", None),
                (28, "Die Lehrkräfte sollten sich besser absprechen.", None, "c", None),
                (29, "Die Hörer können in der Sendung anrufen.", None, "a", None),
                (30, "Hausaufgaben ganz abzuschaffen, wäre falsch.", None, "b", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 60,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "سه تکلیف، ۶۰ دقیقه: در تکلیف ۱ و ۳ ایمیل می‌نویسید، در تکلیف ۲ نظرتان را در یک بحث.",
        "Three tasks, 60 minutes: emails in tasks 1 and 3, an opinion in task 2.",
        "Das Modul Schreiben besteht aus drei Teilen. In den Aufgaben 1 und 3 schreiben Sie "
        "E-Mails. In Aufgabe 2 schreiben Sie einen Diskussionsbeitrag. Sie können mit jeder "
        "Aufgabe beginnen.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 20,
            "title": ("شرایبن ۱", "Schreiben 1", "Aufgabe 1"),
            "instructions": (
                "یک ایمیل حدود ۸۰ کلمه بنویسید و به هر سه نکته بپردازید. به ساختار متن "
                "(سلام، مقدمه، ترتیب نکته‌ها، پایان) توجه کنید.",
                "Write an email of about 80 words covering all three points. Mind the "
                "structure: greeting, opening, the points in order, closing.",
                "Schreiben Sie eine E-Mail (circa 80 Wörter). Schreiben Sie etwas zu allen drei "
                "Punkten. Achten Sie auf den Textaufbau (Anrede, Einleitung, Reihenfolge der "
                "Inhaltspunkte, Schluss).",
            ),
            "stimulus_title": "Aufgabe 1",
            "stimulus_intro":
                "Sie sind vor zwei Wochen in eine neue Wohnung umgezogen. Ihre Freundin Mira "
                "konnte beim Umzug nicht helfen, weil sie auf Dienstreise war.",
            "blocks": [
                ("bullet", "", "", "Beschreiben Sie: Wie ist die neue Wohnung?"),
                ("bullet", "", "", "Begründen Sie: Was gefällt Ihnen an der neuen Umgebung "
                                   "besonders und warum?"),
                ("bullet", "", "", "Machen Sie einen Vorschlag für einen Besuch."),
            ],
            "items": [(1, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 80,
        },
        {
            "type": "writing",
            "minutes": 25,
            "title": ("شرایبن ۲", "Schreiben 2", "Aufgabe 2"),
            "instructions": (
                "نظر خود را دربارهٔ موضوع بنویسید، حدود ۸۰ کلمه.",
                "Write your opinion on the topic, about 80 words.",
                "Schreiben Sie nun Ihre Meinung zum Thema (circa 80 Wörter).",
            ),
            "stimulus_title": "www.diskussion-heute.de · Gästebuch",
            "stimulus_intro":
                "Sie haben im Fernsehen eine Diskussionssendung zum Thema „Einkaufen im "
                "Internet oder im Geschäft?“ gesehen. Im Online-Gästebuch der Sendung finden "
                "Sie folgende Meinung:",
            "blocks": [
                ("statement", "", "Petra · 03.11. · 18:42 Uhr",
                 "Ich kaufe fast alles nur noch online. Es ist billiger, ich spare Zeit und "
                 "habe mehr Auswahl. Die Geschäfte in der Innenstadt brauche ich eigentlich "
                 "gar nicht mehr."),
            ],
            "items": [(2, "Schreiben Sie Ihren Diskussionsbeitrag.", None, "", None)],
            "min_words": 80,
        },
        {
            "type": "writing",
            "minutes": 15,
            "title": ("شرایبن ۳", "Schreiben 3", "Aufgabe 3"),
            "instructions": (
                "یک ایمیل حدود ۴۰ کلمه بنویسید. سلام و خداحافظی را فراموش نکنید.",
                "Write an email of about 40 words. Don't forget the greeting and closing.",
                "Schreiben Sie eine E-Mail (circa 40 Wörter). Vergessen Sie nicht die Anrede "
                "und den Gruß am Schluss.",
            ),
            "stimulus_title": "Aufgabe 3",
            "stimulus_intro":
                "Ihr Kursleiter, Herr Berger, hat Sie zu einem Gespräch über Ihre Prüfung "
                "eingeladen. Zu dem Termin können Sie aber nicht kommen. Schreiben Sie an "
                "Herrn Berger. Entschuldigen Sie sich höflich und berichten Sie, warum Sie "
                "nicht kommen können.",
            "items": [(3, "Schreiben Sie die E-Mail.", None, "", None)],
            "min_words": 40,
        },
    ],
}
