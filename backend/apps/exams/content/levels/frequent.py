"""High-frequency sets for B2 and C1.

These are not full sittings. They collect the task types that cost candidates
the most marks, so a learner can drill one shape repeatedly after a full
simulator has shown where the gap is.
"""

from ._build import TRUE_FALSE

AUDIO_B2 = "/media/exams/frequent-b2/hoeren"
AUDIO_C1 = "/media/exams/frequent-c1/hoeren"

# ------------------------------------------------------------------- B2 ---

B2_LESEN = {
    "skill": "lesen",
    "duration": 35,
    "title": ("لزن — پرتکرار", "Lesen — high frequency", "Lesen — häufige Aufgaben"),
    "intro": (
        "دو تسکی که در B2 بیشترین نمره را می‌برند: تطبیق عنوان با پاراگراف و پر کردن جای خالی.",
        "The two B2 tasks that cost the most marks: heading-to-paragraph and gap filling.",
        "Die zwei B2-Aufgaben mit den meisten Punktverlusten: Überschrift-zu-Absatz und Lücken.",
    ),
    "parts": [
        {
            "type": "match_heading",
            "minutes": 18,
            "title": ("تطبیق عنوان", "Heading matching", "Überschriften zuordnen"),
            "instructions": (
                "برای هر پاراگراف عنوان مناسب را از a تا j انتخاب کنید. سه عنوان اضافه است.",
                "Choose the fitting heading from a–j for each paragraph. Three are extra.",
                "Wählen Sie zu jedem Absatz die passende Überschrift aus a–j. Drei bleiben übrig.",
            ),
            "stimulus_title": "Warum Pendeln unterschätzt wird",
            "pool": [
                ("a", "Was die Zahlen verschweigen"),
                ("b", "Der Preis in Lebenszeit"),
                ("c", "Wenn Wohnen billiger wird, aber nicht günstiger"),
                ("d", "Unterschiede zwischen den Verkehrsmitteln"),
                ("e", "Was Arbeitgeber ändern könnten"),
                ("f", "Eine Frage der Gewöhnung"),
                ("g", "Historische Entwicklung"),
                ("h", "Der Blick nach Skandinavien"),
                ("i", "Gesundheit als Nebenkosten"),
                ("j", "Ein Rechenbeispiel"),
            ],
            "blocks": [
                ("paragraph", "1", "",
                 "Wer täglich vierzig Minuten pro Richtung unterwegs ist, verbringt im "
                 "Arbeitsjahr rund dreihundert Stunden auf dem Weg — das entspricht etwa "
                 "siebeneinhalb Arbeitswochen. In Gehaltsverhandlungen taucht diese Größe "
                 "praktisch nie auf, obwohl sie den effektiven Stundenlohn deutlich verändert."),
                ("paragraph", "2", "",
                 "Der übliche Vergleich lautet: draußen wohnen ist billiger. Rechnet man "
                 "jedoch Fahrtkosten, den zweiten Wagen und die Zeit hinzu, kippt das Ergebnis "
                 "in vielen Fällen. Eine Wohnung, die dreihundert Euro weniger kostet, ist "
                 "keine Ersparnis, wenn sie zweihundert Euro Fahrtkosten und acht Stunden "
                 "Fahrzeit im Monat erzeugt."),
                ("paragraph", "3", "",
                 "Nicht jede Fahrt wirkt gleich. Wer im Zug sitzt und liest, erlebt die Zeit "
                 "als weniger verloren als jemand, der im Stau steht. Untersuchungen zur "
                 "Zufriedenheit zeigen den größten Unterschied nicht zwischen kurz und lang, "
                 "sondern zwischen planbar und unplanbar."),
                ("paragraph", "4", "",
                 "Hinzu kommen Kosten, die auf keiner Abrechnung stehen. Langes Pendeln geht "
                 "mit weniger Schlaf, weniger Bewegung und häufigeren Rückenbeschwerden "
                 "einher. Diese Effekte treten schon deutlich unter der oft genannten "
                 "Ein-Stunden-Grenze auf."),
                ("paragraph", "5", "",
                 "Betriebe könnten mehr tun, als sie tun. Gestaffelte Anfangszeiten kosten "
                 "wenig und entzerren die Spitzen; ein einziger fester Tag im Homeoffice "
                 "reduziert die Jahresfahrleistung um zwanzig Prozent. Beides scheitert "
                 "seltener am Geld als an der Gewohnheit."),
            ],
            "items": [
                (1, "Absatz 1", None, "j", None),
                (2, "Absatz 2", None, "c", None),
                (3, "Absatz 3", None, "d", None),
                (4, "Absatz 4", None, "i", None),
                (5, "Absatz 5", None, "e", None),
            ],
        },
        {
            "type": "gap_drag",
            "minutes": 17,
            "title": ("جای خالی", "Gap filling", "Lückentext"),
            "instructions": (
                "متن را کامل کنید. هر گزینه فقط یک بار استفاده می‌شود.",
                "Complete the text. Each option is used once only.",
                "Ergänzen Sie den Text. Jede Option wird nur einmal verwendet.",
            ),
            "stimulus_title": "Aus einem Anschreiben",
            "blocks": [
                ("section", "", "",
                 "Sehr geehrte Frau Dr. Kramer,\n\nmit großem Interesse habe ich Ihre "
                 "Ausschreibung gelesen, __6__ ich seit Jahren in genau diesem Bereich "
                 "arbeite."),
                ("section", "", "",
                 "In meiner jetzigen Position betreue ich ein Team von acht Personen, "
                 "__7__ ich zusätzlich die Budgetplanung verantworte."),
                ("section", "", "",
                 "__8__ meiner technischen Ausbildung bringe ich Erfahrung in der "
                 "Kundenkommunikation mit."),
                ("section", "", "",
                 "Über eine Einladung zu einem Gespräch würde ich mich freuen, __9__ Sie "
                 "weitere Unterlagen benötigen, sende ich diese gern nach."),
                ("section", "", "",
                 "__10__ verbleibe ich mit freundlichen Grüßen"),
            ],
            "pool": [
                ("a", "da"), ("b", "wobei"), ("c", "Neben"), ("d", "sollten"),
                ("e", "Bis dahin"), ("f", "obwohl"), ("g", "trotz"), ("h", "damit"),
            ],
            "items": [
                (6, "Lücke 6", None, "a", None),
                (7, "Lücke 7", None, "b", None),
                (8, "Lücke 8", None, "c", None),
                (9, "Lücke 9", None, "d", None),
                (10, "Lücke 10", None, "e", None),
            ],
        },
    ],
}

