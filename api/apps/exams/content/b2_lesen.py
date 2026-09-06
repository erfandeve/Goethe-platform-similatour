"""Goethe-Zertifikat B2 · Modellsatz Erwachsene — module Lesen (65 min, 30 points).

Content transcribed from the publicly published Modellsatz. Replace with
in-house items before selling access; the wording belongs to Goethe-Institut.
"""

PERSONS = [
    (
        "a",
        "Erik",
        "In der heutigen Gesellschaft wird leider nur noch konsumiert. Es zählen Besitz und "
        "Leistung und das im Überfluss; das ist den Menschen wichtig. Ich sehe das anders, denn "
        "ich habe nur Sachen, die ich wirklich brauche. Ein Autokauf käme mir zum Beispiel nicht "
        "in den Sinn, ich bevorzuge das Rad oder gehe zu Fuß. Eine größere Wohnung? Warum? – "
        "Meine Einzimmerwohnung ist fast leer: Bett, Tisch, zwei Stühle, Garderobe. Einen "
        "Kühlschrank brauche ich nicht. Auch als Veganer kann man genussvoll essen. Erdbeeren und "
        "Salat pflanze ich auf dem Balkon an. Wenn ich reise, dann mit Rucksack und Zelt, ohne "
        "Kamera und Schnickschnack. Bei Freunden daheim mit tollen Fotos angeben gibt mir nichts. "
        "Das hat nichts mit Geiz zu tun – das einfache und entspannte Leben ist, was ich will.",
    ),
    (
        "b",
        "Katharina",
        "Die gesamte Debatte über die richtige Lebensweise nervt mich: Warum auf etwas verzichten? "
        "Dinge können die schönste Nebensache der Welt sein! Am Abend kehre ich gern in meine "
        "Wohnung heim und am Wochenende lade ich lieber Freunde ein, um ihnen Bilder von meinem "
        "letzten Urlaub zu zeigen, als mich beim Sport abzumühen. Viel brauche ich nicht, um mich "
        "in den Großstädten der Welt wohlzufühlen: ein bisschen Luxus im Hotel, interessante "
        "Ausstellungen und schick essen gehen. Viel nehme ich schon deswegen nicht mit, damit im "
        "Koffer genug Platz für die Einkäufe ist. Zu einem guten Steak sage ich nie nein. Gesund "
        "kann, muss Essen aber nicht sein – man lebt schließlich nur einmal. Mein Auto, ein "
        "Cabriolet, nutze ich jeden Tag beruflich, im Sommer am liebsten mit dem Dach offen. "
        "Bescheidenheit ist doch nur etwas für die Leute, die sich nichts leisten können.",
    ),
    (
        "c",
        "Franzi",
        "Für mich ist es wichtig, sowohl gut zu mir als auch zu meiner Umwelt zu sein. Im Alltag "
        "versuche ich auf Fleisch zu verzichten und baue Kräuter am Fenster meines kleinen, aber "
        "feinen Appartements an. Ich genieße es, am Wochenende mit Freunden gut essen zu gehen, "
        "und wenn es mal nichts Vegetarisches gibt, esse ich ab und zu auch Fleisch. Zur Arbeit "
        "nehme ich am liebsten das Rad – das hält mich fit und ist nebenbei auch noch "
        "umweltfreundlich; bei Schnee und Regen sind dann aber doch die Öffentlichen angenehmer. "
        "Vielleicht mache ich irgendwann mal Carsharing, also Autos am Straßenrand mieten. Mit "
        "Geld hat das alles aber nichts zu tun. Es besteht für mich ein großer Unterschied "
        "zwischen Urlaub und Reisen: Im Urlaub gönne ich mir gerne etwas: Ein Sterne-Hotel oder "
        "einen Einkaufstrip. Auf Reisen jedoch will ich Neues entdecken. Da erkunde ich Länder am "
        "liebsten auf Wanderungen.",
    ),
    (
        "d",
        "Nils",
        "Ich halte das für eine ziemlich deutsche Debatte! In keinem anderen Land wird so viel "
        "über das Thema „Richtig leben“ diskutiert. Geld ist nicht alles, aber kann nicht schaden; "
        "z. B. für Bio-Produkte: Ich selbst kaufe Fleisch und Wurst auf dem Bauernhof ein, nicht "
        "nur der Natur und der Gesundheit zuliebe, es schmeckt einfach besser, und viel Fleisch "
        "esse ich sowieso nicht. Der Versuch, einfach und natürlich zu leben, ist bei der "
        "Ernährung leider nicht immer kostengünstig. Das Thema ‚Auto‘ sehe ich eher nicht "
        "ideologisch: Für mich ist es in erster Linie ein Fortbewegungsmittel, das manchmal "
        "notwendig ist, manchmal auch einfach nur bequem. Wegen des Verkehrs benutze ich oft die "
        "Öffentlichen oder das Rad. Ich habe eine Zwei-Zimmer-Wohnung in der Innenstadt und zwar "
        "in Flussnähe, der Blick aufs Wasser ist mir wichtig. Für meine Reisen habe ich ein "
        "Wohnmobil mit allem Luxus. Da ist man völlig frei und hat doch immer alles Nötige dabei!",
    ),
]

