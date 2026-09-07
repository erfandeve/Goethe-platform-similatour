"""Goethe-Zertifikat C1 — original material in the official task shapes.

Lesen 70 min / 30 items · Hören 40 min / 30 items · Schreiben 75 min / 2 tasks.
"""

from ._build import TRUE_FALSE

AUDIO = "/media/exams/c1/hoeren"

LESEN = {
    "skill": "lesen",
    "duration": 70,
    "title": ("لزن — درک مطلب", "Lesen — Reading", "Lesen"),
    "intro": (
        "چهار بخش، ۳۰ سؤال، ۷۰ دقیقه. متن‌ها آکادمیک و استدلالی‌اند.",
        "Four parts, 30 items, 70 minutes. The texts are academic and argumentative.",
        "Vier Teile, 30 Aufgaben, 70 Minuten. Die Texte sind akademisch und argumentativ.",
    ),
    "parts": [
        {
            "type": "match_paragraph",
            "minutes": 18,
            "title": ("لزن ۱", "Lesen 1", "Lesen 1"),
            "instructions": (
                "یک مقاله در هفت بخش می‌خوانید. برای هر بخش عنوان مناسب را از a تا j انتخاب "
                "کنید. سه عنوان اضافه است.",
                "You read an article in seven sections. Choose the matching heading from a–j "
                "for each. Three headings are extra.",
                "Sie lesen einen Artikel in sieben Abschnitten. Wählen Sie zu jedem die "
                "passende Überschrift aus a–j. Drei bleiben übrig.",
            ),
            "stimulus_title": "Die Rückkehr der Stille",
            "pool": [
                ("a", "Wenn Ruhe zum Luxusgut wird"),
                ("b", "Messbare Folgen für den Körper"),
                ("c", "Ein Begriff, der schwer zu fassen ist"),
                ("d", "Was Städte konkret verändern könnten"),
                ("e", "Warum Gewöhnung trügt"),
                ("f", "Die Rolle der Arbeitswelt"),
                ("g", "Vom Nutzen des Lärms"),
                ("h", "Widerstand aus der Wirtschaft"),
                ("i", "Der Anfang einer Bewegung"),
                ("j", "Ein juristischer Ausblick"),
            ],
            "blocks": [
                ("paragraph", "1", "",
                 "Wer über Stille spricht, meint selten dasselbe. Für die einen ist sie die "
                 "Abwesenheit von Geräusch, für andere die Abwesenheit von Störung — ein "
                 "Unterschied, der in der Forschung erhebliche Folgen hat. Ein Wasserfall "
                 "erreicht Werte, die technisch als laut gelten, wird aber kaum je als Lärm "
                 "empfunden. Umgekehrt kann ein leise tickender Zeiger nachts unerträglich "
                 "sein. Was zählt, ist nicht allein die Lautstärke, sondern die Frage, ob wir "
                 "das Geräusch kontrollieren können."),
                ("paragraph", "2", "",
                 "Diese Unterscheidung erklärt, warum Gewöhnung weniger schützt, als man "
                 "annimmt. Anwohner einer Bahnstrecke berichten nach einigen Monaten, sie "
                 "hörten die Züge gar nicht mehr. Messungen des Schlafverhaltens zeigen "
                 "jedoch, dass die Weckreaktionen unverändert auftreten — der Körper reagiert "
                 "weiter, nur das Bewusstsein meldet es nicht mehr. Subjektive Auskunft und "
                 "objektive Belastung fallen hier deutlich auseinander."),
                ("paragraph", "3", "",
                 "Die gesundheitlichen Folgen sind inzwischen gut belegt. Dauerhafte "
                 "Lärmbelastung erhöht die Ausschüttung von Stresshormonen, was langfristig "
                 "den Blutdruck steigen lässt. Europäische Erhebungen führen einen "
                 "nennenswerten Anteil der Herz-Kreislauf-Erkrankungen in Ballungsräumen auf "
                 "Verkehrslärm zurück. Bemerkenswert ist, dass die Effekte auch dort "
                 "auftreten, wo Betroffene sich ausdrücklich nicht gestört fühlen."),
                ("paragraph", "4", "",
                 "In den Städten verschiebt sich damit eine alte Frage der Verteilung. "
                 "Wohnungen an ruhigen Innenhöfen kosten in vergleichbarer Lage regelmäßig "
                 "mehr als solche an der Straße. Wer wenig zahlen kann, wohnt lauter — und "
                 "trägt die gesundheitlichen Kosten. Ruhe, lange als selbstverständlicher Teil "
                 "des Wohnens betrachtet, wird so zu einem Gut, das man sich leisten können "
                 "muss."),
                ("paragraph", "5", "",
                 "Auch die Arbeitswelt hat ihren Anteil. Das Großraumbüro wurde eingeführt, um "
                 "Austausch zu fördern; empirisch überwiegt jedoch der Verlust an "
                 "Konzentration. Untersuchungen zeigen, dass anspruchsvolle Aufgaben in "
                 "offenen Büros messbar langsamer bearbeitet werden, und dass die Zahl der "
                 "direkten Gespräche nach der Umstellung eher sinkt als steigt — die "
                 "Beschäftigten weichen auf schriftliche Kanäle aus."),
                ("paragraph", "6", "",
                 "Praktisch ließe sich einiges ändern, und zwar ohne große Technik. "
                 "Geschwindigkeitsbegrenzungen wirken unmittelbar, weil Reifengeräusche mit "
                 "dem Tempo überproportional zunehmen. Bepflanzte Innenhöfe, versetzte "
                 "Lieferzeiten und leisere Beläge sind erprobt und vergleichsweise günstig. "
                 "Entscheidend ist weniger die einzelne Maßnahme als die Frage, ob Ruhe bei "
                 "der Planung überhaupt als Kriterium auftaucht."),
                ("paragraph", "7", "",
                 "Ansätze dazu gibt es. Mehrere europäische Städte haben begonnen, ruhige "
                 "Zonen auszuweisen und rechtlich zu schützen, ähnlich wie Grünflächen. Noch "
                 "sind das Ausnahmen, und die Wirkung lässt sich schwer belegen. Doch dass "
                 "Ruhe überhaupt als planbares Gut verhandelt wird, ist neu — und könnte am "
                 "Ende mehr bewirken als jede einzelne Lärmschutzwand."),
            ],
            "items": [
                (1, "Abschnitt 1", None, "c", None),
                (2, "Abschnitt 2", None, "e", None),
                (3, "Abschnitt 3", None, "b", None),
                (4, "Abschnitt 4", None, "a", None),
                (5, "Abschnitt 5", None, "f", None),
                (6, "Abschnitt 6", None, "d", None),
                (7, "Abschnitt 7", None, "i", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 18,
            "title": ("لزن ۲", "Lesen 2", "Lesen 2"),
            "instructions": (
                "یک متن استدلالی می‌خوانید و به هشت سؤال چهارگزینه‌ای پاسخ می‌دهید.",
                "You read an argumentative text and answer eight multiple-choice questions.",
                "Sie lesen einen argumentativen Text und beantworten acht Multiple-Choice-Fragen.",
            ),
            "stimulus_title": "Der Nutzen des Nichtwissens",
            "blocks": [
                ("paragraph", "", "",
                 "In der Wissenschaftskommunikation gilt Unsicherheit als Problem. Wer forscht, "
                 "soll erklären; wer erklärt, soll überzeugen — und Zweifel, so die verbreitete "
                 "Annahme, untergraben das Vertrauen. Eine Reihe neuerer Untersuchungen legt "
                 "das Gegenteil nahe.\n\n"
                 "In einem oft zitierten Experiment erhielten Versuchspersonen dieselbe "
                 "Meldung über eine medizinische Studie, einmal mit und einmal ohne Angabe der "
                 "statistischen Unsicherheit. Die Gruppe mit der Unsicherheitsangabe bewertete "
                 "die Quelle als glaubwürdiger, nicht als schwächer. Die Autoren erklären das "
                 "damit, dass eine offengelegte Grenze als Zeichen von Sorgfalt gelesen wird, "
                 "während der Anspruch auf vollständige Gewissheit misstrauisch macht.\n\n"
                 "Der Effekt hat allerdings Bedingungen. Er verschwindet, sobald die "
                 "Unsicherheit ohne Einordnung präsentiert wird. Wer schreibt, ein Ergebnis sei "
                 "'nicht gesichert', ohne zu sagen, was gesichert ist, produziert Ratlosigkeit. "
                 "Wirksam ist die Kombination: eine klare Aussage, gefolgt von der Angabe, wie "
                 "belastbar sie ist und was sie noch nicht abdeckt.\n\n"
                 "Für die Praxis folgt daraus ein unbequemer Schluss. Die verbreitete Strategie, "
                 "Ergebnisse für die Öffentlichkeit zu vereinfachen und Einschränkungen "
                 "wegzulassen, erhöht die kurzfristige Verständlichkeit auf Kosten der "
                 "langfristigen Glaubwürdigkeit. Wird eine Empfehlung später revidiert — was in "
                 "einem laufenden Forschungsprozess normal ist — erscheint sie dann nicht als "
                 "Fortschritt, sondern als Fehler.\n\n"
                 "Kritiker wenden ein, dass diese Befunde aus Laborsituationen stammen und sich "
                 "nicht ohne Weiteres auf eine Krisenlage übertragen lassen, in der schnell "
                 "gehandelt werden muss. Der Einwand ist berechtigt. Er ändert jedoch wenig an "
                 "der Grundfrage, die weniger lautet, ob man Unsicherheit kommuniziert, als "
                 "wann und in welcher Form."),
            ],
            "items": [
                (8, "Die verbreitete Annahme in der Wissenschaftskommunikation lautet, dass "
                    "Unsicherheit …",
                 [("a", "das Vertrauen schwächt"), ("b", "unvermeidlich ist"),
                  ("c", "das Interesse steigert"), ("d", "selten vorkommt")], "a", None),
                (9, "Im beschriebenen Experiment wurde die Quelle mit Unsicherheitsangabe …",
                 [("a", "als weniger kompetent bewertet"), ("b", "als glaubwürdiger bewertet"),
                  ("c", "gar nicht bewertet"), ("d", "als schwer verständlich bewertet")],
                 "b", None),
                (10, "Die Autoren erklären den Effekt damit, dass eine offengelegte Grenze …",
                 [("a", "als Sorgfalt gelesen wird"), ("b", "die Aussage relativiert"),
                  ("c", "Fachwissen voraussetzt"), ("d", "seltener erinnert wird")], "a", None),
                (11, "Der Effekt verschwindet, wenn …",
                 [("a", "die Studie zu klein ist"),
                  ("b", "die Unsicherheit ohne Einordnung genannt wird"),
                  ("c", "die Leser Vorwissen haben"), ("d", "die Quelle unbekannt ist")],
                 "b", None),
                (12, "Wirksam ist laut Text …",
                 [("a", "eine reine Zahlenangabe"),
                  ("b", "der Verzicht auf Einschränkungen"),
                  ("c", "eine klare Aussage samt Belastbarkeit"),
                  ("d", "die Wiederholung der Botschaft")], "c", None),
                (13, "Das Weglassen von Einschränkungen erhöht kurzfristig …",
                 [("a", "die Reichweite"), ("b", "die Verständlichkeit"),
                  ("c", "die Genauigkeit"), ("d", "die Zustimmung der Fachwelt")], "b", None),
                (14, "Eine spätere Korrektur erscheint dann als …",
                 [("a", "Fortschritt"), ("b", "Nebensache"), ("c", "Fehler"), ("d", "Ausnahme")],
                 "c", None),
                (15, "Den Einwand der Kritiker bewertet der Text als …",
                 [("a", "unbegründet"), ("b", "berechtigt, aber nicht entscheidend"),
                  ("c", "entscheidend"), ("d", "unverständlich")], "b", None),
            ],
        },
        {
            "type": "match_person",
            "minutes": 16,
            "title": ("لزن ۳", "Lesen 3", "Lesen 3"),
            "instructions": (
                "چهار متخصص درباره کار از راه دور نظر داده‌اند. هر جمله به کدام نفر مربوط "
                "است؟ هر نفر می‌تواند چند بار انتخاب شود.",
                "Four experts comment on remote work. Which one does each statement fit? A "
                "person can be chosen more than once.",
                "Vier Fachleute äußern sich zur Fernarbeit. Auf wen trifft jede Aussage zu? "
                "Personen können mehrmals gewählt werden.",
            ),
            "stimulus_title": "Vier Stimmen zur Fernarbeit",
            "pool": [
                ("a", "Prof. Dr. Anselm Weiler"),
                ("b", "Dr. Bahar Ekinci"),
                ("c", "Cornelia Lindt"),
                ("d", "Dr. Fabian Roth"),
            ],
            "blocks": [
                ("person", "a", "Prof. Dr. Anselm Weiler, Arbeitssoziologe",
                 "Die Debatte wird zu oft als Frage der Produktivität geführt, obwohl die Daten "
                 "dort erstaunlich unklar sind. Interessanter ist die Verteilung: Fernarbeit "
                 "steht überwiegend qualifizierten Beschäftigten offen, während Pflege, Handel "
                 "und Produktion davon ausgeschlossen bleiben. Wir verhandeln also eine "
                 "Freiheit, die von vornherein nur einem Teil der Erwerbstätigen zur Verfügung "
                 "steht, und übersehen dabei, dass sich der Abstand zwischen den Gruppen "
                 "vergrößert."),
                ("person", "b", "Dr. Bahar Ekinci, Organisationspsychologin",
                 "Was in unseren Erhebungen deutlich hervortritt, ist der Verlust an "
                 "beiläufiger Information. Wer nicht im Haus ist, erfährt Entscheidungen "
                 "später und ist an ihrer Entstehung seltener beteiligt. Das trifft besonders "
                 "Berufseinsteiger, die noch kein Netz haben. Ich halte hybride Modelle "
                 "deshalb nicht für einen Kompromiss, sondern für die sachlich bessere Lösung — "
                 "vorausgesetzt, die Anwesenheitstage werden gemeinsam gelegt und nicht "
                 "individuell gewählt."),
                ("person", "c", "Cornelia Lindt, Personalleiterin",
                 "In der Praxis scheitert es selten an der Technik und fast immer an der "
                 "Führung. Wer vorher über Anwesenheit gesteuert hat, steuert aus der Ferne "
                 "über Kontrolle weiter, nur schlechter. Wir haben bei uns die "
                 "Zielvereinbarungen umgestellt, bevor wir die Bürotage reduziert haben, und "
                 "genau in dieser Reihenfolge liegt der Unterschied. Kosten spart das übrigens "
                 "kaum: Was wir an Fläche einsparen, geben wir für Ausstattung und Reisen "
                 "wieder aus."),
                ("person", "d", "Dr. Fabian Roth, Stadtforscher",
                 "Die Folgen reichen weit über die Unternehmen hinaus. Innenstädte, deren "
                 "Gastronomie und Einzelhandel von Pendlerströmen lebten, verlieren an "
                 "Werktagen spürbar Umsatz, während Randlagen gewinnen. Das ist zunächst "
                 "weder gut noch schlecht, verlangt aber eine Anpassung der Planung, die "
                 "bislang kaum stattfindet. Wer heute Büroflächen im Zentrum neu baut, sollte "
                 "sich fragen, wofür sie in fünfzehn Jahren genutzt werden."),
            ],
            "example_prompt": "Wer betont, dass Fernarbeit nicht allen Berufsgruppen offensteht?",
            "example_answer": "a",
            "items": [
                (16, "Wer hält die Reihenfolge der Veränderungen für entscheidend?", None, "c", None),
                (17, "Wer verweist auf Auswirkungen außerhalb der Betriebe?", None, "d", None),
                (18, "Wer sieht Nachteile besonders für Beschäftigte am Anfang ihrer Laufbahn?",
                 None, "b", None),
                (19, "Wer hält die Datenlage zur Produktivität für wenig aussagekräftig?",
                 None, "a", None),
                (20, "Wer widerspricht der Erwartung, dass Fernarbeit Kosten senkt?", None, "c", None),
                (21, "Wer knüpft die Empfehlung an eine organisatorische Bedingung?", None, "b", None),
                (22, "Wer fordert, langfristige Nutzungsfragen früher zu stellen?", None, "d", None),
                (23, "Wer sieht eine wachsende Kluft zwischen Beschäftigtengruppen?", None, "a", None),
            ],
        },
        {
            "type": "gap_drag",
            "minutes": 18,
            "title": ("لزن ۴", "Lesen 4", "Lesen 4"),
            "instructions": (
                "متن را کامل کنید. برای هر جای خالی گزینه مناسب را از فهرست انتخاب کنید.",
                "Complete the text. For each gap choose the fitting option from the list.",
                "Ergänzen Sie den Text. Wählen Sie für jede Lücke die passende Option.",
            ),
            "stimulus_title": "Aus einer Stellungnahme zur Hochschulreform",
            "blocks": [
                ("section", "", "",
                 "Die vorgeschlagene Reform verfolgt ein nachvollziehbares Ziel, __24__ sie die "
                 "Studiendauer verkürzen und den Übergang in den Beruf erleichtern soll."),
                ("section", "", "",
                 "Gleichwohl bleibt offen, __25__ die zusätzlichen Mittel bereitgestellt werden, "
                 "ohne die eine Betreuung in kleineren Gruppen nicht möglich ist."),
                ("section", "", "",
                 "Die Erfahrung anderer Bundesländer zeigt, dass Reformen dieser Art "
                 "__26__ scheitern, wenn sie ohne Beteiligung der Fachbereiche eingeführt werden."),
                ("section", "", "",
                 "Wir empfehlen daher, den Zeitplan zu strecken, __27__ die betroffenen "
                 "Einrichtungen ihre Curricula anpassen können."),
                ("section", "", "",
                 "__28__ einer sorgfältigen Vorbereitung wäre der erwartete Nutzen kaum zu "
                 "erreichen."),
                ("section", "", "",
                 "Die Stellungnahme versteht sich __29__ als Ablehnung, sondern als Beitrag zu "
                 "einer tragfähigen Umsetzung."),
                ("section", "", "",
                 "Für Rückfragen stehen wir __30__ zur Verfügung."),
            ],
            "pool": [
                ("a", "indem"), ("b", "inwiefern"), ("c", "regelmäßig"), ("d", "damit"),
                ("e", "Ohne"), ("f", "nicht"), ("g", "selbstverständlich"), ("h", "sofern"),
                ("i", "trotz"), ("j", "gelegentlich"),
            ],
            "items": [
                (24, "Lücke 24", None, "a", None),
                (25, "Lücke 25", None, "b", None),
                (26, "Lücke 26", None, "c", None),
                (27, "Lücke 27", None, "d", None),
                (28, "Lücke 28", None, "e", None),
                (29, "Lücke 29", None, "f", None),
                (30, "Lücke 30", None, "g", None),
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
                "یک گفتگوی حرفه‌ای می‌شنوید، فقط یک بار.",
                "You hear a professional conversation, only once.",
                "Sie hören ein Fachgespräch, nur einmal.",
            ),
            "tracks": [("Teil 1", f"{AUDIO}/teil1.m4a", 1, 30, list(range(1, 9)))],
            "items": [
                (1, "Die beiden sprechen über ein laufendes Projekt.", TRUE_FALSE, "richtig", None),
                (2, "Der Zeitplan wurde bereits einmal verschoben.", TRUE_FALSE, "richtig", None),
                (3, "Die Verzögerung liegt am Personal.", TRUE_FALSE, "falsch", None),
                (4, "Ein externer Dienstleister soll beauftragt werden.", TRUE_FALSE, "richtig", None),
                (5, "Die Kosten sind bereits genehmigt.", TRUE_FALSE, "falsch", None),
                (6, "Die Leitung wird am Freitag informiert.", TRUE_FALSE, "richtig", None),
                (7, "Beide halten das Ziel für nicht mehr erreichbar.", TRUE_FALSE, "falsch", None),
                (8, "Es wird ein weiteres Treffen vereinbart.", TRUE_FALSE, "richtig", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۲", "Hören 2", "Hören 2"),
            "instructions": (
                "یک سخنرانی دانشگاهی می‌شنوید، دو بار.",
                "You hear a university lecture, twice.",
                "Sie hören einen Hochschulvortrag, zweimal.",
            ),
            "tracks": [("Teil 2", f"{AUDIO}/teil2.m4a", 2, 30, list(range(9, 17)))],
            "items": [
                (9, "Das Thema des Vortrags ist …",
                 [("a", "Stadtgeschichte"), ("b", "Sprachwandel"), ("c", "Klimapolitik")], "b", None),
                (10, "Die Rednerin beginnt mit …",
                 [("a", "einem Beispiel"), ("b", "einer Definition"), ("c", "einer Zahl")], "a", None),
                (11, "Sprachwandel geschieht laut Vortrag vor allem …",
                 [("a", "durch Gesetze"), ("b", "durch Gebrauch"), ("c", "durch Medien allein")],
                 "b", None),
                (12, "Als häufigsten Irrtum nennt sie …",
                 [("a", "Wandel sei Verfall"), ("b", "Wandel sei schnell"),
                  ("c", "Wandel sei planbar")], "a", None),
                (13, "Entlehnungen aus anderen Sprachen bewertet sie als …",
                 [("a", "Gefahr"), ("b", "normalen Vorgang"), ("c", "Randerscheinung")], "b", None),
                (14, "Ihre wichtigste Quelle sind …",
                 [("a", "Wörterbücher"), ("b", "Korpusdaten"), ("c", "Umfragen")], "b", None),
                (15, "Zum Schluss empfiehlt sie …",
                 [("a", "sprachliche Normen zu stärken"), ("b", "Beobachtung statt Bewertung"),
                  ("c", "mehr Unterricht")], "b", None),
                (16, "Fragen sind möglich …",
                 [("a", "während des Vortrags"), ("b", "am Ende"), ("c", "nur schriftlich")],
                 "b", None),
            ],
        },
        {
            "type": "listening_mixed",
            "minutes": 10,
            "title": ("هؤرن ۳", "Hören 3", "Hören 3"),
            "instructions": (
                "یک گفتگوی رادیویی می‌شنوید، فقط یک بار.",
                "You hear a radio conversation, only once.",
                "Sie hören ein Radiogespräch, nur einmal.",
            ),
            "tracks": [("Teil 3", f"{AUDIO}/teil3.m4a", 1, 30, list(range(17, 24)))],
            "items": [
                (17, "Der Gast arbeitet seit Kurzem in dem Bereich.", TRUE_FALSE, "falsch", None),
                (18, "Er beschreibt seinen Einstieg als zufällig.", TRUE_FALSE, "richtig", None),
                (19, "Er hält formale Qualifikationen für unwichtig.", TRUE_FALSE, "falsch", None),
                (20, "Er kritisiert die Ausbildung in seinem Fach.", TRUE_FALSE, "richtig", None),
                (21, "Er empfiehlt jungen Leuten, früh zu spezialisieren.", TRUE_FALSE, "falsch", None),
                (22, "Er sieht die Entwicklung der Branche skeptisch.", TRUE_FALSE, "falsch", None),
                (23, "Er kündigt ein neues Projekt an.", TRUE_FALSE, "richtig", None),
            ],
        },
        {
            "type": "mcq",
            "minutes": 10,
            "title": ("هؤرن ۴", "Hören 4", "Hören 4"),
            "instructions": (
                "یک بحث با سه شرکت‌کننده می‌شنوید، دو بار. هر نظر مال کیست؟",
                "You hear a discussion with three participants, twice. Who says what?",
                "Sie hören eine Diskussion mit drei Teilnehmenden, zweimal. Wer sagt was?",
            ),
            "tracks": [("Teil 4", f"{AUDIO}/teil4.m4a", 2, 30, list(range(24, 31)))],
            "items": [
                (24, "Ehrenamt darf keine staatlichen Aufgaben ersetzen.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "a", None),
                (25, "Ohne Freiwillige bräche vieles sofort zusammen.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "b", None),
                (26, "Die Anerkennung sollte über Dankesworte hinausgehen.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "c", None),
                (27, "Junge Menschen engagieren sich anders, nicht weniger.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "c", None),
                (28, "Der bürokratische Aufwand schreckt Freiwillige ab.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "b", None),
                (29, "Verbindliche Strukturen sind wichtiger als Begeisterung.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "a", None),
                (30, "Ein Rechtsanspruch auf Freistellung wäre sinnvoll.",
                 [("a", "Frau Dorn"), ("b", "Herr Petrov"), ("c", "Frau Aslan")], "c", None),
            ],
        },
    ],
}

SCHREIBEN = {
    "skill": "schreiben",
    "duration": 75,
    "title": ("شرایبن — نگارش", "Schreiben — Writing", "Schreiben"),
    "intro": (
        "دو تکلیف، ۷۵ دقیقه: یک متن استدلالی بر پایه نمودار و یک متن رسمی.",
        "Two tasks, 75 minutes: an argumentative text based on data, and a formal text.",
        "Zwei Aufgaben, 75 Minuten: ein argumentativer Text auf Datenbasis und ein formeller "
        "Text.",
    ),
    "max_points": 0,
    "parts": [
        {
            "type": "writing",
            "minutes": 55,
            "title": ("شرایبن ۱", "Schreiben 1", "Schreiben 1"),
            "instructions": (
                "بر اساس داده‌های زیر یک متن استدلالی حدود ۲۳۰ کلمه بنویسید. داده‌ها را توصیف "
                "کنید، دلایل احتمالی را بررسی کنید و نظر خود را با استدلال بیان کنید.",
                "Write an argumentative text of about 230 words using the data below: describe "
                "it, discuss possible reasons and give a reasoned opinion.",
                "Schreiben Sie einen argumentativen Text von etwa 230 Wörtern auf Basis der "
                "Daten: beschreiben Sie sie, erörtern Sie mögliche Gründe und begründen Sie "
                "Ihre Meinung.",
            ),
            "stimulus_title": "Wöchentliche Lesezeit nach Altersgruppe (Angaben in Minuten)",
            "stimulus_intro":
                "Eine Erhebung vergleicht, wie lange Menschen in Deutschland pro Woche Bücher "
                "lesen — 2015 gegenüber 2025.",
            "blocks": [
                ("section", "", "18–29 Jahre", "2015: 180 Minuten · 2025: 95 Minuten"),
                ("section", "", "30–49 Jahre", "2015: 155 Minuten · 2025: 120 Minuten"),
                ("section", "", "50–64 Jahre", "2015: 210 Minuten · 2025: 205 Minuten"),
                ("section", "", "65 Jahre und älter", "2015: 260 Minuten · 2025: 290 Minuten"),
                ("bullet", "", "", "Beschreiben Sie die auffälligsten Entwicklungen."),
                ("bullet", "", "", "Nennen Sie mögliche Gründe für die Unterschiede."),
                ("bullet", "", "", "Nehmen Sie begründet Stellung: Ist das ein Problem?"),
            ],
            "items": [(1, "Schreiben Sie den Text.", None, "", None)],
            "min_words": 230,
        },
        {
            "type": "writing",
            "minutes": 20,
            "title": ("شرایبن ۲", "Schreiben 2", "Schreiben 2"),
            "instructions": (
                "متن غیررسمی زیر باید رسمی بازنویسی شود، حدود ۸۰ کلمه. لحن و ساختار را "
                "متناسب با یک نامه اداری تغییر دهید.",
                "Rewrite the informal note below as a formal letter of about 80 words, adapting "
                "register and structure.",
                "Formulieren Sie die folgende informelle Notiz als formelles Schreiben von etwa "
                "80 Wörtern um und passen Sie Ton und Aufbau an.",
            ),
            "stimulus_title": "Informelle Notiz",
            "blocks": [
                ("paragraph", "", "",
                 "Hey, also das mit dem Seminar am 14. klappt bei mir leider nicht, ich hab an "
                 "dem Tag eine Dienstreise. Könnt ihr mir die Unterlagen schicken? Und wenn's "
                 "noch einen zweiten Termin gibt, wär das super, dann meld ich mich da an. "
                 "Danke!"),
                ("bullet", "", "", "Adressat: Fortbildungsstelle der Handelskammer"),
                ("bullet", "", "", "Achten Sie auf Anrede, Aufbau und Schlussformel."),
            ],
            "items": [(2, "Schreiben Sie das formelle Schreiben.", None, "", None)],
            "min_words": 80,
        },
    ],
}