B2_HOEREN = {
    "skill": "hoeren",
    "duration": 20,
    "title": ("هؤرن — پرتکرار", "Hören — high frequency", "Hören — häufige Aufgaben"),
    "intro": (
        "بخش «کی چه گفت» که در B2 بیشترین اشتباه را می‌سازد.",
        "The \"who said what\" task that produces most B2 errors.",
        "Die „Wer sagt was“-Aufgabe mit den meisten B2-Fehlern.",
    ),
    "parts": [
        {
            "type": "mcq",
            "minutes": 20,
            "title": ("کی چه گفت", "Who said what", "Wer sagt was"),
            "instructions": (
                "یک بحث با دو مهمان می‌شنوید، دو بار. هر نظر مال کیست؟",
                "You hear a discussion with two guests, twice. Who says what?",
                "Sie hören eine Diskussion mit zwei Gästen, zweimal. Wer sagt was?",
            ),
            "tracks": [("Diskussion", f"{AUDIO_B2}/teil1.m4a", 2, 30, list(range(11, 21)))],
            "items": [
                (11, "Kostenlose Öffentliche würden die Städte entlasten.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "b", None),
                (12, "Zuerst muss das Angebot besser werden, dann der Preis.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "a", None),
                (13, "Auf dem Land nützt ein Gratis-Ticket wenig.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "c", None),
                (14, "Die Finanzierung ist ungeklärt.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "a", None),
                (15, "Erfahrungen aus anderen Städten sind ermutigend.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "b", None),
                (16, "Ein Umstieg gelingt nur mit dichterem Takt.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "c", None),
                (17, "Der Autoverkehr würde kaum abnehmen.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "a", None),
                (18, "Sozial wäre die Maßnahme sinnvoll.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "b", None),
                (19, "Ein Versuch über mehrere Jahre wäre nötig.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "c", None),
                (20, "Die Debatte wird zu emotional geführt.",
                 [("a", "Frau Brandt"), ("b", "Herr Yildiz"), ("c", "beide")], "a", None),
            ],
        },
    ],
}

# ------------------------------------------------------------------- C1 ---

C1_LESEN = {
    "skill": "lesen",
    "duration": 40,
    "title": ("لزن — پرتکرار", "Lesen — high frequency", "Lesen — häufige Aufgaben"),
    "intro": (
        "دو تسک سخت C1: تطبیق نظر با شخص، و جای خالی نحوی.",
        "The two hard C1 tasks: matching opinions to people, and syntactic gaps.",
        "Die zwei schweren C1-Aufgaben: Meinungen zuordnen und syntaktische Lücken.",
    ),
    "parts": [
        {
            "type": "match_person",
            "minutes": 22,
            "title": ("تطبیق نظر", "Opinion matching", "Meinungen zuordnen"),
            "instructions": (
                "سه نفر درباره ارزیابی در دانشگاه نظر داده‌اند. هر جمله به کدام نفر مربوط است؟",
                "Three people comment on university assessment. Which one does each fit?",
                "Drei Personen äußern sich zur Hochschulprüfung. Auf wen trifft jede Aussage zu?",
            ),
            "stimulus_title": "Prüfen oder begleiten?",
            "pool": [("a", "Dr. Held"), ("b", "Prof. Marek"), ("c", "Frau Sadeghi")],
            "blocks": [
                ("person", "a", "Dr. Held, Hochschuldidaktik",
                 "Die klassische Abschlussklausur misst vor allem, wer unter Zeitdruck "
                 "abrufen kann, was er drei Tage vorher gelernt hat. Was sie nicht misst, ist "
                 "die Fähigkeit, ein Problem über Wochen zu bearbeiten — also genau das, was "
                 "im Beruf verlangt wird. Ich plädiere deshalb für Portfolios, auch wenn sie "
                 "aufwendiger zu bewerten sind."),
                ("person", "b", "Prof. Marek, Rechtswissenschaft",
                 "Bei aller Sympathie für neue Formate: Vergleichbarkeit ist kein Detail, "
                 "sondern eine Frage der Fairness. Wer in Passau studiert, muss dieselbe "
                 "Chance haben wie jemand in Kiel. Portfolios sind hochgradig abhängig von der "
                 "Betreuung, und die ist eben nicht überall gleich. Ich bin nicht gegen "
                 "Reformen, aber gegen Reformen ohne Standards."),
                ("person", "c", "Frau Sadeghi, Studierendenvertretung",
                 "In der Debatte fehlt fast immer die Belastungsseite. Portfolios klingen "
                 "entspannt, bedeuten aber dauerhafte Abgabefristen über das ganze Semester. "
                 "Wer nebenbei arbeitet oder ein Kind hat, kommt damit schlechter zurecht als "
                 "mit zwei konzentrierten Prüfungswochen. Man sollte die Wahl lassen, statt "
                 "eine Form für alle vorzuschreiben."),
            ],
            "example_prompt": "Wer hält die klassische Klausur für zu eng?",
            "example_answer": "a",
            "items": [
                (1, "Wer betont die Vergleichbarkeit zwischen Hochschulen?", None, "b", None),
                (2, "Wer weist auf die Belastung durch dauernde Fristen hin?", None, "c", None),
                (3, "Wer nennt einen Nachteil des eigenen Vorschlags?", None, "a", None),
                (4, "Wer möchte Studierenden die Entscheidung überlassen?", None, "c", None),
                (5, "Wer lehnt Reformen nicht grundsätzlich ab?", None, "b", None),
                (6, "Wer stellt einen Bezug zur späteren Berufspraxis her?", None, "a", None),
            ],
        },
        {
            "type": "gap_drag",
            "minutes": 18,
            "title": ("جای خالی نحوی", "Syntactic gaps", "Syntaktische Lücken"),
            "instructions": (
                "متن را کامل کنید. به ساختار جمله دقت کنید، نه فقط به معنی.",
                "Complete the text. Watch the sentence structure, not only the meaning.",
                "Ergänzen Sie den Text. Achten Sie auf den Satzbau, nicht nur auf die Bedeutung.",
            ),
            "stimulus_title": "Aus einem Gutachten",
            "blocks": [
                ("section", "", "",
                 "Die Ergebnisse sind belastbar, __7__ sie auf einer ausreichend großen "
                 "Stichprobe beruhen."),
                ("section", "", "",
                 "__8__ der methodischen Sorgfalt bleibt eine Unsicherheit bestehen, die im "
                 "Bericht offen benannt wird."),
                ("section", "", "",
                 "Es empfiehlt sich, die Erhebung zu wiederholen, __9__ sich die "
                 "Rahmenbedingungen ändern sollten."),
                ("section", "", "",
                 "Die Auftraggeberin hat darauf verzichtet, __10__ in die Auswertung "
                 "einzugreifen."),
                ("section", "", "",
                 "__11__ sich die Empfehlungen umsetzen lassen, hängt maßgeblich von den "
                 "Ressourcen ab."),
                ("section", "", "",
                 "Der Bericht ist __12__ als abschließende Bewertung zu verstehen, sondern als "
                 "Grundlage weiterer Prüfung."),
            ],
            "pool": [
                ("a", "sofern"), ("b", "Ungeachtet"), ("c", "falls"), ("d", "irgendwie"),
                ("e", "Inwieweit"), ("f", "nicht"), ("g", "obwohl"), ("h", "Dank"),
            ],
            "items": [
                (7, "Lücke 7", None, "a", None),
                (8, "Lücke 8", None, "b", None),
                (9, "Lücke 9", None, "c", None),
                (10, "Lücke 10", None, "d", None),
                (11, "Lücke 11", None, "e", None),
                (12, "Lücke 12", None, "f", None),
            ],
        },
    ],
}

C1_HOEREN = {
    "skill": "hoeren",
    "duration": 20,
    "title": ("هؤرن — پرتکرار", "Hören — high frequency", "Hören — häufige Aufgaben"),
    "intro": (
        "بخش تک‌پخشی که در C1 بیشترین نمره را می‌برد.",
        "The play-once task that costs most at C1.",
        "Die Einmal-Hören-Aufgabe mit den größten Verlusten auf C1.",
    ),
    "parts": [
        {
            "type": "listening_mixed",
            "minutes": 20,
            "title": ("یک بار شنیدن", "Heard once", "Einmal hören"),
            "instructions": (
                "یک گفتگوی تخصصی می‌شنوید، فقط یک بار. درست یا غلط؟",
                "You hear a specialist conversation, only once. True or false?",
                "Sie hören ein Fachgespräch, nur einmal. Richtig oder falsch?",
            ),
            "tracks": [("Fachgespräch", f"{AUDIO_C1}/teil1.m4a", 1, 30, list(range(13, 21)))],
            "items": [
                (13, "Die Sprecherin arbeitet an einer Hochschule.", TRUE_FALSE, "falsch", None),
                (14, "Der Auftrag kam von einer Kommune.", TRUE_FALSE, "richtig", None),
                (15, "Die Datenlage war von Anfang an gut.", TRUE_FALSE, "falsch", None),
                (16, "Die Befragung wurde zweimal durchgeführt.", TRUE_FALSE, "richtig", None),
                (17, "Die Ergebnisse haben sie überrascht.", TRUE_FALSE, "richtig", None),
                (18, "Sie hält die Methode für übertragbar.", TRUE_FALSE, "falsch", None),
                (19, "Die Kosten lagen über dem Plan.", TRUE_FALSE, "richtig", None),
                (20, "Ein Folgeprojekt ist bereits beschlossen.", TRUE_FALSE, "falsch", None),
            ],
        },
    ],
}
