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
        # Teil 1: five texts, one file each, so each can be replayed on its own.
        "teil1-1": [
            ("Anna", "Text eins."),
            ("Sandy", "Achtung an Gleis drei: Der ICE nach München fährt heute nicht von "
                      "Gleis drei, sondern von Gleis sieben ab. Der Zug hat etwa zehn Minuten "
                      "Verspätung. Die Regionalbahn nach Augsburg fährt wie geplant von Gleis "
                      "zwölf."),
        ],
        "teil1-2": [
            ("Anna", "Text zwei."),
            ("Shelley", "Hallo Jonas, hier ist Mia. Wegen morgen Abend: Getränke haben wir "
                        "genug, die hat Paul schon gekauft. Kannst du vielleicht einen Salat "
                        "machen? Brot bringt meine Schwester mit. Bis morgen!"),
        ],
        "teil1-3": [
            ("Anna", "Text drei."),
            ("Sandy", "Guten Tag, Herr Schulz, hier ist die Praxis Doktor Lehner. Ihr Termin "
                      "am Dienstag um neun Uhr muss leider ausfallen, die Ärztin ist krank. "
                      "Können Sie am Mittwoch kommen? Um neun ist schon besetzt, aber um elf "
                      "Uhr ist noch frei. Bitte rufen Sie uns kurz zurück."),
        ],
        "teil1-4": [
            ("Anna", "Text vier."),
            ("Markus", "Und nun das Wetter für das Wochenende. Am Freitag regnet es noch in "
                       "ganz Deutschland, und es bleibt kühl. Am Samstag scheint dann überall "
                       "die Sonne, bei Temperaturen bis dreiundzwanzig Grad. Am Sonntag wird "
                       "es im Norden windig, in den Bergen ist sogar Schnee möglich."),
        ],
        "teil1-5": [
            ("Anna", "Text fünf."),
            ("Reed", "Am Samstag ist wieder Stadtfest auf dem Marktplatz! Es gibt Musik, "
                     "Essen und viele Spiele. Für alle Kinder unter zehn Jahren ist die Fahrt "
                     "mit dem Riesenrad kostenlos. Die ersten hundert Besucher bekommen ein "
                     "T-Shirt, aber nur mit einem Online-Ticket. Und Eis gibt es am Stand vom "
                     "Café Venezia zum halben Preis."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören ein Gespräch. Sie hören den Text einmal."),
            ("Markus", "Jana, ich freue mich so auf die Woche bei dir! Was machen wir denn am "
                       "Montag, wenn ich ankomme?"),
            ("Sandy", "Am Montag soll das Wetter schlecht sein. Da gehen wir ins Museum, das "
                      "neue Technikmuseum ist super."),
            ("Markus", "Gut. Und am Dienstag? Ich möchte unbedingt mal ins Schwimmbad."),
            ("Sandy", "Dienstags ist das Schwimmbad geschlossen. Aber am Dienstag wird es warm, "
                      "da können wir eine Radtour an den See machen. Ich habe ein zweites "
                      "Fahrrad für dich."),
            ("Markus", "Super. Und Schwimmen geht dann am Mittwoch?"),
            ("Sandy", "Nein, am Mittwoch bin ich bis zum Abend im Büro. Du kannst ja allein in "
                      "die Stadt gehen. Aber abends koche ich für uns – dein Lieblingsessen!"),
            ("Markus", "Toll. Am Donnerstag gibt es doch ein Fußballspiel, oder?"),
            ("Sandy", "Ja, aber das sehen wir nicht. Am Donnerstag spielt meine Lieblingsband "
                      "im Park, die Karten habe ich schon gekauft."),
            ("Markus", "Ein Konzert, sehr gut! Aber am Freitag möchte ich endlich schwimmen "
                       "gehen."),
            ("Sandy", "Okay, am Freitag gehen wir ins Schwimmbad. Versprochen. Danach könnten "
                      "wir noch ins Kino gehen."),
            ("Markus", "Ach nein, ins Kino gehe ich zu Hause schon so oft. Lieber nicht."),
            ("Sandy", "Wie du willst. Und am Samstag ist morgens Markt auf dem Domplatz. Da "
                      "kaufen wir Käse und Obst für deine Reise."),
            ("Markus", "Und danach machen wir noch eine Wanderung?"),
            ("Sandy", "Dafür haben wir keine Zeit. Dein Zug fährt doch schon um zwei."),
        ],
        # Teil 3: five conversations, one file each, heard once.
        "teil3-1": [
            ("Anna", "Gespräch eins."),
            ("Sandy", "Nimmst du wieder die Pizza?"),
            ("Markus", "Nein, heute nicht. Ich hätte gern einen Salat."),
            ("Sandy", "Der Salat ist leider schon aus, tut mir leid."),
            ("Markus", "Schade. Dann nehme ich eben die Suppe."),
        ],
        "teil3-2": [
            ("Anna", "Gespräch zwei."),
            ("Reed", "Wie gefällt Ihnen dieser Rucksack?"),
            ("Shelley", "Der ist schön, aber zu groß für die Arbeit. Und für die Reise habe "
                        "ich schon einen Koffer. Haben Sie die schwarze Handtasche auch in "
                        "Braun?"),
            ("Reed", "Ja, hier ist sie."),
            ("Shelley", "Prima. Die nehme ich."),
        ],
        "teil3-3": [
            ("Anna", "Gespräch drei."),
            ("Sandy", "Guten Tag. Ich habe gestern im Zug nach Köln etwas liegen lassen."),
            ("Markus", "Einen Regenschirm? Davon haben wir hier sehr viele."),
            ("Sandy", "Nein, den habe ich hier. Und meinen Schlüssel habe ich zum Glück auch "
                      "wiedergefunden. Es ist meine Brille, in einem blauen Etui."),
            ("Markus", "Moment … ja, hier ist eine."),
        ],
        "teil3-4": [
            ("Anna", "Gespräch vier."),
            ("Markus", "Treffen wir uns um sieben vor dem Kino?"),
            ("Sandy", "Um sieben schaffe ich es nicht, ich arbeite bis halb sieben. Sagen wir "
                      "halb acht?"),
            ("Markus", "Der Film fängt um acht an. Gut, halb acht."),
        ],
        "teil3-5": [
            ("Anna", "Gespräch fünf."),
            ("Shelley", "Fährst du immer noch mit dem Auto ins Büro?"),
            ("Reed", "Nein, das Parken ist viel zu teuer. Eine Zeit lang bin ich mit dem Bus "
                     "gefahren, aber jetzt nehme ich das Fahrrad – das ist sogar schneller."),
        ],
        "teil4": [
            ("Anna", "Teil vier. Sie hören ein Interview. Sie hören den Text zweimal."),
            ("Reed", "Heute ist Lina Park bei uns im Studio. Frau Park, Sie sind in Korea "
                     "geboren, richtig?"),
            ("Sandy", "Nein, ich bin in Frankfurt geboren. Meine Eltern kommen aus Korea, sie "
                      "sind vor dreißig Jahren nach Deutschland gekommen."),
            ("Reed", "Sie arbeiten als Tierpflegerin im Tierpark. Wollten Sie das schon als "
                     "Kind werden?"),
            ("Sandy", "Oh ja! Wir hatten zu Hause immer Tiere, zwei Katzen und einen Hund. "
                      "Mit zwölf habe ich schon im Tierheim geholfen."),
            ("Reed", "Und wie sind Sie zum Tierpark gekommen?"),
            ("Sandy", "Nach der Schule habe ich zuerst Biologie studiert. Aber das war mir zu "
                      "theoretisch. Nach einem Jahr habe ich aufgehört. Ein Freund hat mir "
                      "dann von der Ausbildung im Tierpark erzählt, und ich habe mich sofort "
                      "beworben."),
            ("Reed", "Wie sieht Ihr Arbeitstag aus?"),
            ("Sandy", "Ich fange um sieben Uhr an. Zuerst mache ich die Ställe sauber, dann "
                      "bekommen die Tiere ihr Futter. Am Nachmittag erkläre ich Schulklassen, "
                      "wie wir mit den Tieren arbeiten. Das mache ich am liebsten."),
            ("Reed", "Arbeiten Sie auch am Wochenende?"),
            ("Sandy", "Ja, jedes zweite Wochenende. Die Tiere haben ja auch am Sonntag Hunger! "
                      "Dafür habe ich dann in der Woche frei."),
            ("Reed", "Und was sind Ihre Pläne für die Zukunft?"),
            ("Sandy", "Nächstes Jahr gehe ich für drei Monate nach Kanada, in einen Park für "
                      "Bären. Darauf freue ich mich sehr."),
            ("Reed", "Dann alles Gute, Frau Park, und vielen Dank für das Gespräch."),
            ("Sandy", "Gern."),
        ],
    },
    "b1": {
        # Teil 1: one file per text, so the player can replay each one on its own.
        "teil1-1": [
            ("Anna", "Text eins."),
            ("Markus", "Guten Tag, Herr Baum, hier ist das Autohaus Riedel. Ihr Wagen ist "
                       "fertig, allerdings erst morgen abholbereit, weil die Rechnung noch "
                       "geschrieben wird. Ab neun Uhr können Sie gerne vorbeikommen."),
        ],
        "teil1-2": [
            ("Anna", "Text zwei."),
            ("Sandy", "Liebe Gäste, wegen des Regens findet das Sommerfest heute nicht im Park "
                      "statt, sondern in der Aula der Schule. Die Turnhalle wird gerade "
                      "renoviert. Das Programm beginnt wie geplant um fünfzehn Uhr."),
        ],
        "teil1-3": [
            ("Anna", "Text drei."),
            ("Sandy", "Guten Tag, hier spricht Frau Ritter. Ich hatte mich vor zwei Wochen um "
                      "einen Praktikumsplatz bei Ihnen beworben und wollte fragen, ob meine "
                      "Unterlagen angekommen sind. Sie erreichen mich unter null eins sieben "
                      "sechs, vier vier drei, zwei eins null."),
        ],
        "teil1-4": [
            ("Anna", "Text vier."),
            ("Markus", "Volkshochschule Süd, Anmeldung. Der Kurs Fotografie für Anfänger ist "
                       "leider bereits voll. Sie können sich aber gern auf die Warteliste "
                       "setzen lassen – es wird fast immer noch ein Platz frei."),
        ],
        "teil1-5": [
            ("Anna", "Text fünf."),
            ("Sandy", "Und nun die Verkehrsmeldungen. Die Ringstraße ist wegen einer Baustelle "
                      "gesperrt, voraussichtlich zwei Wochen lang. Bitte fahren Sie über die "
                      "Uferstraße. Auf der A vier gibt es zurzeit keine Staus."),
        ],
        "teil2": [
            ("Anna", "Teil zwei. Sie hören einen Text. Sie hören den Text einmal."),
            ("Sandy", "Herzlich willkommen zu unserer Führung durch die Alte Tuchfabrik. Das "
                      "Gebäude, in dem wir stehen, war bis neunzehnhundertachtundsiebzig eine "
                      "Textilfabrik. Danach stand es fast dreißig Jahre leer.\n"
                      "Die Renovierung hat vier Jahre gedauert, deutlich länger als geplant, "
                      "vor allem wegen des Daches.\n"
                      "Heute finden Sie hier Büros und Ateliers, insgesamt vierzig Einheiten. "
                      "Ein Museum war am Anfang geplant, ließ sich aber nicht finanzieren.\n"
                      "Unsere Führung dauert insgesamt neunzig Minuten, mit einer kurzen Pause "
                      "nach etwa einer Stunde.\n"
                      "Und noch ein Hinweis: Fotografieren ist nur im Innenhof erlaubt, in den "
                      "Ateliers bitte nicht."),
        ],
        "teil3": [
            ("Anna", "Teil drei. Sie hören ein Gespräch. Sie hören das Gespräch einmal."),
            ("Markus", "Lena! Das ist ja eine Überraschung. Seit dem Studium haben wir uns "
                       "nicht mehr gesehen."),
            ("Sandy", "Markus! Stimmt, sieben Jahre. Ich habe letzten Monat eine neue Stelle "
                      "angefangen, bei einem Verlag hier in der Stadt."),
            ("Markus", "Und, wie ist es?"),
            ("Sandy", "Viel besser. Vorher bin ich jeden Tag eine Stunde gependelt, jetzt sind "
                      "es fünfzehn Minuten mit dem Rad. Und ich verdiene auch etwas mehr als "
                      "vorher."),
            ("Markus", "Und der Chef?"),
            ("Sandy", "Sehr angenehm, wirklich. Er lässt einen arbeiten. Ich überlege sogar, "
                      "nebenbei den Master zu machen – die Firma würde das unterstützen."),
            ("Markus", "Das klingt gut. Wollen wir nächste Woche mal einen Kaffee trinken?"),
            ("Sandy", "Gern. Donnerstag nach der Arbeit?"),
            ("Markus", "Donnerstag passt."),
        ],
        "teil4": [
            ("Anna", "Teil vier. Sie hören eine Diskussion. Sie hören die Diskussion zweimal."),
            ("Reed", "Guten Abend und willkommen bei Thema am Abend. Heute geht es um eine "
                     "Frage, die fast alle Familien betrifft: Brauchen Kinder Hausaufgaben? "
                     "Bei mir sind die Lehrerin Sabine Klein und der Vater Jonas Adler. Frau "
                     "Klein, Sie sind für Hausaufgaben?"),
            ("Sandy", "Ja, eindeutig. Was man nicht wiederholt, vergisst man innerhalb weniger "
                      "Tage. Hausaufgaben helfen den Kindern, den Stoff zu wiederholen."),
            ("Reed", "Herr Adler, Sie sehen das anders."),
            ("Markus", "Ganz anders. Kinder sitzen sechs Stunden in der Schule und sollen "
                       "danach weitermachen. Sie brauchen am Nachmittag mehr freie Zeit. "
                       "Ganztagsschulen, in denen alles in der Schule passiert, wären die "
                       "bessere Lösung."),
            ("Sandy", "Ein Problem sehe ich allerdings auch: Viele Eltern helfen zu viel. "
                      "Dann übt nicht das Kind, sondern die Mutter."),
            ("Reed", "Interessant ist übrigens, dass es in manchen Ländern kaum Hausaufgaben "
                     "gibt – und die Ergebnisse dort sind trotzdem gut."),
            ("Markus", "Genau. Und wenn vier Fächer am selben Tag Aufgaben geben, läuft etwas "
                       "falsch. Die Lehrkräfte sollten sich besser absprechen."),
            ("Sandy", "Das kann ich verstehen. Aber Hausaufgaben ganz abzuschaffen, wäre "
                      "falsch."),
            ("Reed", "Liebe Hörerinnen und Hörer, was meinen Sie? Rufen Sie uns an – die "
                     "Nummer finden Sie auf unserer Webseite."),
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
