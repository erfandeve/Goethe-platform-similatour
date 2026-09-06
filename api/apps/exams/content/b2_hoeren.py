"""Goethe-Zertifikat B2 · Modellsatz Erwachsene — module Hören (40 min, 30 points)."""

AUDIO_BASE = "/media/exams/b2/hoeren"

RF = [("richtig", "Richtig"), ("falsch", "Falsch")]

# --- Teil 1: five short recordings, two items each ---------------------------
# Odd items are richtig/falsch statements, even items are three-option questions.

TEIL1_TRACKS = [
    (f"{AUDIO_BASE}/teil1-1.m4a", "Aufgabe 1 und 2", [1, 2]),
    (f"{AUDIO_BASE}/teil1-2.m4a", "Aufgabe 3 und 4", [3, 4]),
    (f"{AUDIO_BASE}/teil1-3.m4a", "Aufgabe 5 und 6", [5, 6]),
    (f"{AUDIO_BASE}/teil1-4.m4a", "Aufgabe 7 und 8", [7, 8]),
    (f"{AUDIO_BASE}/teil1-5.m4a", "Aufgabe 9 und 10", [9, 10]),
]

TEIL1_ITEMS = [
    (1, "Die Frau spricht darüber, warum sie sich für Literatur interessiert.", RF, "richtig", 0),
    (2, "Welche Meinung hat die Frau über das Lesen?",
     [("a", "Zum Romanlesen braucht sie ihre Fantasie."),
      ("b", "Sie hat oft zu wenig Zeit, sich eigene Gedanken zu machen."),
      ("c", "Was sie gelesen hat, bleibt nicht lang im Gedächtnis.")], "a", 0),
    (3, "Die Frau berichtet über die Zahlungsmoral in vielen Ländern.", RF, "falsch", 1),
    (4, "Was wird immer seltener gemacht?",
     [("a", "Im Internet eingekauft."),
      ("b", "Geld gewechselt."),
      ("c", "Mit Bargeld bezahlt.")], "c", 1),
    (5, "Die Frau hat ein Praktikum bei einem Gericht gemacht.", RF, "falsch", 2),
    (6, "Die Frau fand ihre Aufgaben …",
     [("a", "wie zum Beispiel Kaffee kochen unangenehm."),
      ("b", "nützlich für ihr Studium."),
      ("c", "für ihre berufliche Tätigkeit sehr hilfreich.")], "b", 2),
    (7, "Der Mann berichtet über Sicherheit im Straßenverkehr.", RF, "richtig", 3),
    (8, "Nummernschilder bei Fahrrädern …",
     [("a", "lehnen Experten ab."),
      ("b", "halten Experten für eine gute Idee."),
      ("c", "möchten Experten ausprobieren.")], "a", 3),
    (9, "Die beiden Freunde unterhalten sich über einen Professor.", RF, "falsch", 4),
    (10, "Die beiden Freunde brauchen noch ein Thema für …",
     [("a", "eine Präsentation."),
      ("b", "einen Aufsatz."),
      ("c", "eine Seminararbeit.")], "a", 4),
]

# --- Teil 2: radio interview, heard twice ------------------------------------