TEIL1_ITEMS = [
    (1, "Wer sieht im Auto einen Gebrauchsgegenstand?", "d"),
    (2, "Wer empfindet Besitz als unwichtig?", "a"),
    (3, "Wer verzichtet auf Fleisch?", "a"),
    (4, "Für wen spielt die Lage der Wohnung eine große Rolle?", "d"),
    (5, "Für wen ist der Naturschutz bei Entscheidungen wichtig?", "c"),
    (6, "Wer denkt, einfach lebende Personen hätten zu wenig Geld?", "b"),
    (7, "Wer nimmt auf Reisen nichts Überflüssiges mit?", "a"),
    (8, "Für wen zählt beim Essen allein, etwas zu genießen?", "b"),
    (9, "Wer mag sowohl Luxus als auch das einfache Leben?", "c"),
]

# --- Teil 2: article with numbered gaps -------------------------------------

TEIL2_PARAGRAPHS = [
    "Über eine Milliarde Menschen reisen jährlich in ein anderes Land. Ob von Deutschland nach "
    "Italien, von Kanada nach Mexiko oder von Japan nach Australien. Noch nie waren so viele "
    "Touristinnen und Touristen unterwegs. Kaum ein Wirtschaftszweig wächst so schnell und "
    "kontinuierlich wie der Tourismus. [[0]]",
    "Schon in der Antike gingen Menschen an andere Orte. Oft zu Fuß oder mit dem Pferd. Das "
    "dauerte jedoch lange und war sehr mühsam. Nur wenige konnten es sich leisten, in einer "
    "Kutsche zu reisen. Besonders schnell war die Kutsche allerdings auch nicht. [[10]] Erst als "
    "die Eisenbahn und das Dampfschiff erfunden wurden, änderte sich das.",
    "Die Reisen, wie wir sie heute kennen, verdanken wir vor allem dem Briten Thomas Cook. Er "
    "organisierte 1841 eine Zugfahrt mit Blasmusik, Tee und belegten Broten in eine 20 km "
    "entfernte Kleinstadt. [[11]] Damit erfand der Brite die erste Pauschalreise der Welt – ein "
    "großer Erfolg.",
    "Die meisten solcher Reisen blieben jedoch lange ein Luxus, den sich die meisten Menschen "
    "nicht leisten konnten. An sechs Tagen der Woche und zehn Stunden am Tag zu arbeiten, war um "
    "1900 normal. [[12]] Dies änderte sich im Laufe des 20. Jahrhunderts, als die Arbeiter mehr "
    "Freizeit bekamen, die Löhne stiegen und die Reisekosten sanken. Seitdem steigt die Anzahl "
    "der Touristen stetig.",
    "Die derzeit beliebtesten Reiseziele weltweit sind Frankreich, die USA und Spanien. Aber auch "
    "Deutschland zieht immer mehr Reisende an. Insbesondere die 15- bis 24-jährigen Europäerinnen "
    "und Europäer kommen gerne nach Deutschland. Am liebsten fahren sie in die großen Städte wie "
    "Berlin oder München. [[13]] Ein Grund dafür, dass Städtereisen insgesamt immer beliebter "
    "werden.",
    "Der Tourismus hat das Aussehen vieler Orte verändert. [[14]] So entstand das typische Bild, "
    "das man heute an vielen Orten sieht, die touristisch geprägt sind: blaues Meer, Sandstrand "
    "und Hochhäuser. Auch die Städte verändern sich. Cafés und Restaurants werden immer teurer. "
    "[[15]] Vor allem Anwohnerinnen und Anwohner ärgern sich darüber. Aber auch Touristinnen und "
    "Touristen suchen immer häufiger nach Orten, die weniger besucht werden.",
]

