"""Hören transcripts for the in-house levels.

`manage.py make_hoeren_audio` reads these and renders one file per track with
the system's German voices, so the listening modules are playable without a
studio. Each script is written to match the answer keys in the level modules.
"""

# {level: {track filename stem: [(voice, line), …]}}
SCRIPTS = {
    "frequent-b2": {
        "teil1": [
            ("Anna", "Sie hören eine Diskussion mit Frau Brandt und Herrn Yildiz über "
                     "kostenlosen Nahverkehr."),
            ("Markus", "Für mich ist die Sache klar: Kostenlose Öffentliche würden die Städte "
                       "spürbar entlasten. Die Erfahrungen aus Tallinn und einigen "
                       "französischen Städten sind ermutigend, die Fahrgastzahlen sind dort "
                       "deutlich gestiegen. Und sozial ist die Maßnahme ohnehin sinnvoll — sie "
                       "entlastet genau die Haushalte, die wenig haben."),
            ("Sandy", "Ich sehe die Reihenfolge anders. Zuerst muss das Angebot besser werden, "
                      "dann kann man über den Preis reden. Solange der Bus zweimal pro Stunde "
                      "fährt, steigt niemand um, auch wenn er nichts kostet. Der Autoverkehr "
                      "würde kaum abnehmen, das zeigen die Zahlen ziemlich deutlich."),
            ("Markus", "Aber der Umstieg gelingt doch nur, wenn der Takt dichter wird — da sind "
                       "wir uns einig."),
            ("Sandy", "Völlig einig. Und ebenso einig sind wir uns wohl darin, dass ein "
                      "Gratis-Ticket auf dem Land wenig nützt, wo es schlicht keine Linie gibt."),
            ("Markus", "Ja, das stimmt leider."),
            ("Sandy", "Ungeklärt bleibt für mich vor allem die Finanzierung. Niemand sagt, "
                      "woher die Milliarden kommen sollen. Und ehrlich gesagt: Die Debatte "
                      "wird viel zu emotional geführt, auf beiden Seiten."),
            ("Markus", "Da würde ich widersprechen, aber gut. Was wir beide fordern, ist "
                       "jedenfalls ein Versuch über mehrere Jahre — ein Jahr sagt gar nichts."),
            ("Sandy", "Das unterschreibe ich."),
        ],
    },
    "frequent-c1": {
        "teil1": [
            ("Anna", "Sie hören ein Fachgespräch. Sie hören es nur einmal."),
            ("Markus", "Frau Doktor Lindqvist, Sie leiten ein privates Forschungsinstitut."),
            ("Sandy", "Richtig, seit neun Jahren. Von der Hochschule bin ich damals bewusst "
                      "weggegangen."),
            ("Markus", "Das Projekt, über das wir sprechen, kam von einer Stadtverwaltung?"),
            ("Sandy", "Ja, die Kommune hat uns beauftragt, die Wirkung ihrer "
                      "Verkehrsberuhigung zu untersuchen. Die Datenlage war anfangs allerdings "
                      "miserabel — es gab kaum Zählungen von vorher."),
            ("Markus", "Wie sind Sie damit umgegangen?"),
            ("Sandy", "Wir haben die Befragung zweimal durchgeführt, im Frühjahr und im "
                      "Herbst, um saisonale Effekte auszuschließen. Das Ergebnis hat uns "
                      "wirklich überrascht: Die Zufriedenheit stieg auch bei denen, die "
                      "vorher dagegen waren."),
            ("Markus", "Ließe sich die Methode auf andere Städte übertragen?"),
            ("Sandy", "Ehrlich gesagt nein, jedenfalls nicht ohne Weiteres. Die Lage dort ist "
                      "sehr speziell, eine Kleinstadt mit einer einzigen Durchgangsstraße."),
            ("Markus", "Und die Kosten?"),
            ("Sandy", "Am Ende gut zwanzig Prozent über dem Plan, wegen der zweiten Welle. "
                      "Ein Folgeprojekt ist im Gespräch, aber noch nichts beschlossen."),
        ],
    },
    "a1": {
        "teil1": [
            ("Anna", "Teil eins. Sie hören sechs kurze Gespräche."),
            ("Anna", "Nummer eins. Entschuldigung, wann fährt der nächste Zug nach Hamburg?"),
            ("Markus", "Der um neun Uhr fünfzehn ist leider ausgefallen. Der nächste geht um "
                       "neun Uhr fünfzig."),
            ("Anna", "Nummer zwei. Was kostet die Fahrkarte nach Bremen?"),
            ("Markus", "Einfach zwölf Euro, hin und zurück zweiundzwanzig."),
            ("Anna", "Und ich brauche hin und zurück."),
            ("Anna", "Nummer drei. Entschuldigen Sie, wo ist hier eine Apotheke?"),
            ("Markus", "Gehen Sie geradeaus bis zur Post. Die Apotheke ist genau gegenüber der "
                       "Post."),
            ("Anna", "Nummer vier. Möchtest du Kaffee?"),
            ("Sandy", "Nein danke, lieber einen Tee. Kaffee trinke ich abends nicht mehr."),
            ("Anna", "Nummer fünf. Wie wird das Wetter am Sonntag?"),
            ("Markus", "Nicht so gut. Es regnet den ganzen Tag. Am Samstag scheint noch die "
                       "Sonne."),
            ("Anna", "Nummer sechs. Wie viele Personen kommen denn zum Essen?"),
            ("Sandy", "Also, Paul und Nina, meine Schwester und ich. Vier Personen."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören vier Durchsagen. Sie hören jede Durchsage nur einmal."),
            ("Markus", "Achtung am Gleis drei. Der Intercity nach Köln hat heute etwa zwanzig "
                       "Minuten Verspätung. Wir bitten um Ihr Verständnis."),
            ("Sandy", "Liebe Gäste, wegen einer technischen Störung schließt das Schwimmbad "
                      "heute bereits um siebzehn Uhr statt um einundzwanzig Uhr."),
            ("Markus", "Liebe Kundinnen und Kunden, unser Markt ist morgen wie immer von acht "
                       "bis zwanzig Uhr für Sie geöffnet."),
            ("Sandy", "Willkommen im Stadtmuseum. Die nächste Führung beginnt um sechzehn Uhr "
                      "am Eingang. Der Eintritt ist heute frei."),
        ],
        "teil3": [
            ("Anna", "Teil drei. Sie hören fünf Nachrichten auf dem Anrufbeantworter."),
            ("Markus", "Guten Tag, hier ist die Firma Elektro Wagner. Unser Techniker kommt am "
                       "Dienstag zwischen zehn und zwölf Uhr. Am Montag geht es leider nicht."),
            ("Sandy", "Hallo Herr Klein, hier ist das Bürgeramt. Bitte bringen Sie zu Ihrem "
                      "Termin unbedingt Ihren Pass mit. Ein Foto brauchen Sie nicht."),
            ("Markus", "Hi, ich bin's. Das Kino ist ausverkauft. Wollen wir uns stattdessen im "
                       "Park treffen? Beim großen Spielplatz, um vier."),
            ("Sandy", "Praxis Doktor Behrens. Ihr Termin morgen wurde verschoben, von acht Uhr "
                      "dreißig auf neun Uhr dreißig. Bitte kommen Sie pünktlich."),
            ("Anna", "Hallo, hier ist Frau Berg von nebenan. Ich habe noch Ihren Schlüssel von "
                     "letzter Woche. Wann kann ich ihn vorbeibringen?"),
        ],
    },
    "a2": {
        "teil1": [
            ("Anna", "Teil eins. Sie hören fünf kurze Gespräche, jedes zweimal."),
            ("Sandy", "So ein Mist. Ich glaube, ich habe mein Handy zu Hause liegen lassen."),
            ("Markus", "Den Schlüssel hast du? Gut, dann ist es halb so schlimm."),
            ("Anna", "Nummer zwei. Treffen wir uns im Büro oder im Restaurant?"),
            ("Markus", "Weder noch. Die Besprechung findet online statt, ich schicke dir den "
                       "Link."),
            ("Anna", "Nummer drei. Wie lange fahren wir denn?"),
            ("Sandy", "Nur eine halbe Stunde. Mit dem Zug wäre es eine Stunde."),
            ("Anna", "Nummer vier. Suchen Sie eine Jacke?"),
            ("Markus", "Nein, eine Hose. Größe zweiundfünfzig, am liebsten in Dunkelblau."),
            ("Anna", "Nummer fünf. Kommt Lena mit ins Konzert?"),
            ("Sandy", "Nein, sie muss arbeiten. Ihre Kollegin ist krank und sie übernimmt die "
                      "Spätschicht."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören ein Interview. Sie hören es nur einmal."),
            ("Sandy", "Herr Nowak, Sie sind Bäcker. Wie lange machen Sie das schon?"),
            ("Markus", "Seit dreiundzwanzig Jahren. Ich habe mit sechzehn angefangen, direkt "
                       "nach der Schule."),
            ("Sandy", "Und wann beginnt Ihr Arbeitstag?"),
            ("Markus", "Ich stehe jeden Tag um drei Uhr auf. Um vier bin ich in der Backstube."),
            ("Sandy", "Auch am Wochenende?"),
            ("Markus", "Gerade am Wochenende. Samstag und Sonntag sind unsere stärksten Tage, "
                       "da haben wir bis mittags geöffnet."),
            ("Sandy", "Haben Sie ein Lieblingsbrot?"),
            ("Markus", "Ganz klar das Roggenbrot. Das braucht Zeit, und Zeit schmeckt man."),
            ("Sandy", "Würden Sie noch einmal etwas anderes machen?"),
            ("Markus", "Nein, auf keinen Fall. Der Beruf ist hart, aber ich würde ihn wieder "
                       "wählen."),
        ],
        "teil3": [
            ("Anna", "Teil drei. Sie hören fünf Nachrichten und Durchsagen, jede zweimal."),
            ("Sandy", "Guten Tag, Sprachschule Horizont. Ihr Kurs beginnt nicht wie geplant am "
                      "zweiten, sondern erst am zwölften September."),
            ("Markus", "Liebe Besucher, das Konzert heute Abend fällt nicht aus, es wird auf "
                       "nächsten Freitag verschoben. Ihre Karten bleiben gültig."),
            ("Sandy", "Guten Tag, hier ist Frau Adam. Ich hätte gern einen Termin für nächste "
                      "Woche, am liebsten am Vormittag."),
            ("Markus", "Achtung, eine Durchsage. Der Regionalzug nach Fulda fährt heute "
                       "ausnahmsweise von Gleis fünf und nicht wie gewohnt von Gleis zwei."),
            ("Sandy", "Guten Tag, Paketdienst. Wir haben Sie nicht angetroffen. Ihr Paket ist "
                      "bei Ihrem Nachbarn, Herrn Vogel, in Wohnung zwölf."),
        ],
        "teil4": [
            ("Anna", "Teil vier. Sie hören ein Gespräch, zweimal."),
            ("Sandy", "Also, wohin fahren wir im Mai?"),
            ("Markus", "Ich hätte Lust auf die Berge. Fliegen ist mir zu teuer und mit dem Auto "
                       "stehen wir nur im Stau. Nehmen wir den Zug."),
            ("Sandy", "Einverstanden. Und wo schlafen wir?"),
            ("Markus", "Ich habe ein kleines Hotel direkt am See gefunden. Nicht im Zentrum, "
                       "aber dafür ruhig."),
            ("Sandy", "Wie viele Tage?"),
            ("Markus", "Freitag bis Sonntag, also drei Tage. Mehr Urlaub habe ich nicht."),
            ("Sandy", "Und was nehmen wir mit?"),
            ("Markus", "Die Wanderschuhe auf jeden Fall, der Regenschirm schadet auch nicht. "
                       "Aber den Laptop lassen wir zu Hause. Wirklich, dieses Mal."),
        ],
    },
    "b1": {
        "teil1": [
            ("Anna", "Teil eins. Sie hören fünf kurze Texte. Sie hören jeden Text nur einmal."),
            ("Markus", "Autohaus Riedel, guten Tag. Ihr Wagen ist fertig, allerdings erst "
                       "morgen abholbereit, weil die Rechnung noch geschrieben wird. Ab neun "
                       "Uhr können Sie kommen."),
            ("Sandy", "Liebe Gäste, wegen des Regens findet das Sommerfest heute nicht im Park "
                      "statt, sondern in der Aula der Schule. Die Turnhalle wird gerade "
                      "renoviert."),
            ("Anna", "Guten Tag, hier spricht Frau Ritter. Ich hatte mich um einen "
                     "Praktikumsplatz beworben und wollte fragen, ob meine Unterlagen "
                     "angekommen sind."),
            ("Markus", "Volkshochschule Süd. Der Kurs Fotografie für Anfänger ist bereits "
                       "ausgebucht. Sie können sich aber gern auf die Warteliste setzen "
                       "lassen, es wird fast immer ein Platz frei."),
            ("Sandy", "Achtung, eine Verkehrsmeldung. Die Ringstraße ist wegen einer Baustelle "
                      "gesperrt, voraussichtlich zwei Wochen lang. Bitte umfahren Sie den "
                      "Bereich über die Uferstraße."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören einen kurzen Vortrag, zweimal."),
            ("Sandy", "Herzlich willkommen zur Führung. Das Gebäude, in dem wir stehen, war bis "
                      "neunzehnhundertachtundsiebzig eine Textilfabrik. Danach stand es fast "
                      "dreißig Jahre leer.\n"
                      "Die Renovierung hat vier Jahre gedauert, deutlich länger als geplant, "
                      "vor allem wegen des Daches.\n"
                      "Heute finden Sie hier Büros und Ateliers, insgesamt vierzig Einheiten. "
                      "Ein Museum war ursprünglich geplant, ließ sich aber nicht finanzieren.\n"
                      "Unsere Führung dauert insgesamt neunzig Minuten, mit einer kurzen Pause "
                      "nach etwa einer Stunde.\n"
                      "Und noch ein Hinweis: Fotografieren ist nur im Innenhof erlaubt, in den "
                      "Ateliers bitte nicht."),
        ],
        "teil3": [
            ("Anna", "Teil drei. Sie hören ein Gespräch. Sie hören es nur einmal."),
            ("Markus", "Lena! Das ist ja eine Überraschung. Seit dem Studium haben wir uns "
                       "nicht mehr gesehen."),
            ("Sandy", "Stimmt, sieben Jahre. Ich habe letzten Monat eine neue Stelle "
                      "angefangen, bei einem Verlag hier in der Stadt."),
            ("Markus", "Und wie ist es?"),
            ("Sandy", "Deutlich besser. Vorher bin ich jeden Tag eine Stunde gependelt, jetzt "
                      "sind es fünfzehn Minuten mit dem Rad. Und ich verdiene auch etwas mehr "
                      "als vorher."),
            ("Markus", "Und der Chef?"),
            ("Sandy", "Sehr angenehm, wirklich. Er lässt einen arbeiten. Ich überlege sogar, "
                      "nebenbei den Master zu machen, die Firma würde das unterstützen."),
            ("Markus", "Das klingt gut. Wollen wir nächste Woche mal einen Kaffee trinken?"),
            ("Sandy", "Gern. Donnerstag nach der Arbeit?"),
            ("Markus", "Donnerstag passt."),
        ],
        "teil4": [
            ("Anna", "Teil vier. Sie hören eine Diskussion, zweimal. Frau Klein und Herr Adler "
                     "sprechen über Hausaufgaben."),
            ("Sandy", "Ich bin überzeugt, dass Hausaufgaben wichtig sind. Was man nicht "
                      "wiederholt, vergisst man innerhalb weniger Tage. Ein völliges Verbot "
                      "wäre der falsche Weg."),
            ("Markus", "Da widerspreche ich. Kinder sitzen sechs Stunden in der Schule und "
                       "sollen danach weitermachen. Sie brauchen nachmittags freie Zeit. "
                       "Ganztagsschulen, in denen alles in der Schule passiert, wären die "
                       "bessere Lösung."),
            ("Sandy", "Ein Punkt eint uns aber: Eltern helfen oft zu viel. Dann übt nicht das "
                      "Kind, sondern die Mutter."),
            ("Markus", "Absolut, das sehe ich genauso. Und entscheidend ist ohnehin die Menge, "
                       "nicht die Frage, ob überhaupt."),
            ("Sandy", "Auch da stimme ich zu. Wenn vier Fächer am selben Tag Aufgaben geben, "
                      "läuft etwas falsch."),
            ("Markus", "Die Lehrkräfte müssten sich einfach besser absprechen."),
            ("Sandy", "Genau. Aber abschaffen? Nein."),
        ],
    },
    "c1": {
        "teil1": [
            ("Anna", "Teil eins. Sie hören ein Gespräch am Arbeitsplatz. Sie hören es nur "
                     "einmal."),
            ("Markus", "Wie steht es um die Migration der Datenbank?"),
            ("Sandy", "Ehrlich gesagt kritisch. Wir haben den Termin schon einmal verschoben, "
                      "vom März auf den Mai, und ich fürchte, auch der ist nicht zu halten."),
            ("Markus", "Liegt es an der Besetzung?"),
            ("Sandy", "Nein, das Team ist vollständig. Das Problem sind die Altdaten, die "
                      "deutlich unsauberer sind als angenommen. Ich schlage vor, einen "
                      "externen Dienstleister für die Bereinigung zu beauftragen."),
            ("Markus", "Sind die Mittel dafür schon freigegeben?"),
            ("Sandy", "Noch nicht, das müsste über den Bereichsleiter laufen. Ich informiere "
                      "die Leitung am Freitag in der Runde."),
            ("Markus", "Halten Sie das Ziel insgesamt noch für erreichbar?"),
            ("Sandy", "Ja, mit der externen Unterstützung durchaus. Ohne sie nicht. Lassen Sie "
                      "uns nächste Woche noch einmal zusammensetzen, Dienstag um zehn?"),
            ("Markus", "Dienstag um zehn, notiert."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören einen Vortrag, zweimal."),
            ("Sandy", "Stellen Sie sich vor, jemand sagt zu Ihnen: Das macht Sinn. Vor dreißig "
                      "Jahren hätten viele das für falsch gehalten. Heute steht es in "
                      "Zeitungen.\n"
                      "Genau darum geht es heute: um Sprachwandel.\n"
                      "Sprachwandel entsteht ganz überwiegend durch Gebrauch, nicht durch "
                      "Regelungen. Kein Gesetz hat je eine Form durchgesetzt, die niemand "
                      "verwendet.\n"
                      "Der häufigste Irrtum ist die Gleichsetzung von Wandel und Verfall. "
                      "Diese Klage finden Sie in jedem Jahrhundert, wörtlich.\n"
                      "Entlehnungen aus anderen Sprachen sind dabei ein vollkommen normaler "
                      "Vorgang; das Deutsche hat immer entlehnt.\n"
                      "Unsere wichtigste Grundlage sind heute Korpusdaten, also große "
                      "Textsammlungen, nicht mehr das Sprachgefühl einzelner Fachleute.\n"
                      "Mein Vorschlag zum Schluss: beobachten statt bewerten.\n"
                      "Fragen sammeln wir bitte bis zum Ende des Vortrags."),
        ],
        "teil3": [
            ("Anna", "Teil drei. Sie hören ein Radiogespräch. Sie hören es nur einmal."),
            ("Markus", "Sie arbeiten seit über zwanzig Jahren als Restauratorin. Wie sind Sie "
                       "dazu gekommen?"),
            ("Sandy", "Durch einen Zufall, ehrlich gesagt. Ich habe während des Studiums in "
                      "einem Museumsdepot gejobbt und bin dort geblieben."),
            ("Markus", "Braucht man dafür zwingend eine formale Ausbildung?"),
            ("Sandy", "Unbedingt. Ohne Chemie und Materialkunde richtet man mehr Schaden an "
                      "als Nutzen. Wer etwas anderes behauptet, hat nie an einem Original "
                      "gearbeitet."),
            ("Markus", "Wie beurteilen Sie die Ausbildung heute?"),
            ("Sandy", "Kritisch. Die Studiengänge sind zu theoretisch geworden, die "
                      "Werkstattzeit wurde immer weiter gekürzt. Das halte ich für einen "
                      "Fehler."),
            ("Markus", "Was raten Sie jungen Leuten?"),
            ("Sandy", "Sich Zeit zu lassen und gerade nicht zu früh zu spezialisieren. Die "
                      "Spezialisierung kommt von selbst."),
            ("Markus", "Und die Zukunft der Branche?"),
            ("Sandy", "Da bin ich zuversichtlich. Es gibt mehr Aufträge, als wir bearbeiten "
                      "können. Im Herbst starte ich ein neues Projekt zur Sicherung von "
                      "Wandmalereien."),
        ],
        "teil4": [
            ("Anna", "Teil vier. Sie hören eine Diskussion mit Frau Dorn, Herrn Petrov und "
                     "Frau Aslan, zweimal."),
            ("Sandy", "Ehrenamt ist wertvoll, aber es darf keine staatlichen Aufgaben "
                      "ersetzen. Wo Pflichtaufgaben von Freiwilligen erledigt werden, spart "
                      "der Staat an der falschen Stelle. Und ehrlich gesagt: verbindliche "
                      "Strukturen sind mir wichtiger als Begeisterung."),
            ("Markus", "Das sehe ich anders. Ohne Freiwillige bräche in vielen Vereinen und "
                       "Verbänden morgen alles zusammen. Und was uns wirklich schadet, ist der "
                       "bürokratische Aufwand — allein die Formulare schrecken die Hälfte der "
                       "Interessierten ab."),
            ("Anna", "Beides stimmt. Ich möchte einen anderen Punkt betonen: Anerkennung muss "
                     "über Dankesworte hinausgehen. Und der Vorwurf, junge Menschen "
                     "engagierten sich weniger, ist falsch — sie engagieren sich anders, "
                     "projektbezogen statt auf zwanzig Jahre.\n"
                     "Ein Rechtsanspruch auf Freistellung für Ehrenamt wäre aus meiner Sicht "
                     "das wirksamste Mittel."),
        ],
    },
}