TEIL2_ITEMS = [
    (11, "Frau Neuhaus findet es für unsere zukünftige Ernährung wichtig, …",
     [("a", "an die Konsequenzen unserer Entscheidung zu denken."),
      ("b", "uns mit Fleisch und Fisch zu ernähren."),
      ("c", "mehr Erbsen und Sojabohnen zu essen.")], "a"),
    (12, "Was ist die Ursache für wachsenden Fleischkonsum?",
     [("a", "Die Fleischproduktion ist gestiegen."),
      ("b", "Die Weltbevölkerung ist gewachsen."),
      ("c", "Mehr Menschen haben genug Geld für Fleisch.")], "c"),
    (13, "Warum sehen viele in Insekten eine Alternative zu Fleisch?",
     [("a", "Sie lassen sich gut zu Schokolade verarbeiten."),
      ("b", "Es gibt viele Zubereitungsarten."),
      ("c", "Sie schmecken wie Hähnchenfleisch.")], "b"),
    (14, "In einigen Ländern isst man heutzutage Insekten, weil …",
     [("a", "dort Viehbetriebe nicht rentabel sind."),
      ("b", "es dort schon länger üblich ist."),
      ("c", "es dort viele verschiedene Insekten gibt.")], "b"),
    (15, "Was ist der Vorteil einer Landwirtschaft in städtischen Gebieten?",
     [("a", "Der Wasserverbrauch sinkt."),
      ("b", "Man spart Strom."),
      ("c", "Sie ist für alle Nutzpflanzen geeignet.")], "a"),
    (16, "Was bedeutet „individualisierte Landwirtschaft“?",
     [("a", "Die Produktion passt sich an das einzelne Tier an."),
      ("b", "Computer zeigen an, wie viel Milch eine Kuh gegeben hat."),
      ("c", "Die Qualität der Milchprodukte steigt.")], "a"),
]

# --- Teil 3: panel discussion, heard once — "Wer sagt das?" ------------------

TEIL3_SPEAKERS = [
    ("a", "Moderator", ""),
    ("b", "Frau Gerster", "Studentin"),
    ("c", "Frau Lücke", "Seniorin"),
]

TEIL3_ITEMS = [
    (17, "Er/Sie lebt aus finanziellen Gründen mit anderen zusammen.", "b"),
    (18, "Eine WG-Wohnung sollte auch Raum zum Alleinsein bieten.", "b"),
    (19, "Es ist schön, Gesprächspartner in der Nähe zu haben.", "b"),
    (20, "Wohngemeinschaften für Menschen verschiedenen Alters sind neu.", "a"),
    (21, "Wohngemeinschaften können für die Bewohner nützlich sein.", "c"),
    (22, "Wohngemeinschaften sind für Senioren passender als für Studenten.", "b"),
]

# --- Teil 4: lecture, heard twice -------------------------------------------

TEIL4_ITEMS = [
    (23, "Es dauert mehr als 20 Minuten, …",
     [("a", "nach einer Störung umzuschalten."),
      ("b", "eine Aufgabe zu erledigen."),
      ("c", "sich in eine neue Aufgabe einzuarbeiten.")], "a"),
    (24, "Was meint Herr Kinigard mit „leeren Kalorien“?",
     [("a", "Inhaltslose Dinge."),
      ("b", "Informationen, die nicht relevant sind."),
      ("c", "Dinge, die sehr komplex sind.")], "b"),
    (25, "Der Versuch, konzentriert zu arbeiten, …",
     [("a", "ist erfolgversprechend."),
      ("b", "macht glücklich."),
      ("c", "strengt an.")], "c"),
    (26, "Mehrere Dinge gleichzeitig zu tun, …",
     [("a", "ändert nichts am Ergebnis."),
      ("b", "verbessert das Ergebnis."),
      ("c", "verschlechtert das Ergebnis.")], "c"),
    (27, "Ein externes Gedächtnis wird geschaffen, indem man …",
     [("a", "Dinge aufschreibt."),
      ("b", "sich auf andere Dinge konzentriert."),
      ("c", "den Kopf frei macht.")], "a"),
    (28, "Laut Herrn Kinigard sind gesetzliche Ruhepausen …",
     [("a", "unnötig."), ("b", "wichtig."), ("c", "zu stark reguliert.")], "b"),
    (29, "Wozu kann Zeitdruck führen? Zu …",
     [("a", "hervorragenden Ergebnissen."),
      ("b", "langen Blockaden."),
      ("c", "negativem Stress.")], "a"),
    (30, "Herr Kinigard rät dazu, …",
     [("a", "Ablenkungen zu vermeiden."),
      ("b", "auf Einflüsse von außen nicht zu reagieren."),
      ("c", "E-Mail-Korrespondenz zu reduzieren.")], "a"),
]