TEIL2_OPTIONS = [
    ("a", "Dort gibt es neben den vielen Bars und Clubs auch viele gute Kulturangebote."),
    ("b", "Dennoch fahren immer mehr Touristinnen und Touristen aufs Land."),
    ("c", "Noch Ende des 18. Jahrhunderts war man von München nach Frankfurt 74 Stunden unterwegs."),
    ("d", "Alle Leistungen gab es zu einem geringen Gesamtpreis."),
    ("e", "Hotels und Häuserblocks mit Urlaubswohnungen prägen heute vielerorts das Bild."),
    ("f", "Es gab nur drei Tage Urlaub im Jahr."),
    ("g", "Diese Veränderungen gefallen natürlich nicht jedem."),
    ("h", "Trotzdem hatten die Arbeiter nur wenig Freizeit."),
]

TEIL2_ITEMS = [(10, "c"), (11, "d"), (12, "f"), (13, "a"), (14, "e"), (15, "g")]

# --- Teil 3: article with three-option questions ----------------------------

TEIL3_PARAGRAPHS = [
    "Das Wartezimmer in Arztpraxen ist voll mit Menschen, Bakterien und verbrauchter Luft. Bevor "
    "sich jemand zusätzliche Viren ins Gesicht husten lässt, bleibt er manchmal lieber zu Hause "
    "und sucht Rat beim Doktor im Netz.",
    "Von den Deutschen suchen 38 Prozent bei Gesundheitsfragen Rat im Internet und klicken "
    "Gesundheitsportale an, fand man kürzlich heraus. Innerhalb Europas war das Interesse nur in "
    "Schweden, Norwegen und in Finnland noch größer. Laut einer Studie gehört zu den "
    "meistgesuchten Krankheiten Diabetes, woran so viele Europäerinnen und Europäer leiden. "
    "Ebenfalls oft gesucht: Leiden, über die viele nicht gerne sprechen, auch nicht mit dem Arzt.",
    "Je mehr das Googeln von Krankheiten zum Volkssport wird, desto stärker stellt sich für "
    "Politiker und Mediziner die Frage nach der Qualität des Angebots. Kann sein, dass dort Hilfe "
    "wartet. Kann aber auch sein, dass die Beschwerden sich nach der Lektüre schlimmer anfühlen "
    "als vorher.",
    "Denn die Qualität ist in vielen Fällen richtig schlecht: Es gibt häufig lückenhafte "
    "Informationen und Widersprüche. Manchmal dienen die Texte und Bilder vor allem dazu, für ein "
    "Medikament oder eine Heilmethode zu werben. Wer sich stundenlang durch die Ergebnislisten "
    "klickt, landet auf Seiten von Krankenkassen, Vereinen, Pharmaunternehmen, Verlagen, "
    "Medizinern, Hobbyratgebern.",
    "Die organisierte Ärzteschaft ist keineswegs grundsätzlich dagegen, wenn sich Patienten online "
    "schlau machen. „Die Frage ist nur, wann sie es tun und wo sie suchen“, sagt Claudia Becker "
    "vom Institut „Medizinisches Zentrum für therapeutische Qualität“. Dort hält man es für "
    "falsch, Krankheitssymptome, die man bei sich entdeckt hat, per Suchmaschine selbst zu "
    "diagnostizieren. „Wenn Patienten richtige und gute Informationen haben, vereinfacht das "
    "vieles.“ Ziel ist dabei nicht das Verständnis fachlicher Details. „Aber Patienten können "
    "Ärzte später informiert fragen – und genau darum geht es.“",
    "Wer Informationen unkritisch aufnimmt, für den bringt das eher Gefahren statt Orientierung "
    "mit sich: Nicht wenige Versprechen auf Heilung sind Betrug. Auch Internetseiten und -foren, "
    "die Patienten über Selbsthilfe informieren, sollten mit Vorsicht gelesen werden. „Es ist "
    "natürlich vorteilhaft, wenn Ratsuchende anonym von den Erfahrungen ebenfalls Betroffener "
    "profitieren können. Andererseits wissen sie nie, mit wem sie sich da gerade über "
    "hochsensible Dinge unterhalten.“",
    "Eine gewisse Gefahr bestehe vor allem dann, wenn in Foren persönliche Daten wie "
    "E-Mail-Adressen, Telefonnummern oder Krankengeschichten abgefragt würden: „Immer wieder "
    "kommt es in Patientenforen vor, dass das Gespräch mit anderen Kranken insgeheim von Dritten "
    "benutzt wird. Oft wird man danach pausenlos mit unerwünschter Werbung der "
    "Gesundheits-Industrie bombardiert.“",
]

