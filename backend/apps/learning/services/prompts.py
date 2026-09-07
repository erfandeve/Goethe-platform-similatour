"""The teacher's brief and the shape of its verdict.

Kept on the server and versioned here so the persona can be tuned without
touching the client or the API contract.
"""

PROMPT_VERSION = "speaking-teacher/2026-09-02"

SYSTEM_PROMPT = """\
Du bist eine erfahrene, freundliche Deutschlehrerin und bewertest die gesprochene \
Antwort einer lernenden Person. Die Antwort wurde automatisch transkribiert, kleine \
Transkriptionsfehler sind daher möglich.

Bewertungsgrundsätze:
- Bewerte IMMER relativ zum angegebenen GER-Niveau. Von A1/A2 erwartest du einfache, \
kurze Sätze; erst ab B2 erwartest du komplexe Strukturen, Konnektoren und Präzision.
- Eine grammatisch korrekte Alternativformulierung ist KEIN Fehler. Unterscheide klar \
zwischen echtem Grammatikfehler, stilistischer Verbesserung, unnatürlicher aber \
verständlicher Formulierung und reinem Wortschatzvorschlag.
- Prüfe: Grammatik, Satzbau, Wortstellung, Verbkonjugation, Verbposition, Artikel, \
Kasus, Präpositionen, Tempora, Wortschatz, Wortwahl, Natürlichkeit, Bezug zur Frage \
und kommunikative Qualität.
- Sehr kurze Antworten sind nicht automatisch falsch. Wenn die Frage kurz beantwortet \
werden kann, bewerte den Inhalt und schlage höflich eine Erweiterung vor.
- Ist die Antwort thematisch unpassend, setze is_relevant auf false, erkläre es \
freundlich und bewerte die sprachliche Leistung trotzdem fair.
- Sei konstruktiv und ermutigend. Nenne höchstens die fünf wichtigsten Fehler.
- Alle Rückmeldungen auf Deutsch, in einfacher Sprache passend zum Niveau.

Bewertung 0–100: 90+ ausgezeichnet, 80–89 sehr gut, 70–79 gut, 60–69 ausbaufähig, \
unter 60 deutlich ausbaufähig. Sei nicht künstlich streng.
WICHTIG: Auch ALLE Werte in "categories" sind Ganzzahlen auf der Skala 0–100 \
(z. B. 75, nicht 7,5 und nicht 7). Verwende niemals eine 0–10-Skala.

corrected_answer ist die verbesserte, natürliche Fassung der Antwort. Ist die Antwort \
bereits korrekt, wiederhole sie unverändert.

SPRACHE DER RÜCKMELDUNG — sehr wichtig:
- Deutsch bleibt Deutsch: "corrected_answer" sowie "original" und "correction" \
in jedem Fehler sind IMMER auf Deutsch.
- ALLE erklärenden Texte schreibst du dagegen in der Sprache, die unten unter \
FEEDBACK-SPRACHE steht: "summary", "explanation" jedes Fehlers, \
"positive_feedback" und "improvement_tips".
- Ist die Feedback-Sprache Persisch, schreibe diese Texte VOLLSTÄNDIG und flüssig \
auf Persisch (فارسی). Nur einzelne deutsche Wörter oder kurze Zitate dürfen in \
lateinischer Schrift stehen, z. B. «فعل gehen با sein صرف می‌شود». Schreibe \
niemals ganze Sätze oder Nebensätze auf Deutsch mitten in einem persischen Text.

Antworte ausschließlich mit dem geforderten JSON-Objekt."""


ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "cefr_estimate": {"type": "string", "enum": ["A1", "A2", "B1", "B2", "C1", "C2"]},
        "is_relevant": {"type": "boolean"},
        "summary": {"type": "string"},
        "corrected_answer": {"type": "string"},
        "mistakes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "original": {"type": "string"},
                    "correction": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": [
                            "grammar",
                            "word_order",
                            "case",
                            "preposition",
                            "article",
                            "verb",
                            "tense",
                            "vocabulary",
                            "style",
                            "pronunciation",
                        ],
                    },
                    "explanation": {"type": "string"},
                },
                "required": ["original", "correction", "type", "explanation"],
                "additionalProperties": False,
            },
        },
        "categories": {
            "type": "object",
            "properties": {
                "grammar": {"type": "integer", "minimum": 0, "maximum": 100},
                "vocabulary": {"type": "integer", "minimum": 0, "maximum": 100},
                "sentence_structure": {"type": "integer", "minimum": 0, "maximum": 100},
                "word_order": {"type": "integer", "minimum": 0, "maximum": 100},
                "naturalness": {"type": "integer", "minimum": 0, "maximum": 100},
                "relevance": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": [
                "grammar",
                "vocabulary",
                "sentence_structure",
                "word_order",
                "naturalness",
                "relevance",
            ],
            "additionalProperties": False,
        },
        "positive_feedback": {"type": "array", "items": {"type": "string"}},
        "improvement_tips": {"type": "array", "items": {"type": "string"}},
        "next_action": {"type": "string", "enum": ["retry", "continue"]},
    },
    "required": [
        "overall_score",
        "cefr_estimate",
        "is_relevant",
        "summary",
        "corrected_answer",
        "mistakes",
        "categories",
        "positive_feedback",
        "improvement_tips",
        "next_action",
    ],
    "additionalProperties": False,
}


FEEDBACK_LANGUAGES = {
    "fa": "Persisch (فارسی)",
    "de": "Deutsch",
    "en": "Englisch",
}


def compose(*, course_title, part_title, video_title, question, cefr, grammar_topics,
            vocabulary, expected_points, transcript, previous_attempts,
            feedback_language="fa"):
    """Render the user message for one evaluation."""
    parts = [
        f"FEEDBACK-SPRACHE:\n{FEEDBACK_LANGUAGES.get(feedback_language, FEEDBACK_LANGUAGES['fa'])}",
        f"KURS:\n{course_title}",
        f"TEIL:\n{part_title}",
        f"VIDEO:\n{video_title}",
        f"FRAGE:\n{question}",
        f"NIVEAU (GER):\n{cefr}",
    ]
    if grammar_topics:
        parts.append("GRAMMATIKTHEMEN:\n" + ", ".join(grammar_topics))
    if vocabulary:
        parts.append("WORTSCHATZ:\n" + ", ".join(vocabulary))
    if expected_points:
        parts.append("ERWARTETE INHALTSPUNKTE:\n- " + "\n- ".join(expected_points))
    parts.append(f"ANTWORT DER LERNENDEN PERSON (Transkript):\n{transcript}")

    if previous_attempts:
        history = "\n".join(
            f"- Versuch {index + 1}: {item.get('transcript', '')[:300]} "
            f"(Punkte: {item.get('score', '—')})"
            for index, item in enumerate(previous_attempts[-3:])
        )
        parts.append(f"FRÜHERE VERSUCHE:\n{history}")

    return "\n\n".join(parts)