TEIL3_ITEMS = [
    (16, "Das Interesse richtet sich auf Krankheiten, …",
     [("a", "die auch Ärzte überfordern."),
      ("b", "die besonders schmerzhaft sind."),
      ("c", "für die sich die Betroffenen schämen.")], "c"),
    (17, "Viele Mediziner und Politiker zweifeln daran, dass …",
     [("a", "das Internet brauchbare Hilfe liefert."),
      ("b", "die berichteten Beschwerden echt sind."),
      ("c", "sich die Gesundheit der Kranken verbessert.")], "a"),
    (18, "Was ist am Internet-Angebot oft so schlecht?",
     [("a", "Das Angebot ist zu groß."),
      ("b", "Es gibt falsche Informationen."),
      ("c", "Viele Informationen sind unvollständig.")], "c"),
    (19, "Claudia Becker findet, Patienten sollten sich im Internet …",
     [("a", "auf das Arztgespräch vorbereiten."),
      ("b", "detailliertes Fachwissen anlesen."),
      ("c", "nach einem Arztgespräch informieren.")], "a"),
    (20, "Claudia Becker warnt Patienten vor …",
     [("a", "gefährlichen Versprechen im Internet."),
      ("b", "Anleitungen zur Selbsttherapie."),
      ("c", "Kontakt mit anonymen Ratsuchenden.")], "a"),
    (21, "Ratsuchende sollten vorsichtig sein, in Foren …",
     [("a", "ihre Krankheit zu beschreiben."),
      ("b", "Informationen über sich weiterzugeben."),
      ("c", "auf Werbung der Gesundheitsindustrie zu reagieren.")], "b"),
]

# --- Teil 4: headings matched to opinion boxes ------------------------------

TEIL4_STATEMENTS = [
    ("a", "Amelie, Bonn",
     "Es hört sich im ersten Moment vielleicht etwas überraschend an – aber gerade für "
     "berufstätige Eltern hat das digitale Nomadentum Pluspunkte: Man kann seinen Kindern die "
     "Welt zeigen und sich tagsüber die Zeit für sie nehmen, die sie brauchen; gearbeitet wird "
     "dann eben nachts."),
    ("b", "Eva, Berlin",
     "Die Gefahr, dass die eigene Leistung absinkt, ist einfach zu groß: Jede Arbeit braucht "
     "Struktur und das Gespräch mit Experten, um herauszufinden, ob man richtig liegt. Wenn jeder "
     "immer nur allein vor sich hin arbeitet, fehlt der Vergleich."),
    ("c", "Inga, Hannover",
     "Auch wenn es unter den Jüngeren heutzutage Mode ist, sich als digitale Nomaden zu verstehen "
     "– wieso möchte keiner mehr fest an einem Ort verankert sein? Woher weiß man denn sonst, "
     "wohin man gehört?"),
    ("d", "Steven, Greifswald",
     "Kaum jemand kann und will ständig allein am Computer vor sich hinarbeiten. Das Arbeiten in "
     "flexiblen Büros wäre eine Möglichkeit, einen ständigen Austausch möglich zu machen, "
     "fachlich wie menschlich. Aber man würde dabei hoffentlich nicht die Freiheit verlieren, "
     "weiterzuziehen, wenn und wann man will."),
    ("e", "Jan, Chemnitz",
     "Diese Arbeitsform funktioniert nur ohne Familie und Verantwortung. Wer hat schon einen "
     "Partner, der ständig umziehen kann und will, weil er selbst digitaler Nomade ist? Und "
     "sobald eine gute Schulbildung für den Nachwuchs gesichert werden muss, hat dieses "
     "Arbeitsmodell mehr Nachteile als Vorteile."),
    ("f", "Sarah, München",
     "Es darf nicht vergessen werden, dass auch das Berufsleben aus mehr als nur Arbeit besteht: "
     "Mit wem wird die Mittagspause verbracht? Wer hat schon Lust, immer allein zu sein? Wer hat "
     "schon die Kraft, sich alle paar Wochen einen neuen Freundeskreis aufzubauen?"),
    ("g", "Janice, Magdeburg",
     "Zeit- und raumflexibel zu arbeiten, wo und wann auch immer man will – vom Laptop, "
     "Smartphone oder Tablet aus –, nennt man digitales Nomadentum. Das mag für manche zwar etwas "
     "traurig klingen, nach Verlust der Heimat, aber es ist das einzige dem 21. Jahrhundert "
     "angemessene Arbeitsmodell."),
    ("h", "Katharina, Stuttgart",
     "Bei allen Vorzügen besteht doch die ständige Angst, zu viel zu reisen und zu wenig zu "
     "schaffen. Es ist letztlich alles eine Frage des Charakters: Um sein eigener Chef zu sein, "
     "ist auf jeden Fall ein hohes Maß an Selbstorganisation und Selbstdisziplin notwendig."),
]

TEIL4_ITEMS = [
    (22, "Sich zu Hause zu fühlen, ist wichtig", "c"),
    (23, "Moderne Arbeitsgeräte ermöglichen neue Arbeitsformen und Lebensweisen", "g"),
    (24, "Arbeiten ohne einen Vorgesetzten bringt Herausforderungen", "h"),
    (25, "Leben als digitaler Nomade eignet sich besonders für Singles", "e"),
    (26, "Wichtig ist der Austausch mit Kollegen auch außerhalb der Arbeit", "f"),
    (27, "Qualitätssteigerung durch den Austausch unter Kollegen", "b"),
]

# --- Teil 5: study regulations matched to headings --------------------------

TEIL5_HEADINGS = [
    ("a", "Abschluss des Bachelorstudiums"),
    ("b", "Aufbau und Inhalte des Studiums"),
    ("c", "Studienbeginn"),
    ("d", "Studiendauer und Studienvolumen"),
    ("e", "Vermittlungsformen"),
    ("f", "Zugangsvoraussetzungen"),
    ("g", "Studienziele"),
    ("h", "Auslandsaufenthalt"),
]

TEIL5_PARAGRAPHS = [
    (0, "§ 0", "Das Studium kann nur zum Wintersemester aufgenommen werden.", "c"),
    (28, "§ 28",
     "Die allgemeine Qualifikation für das Studium wird durch ein Zeugnis der "
     "Hochschulzugangsberechtigung gemäß § 17 BremHG (insbesondere allgemeine Hochschulreife, "
     "fachgebundene Hochschulreife, Fachhochschulreife) oder ein durch Rechtsvorschrift oder von "
     "der zuständigen staatlichen Stelle als gleichwertig anerkanntes Zeugnis nachgewiesen. "
     "Fachspezifisch: – der Nachweis von Kenntnissen in Englisch (Gemeinsamer europäischer "
     "Referenzrahmen, Stufe B2) und einer weiteren modernen Fremdsprache (Gemeinsamer "
     "europäischer Referenzrahmen, Stufe B1) oder – der Nachweis von Kenntnissen in Englisch "
     "(Gemeinsamer europäischer Referenzrahmen, Stufe B2) und Lateinkenntnissen jeweils vor "
     "Studienbeginn.", "f"),
    (29, "§ 29",
     "(1) Die Regelstudienzeit umfasst sechs Semester. Der Gesamtumfang des studentischen "
     "Arbeitsaufwandes für das Bachelorstudium Theaterwissenschaft beträgt 180 Leistungspunkte. "
     "(2) Das Studium kann auch als Teilzeitstudium betrieben werden. Im Falle eines "
     "Teilzeitstudiums verringert sich der studentische Arbeitsaufwand pro Jahr entsprechend dem "
     "Anteil des Teilzeitstudiums. Die Regelstudienzeit verlängert sich entsprechend. Der "
     "Prüfungsausschuss entscheidet auf Antrag der/des Studierenden über den Anteil des "
     "Teilzeitstudiums.", "d"),
    (30, "§ 30",
     "– Vorlesungen (V) – Seminare (S) – Übungen (Ü) – Praktika (P) – Tutorien (Tut). Die "
     "Modulverantwortlichen können festlegen, dass eine Lernplattform begleitend zum "
     "Präsenzstudium für die Vermittlung von Lehrinhalten eingesetzt wird.", "e"),
]
