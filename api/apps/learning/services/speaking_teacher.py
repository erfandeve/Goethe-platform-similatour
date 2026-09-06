"""Turns a transcript into a validated teacher verdict."""

import logging

from django.conf import settings

from .openai_client import OpenAIError, respond_json
from .prompts import ANALYSIS_SCHEMA, PROMPT_VERSION, SYSTEM_PROMPT, compose

logger = logging.getLogger(__name__)

CATEGORY_KEYS = (
    "grammar",
    "vocabulary",
    "sentence_structure",
    "word_order",
    "naturalness",
    "relevance",
)
CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
MISTAKE_LIMIT = 8


def analyse(
    *,
    course_title,
    part_title,
    video_title,
    question,
    cefr,
    grammar_topics=None,
    vocabulary=None,
    expected_points=None,
    transcript,
    previous_attempts=None,
    feedback_language="fa",
):
    """Ask the model for a verdict, retrying only when the shape is unusable."""
    user_input = compose(
        course_title=course_title,
        part_title=part_title,
        video_title=video_title,
        question=question,
        cefr=cefr,
        grammar_topics=grammar_topics or [],
        vocabulary=vocabulary or [],
        expected_points=expected_points or [],
        transcript=transcript,
        previous_attempts=previous_attempts or [],
        feedback_language=feedback_language,
    )

    attempts = max(1, settings.AI_MAX_RETRIES + 1)
    last_error = None

    for attempt in range(attempts):
        try:
            data, raw = respond_json(
                instructions=SYSTEM_PROMPT,
                user_input=user_input,
                schema=ANALYSIS_SCHEMA,
                schema_name="german_speaking_analysis",
            )
        except OpenAIError as error:
            last_error = error
            # A transport failure is worth one more try; a config error is not.
            if error.status in (502, 504) and attempt + 1 < attempts:
                continue
            raise

        cleaned = validate(data)
        if cleaned:
            cleaned["prompt_version"] = PROMPT_VERSION
            return cleaned, raw

        logger.warning("analysis response failed validation (attempt %s)", attempt + 1)
        last_error = OpenAIError("The analysis returned malformed data.", status=502)

    raise last_error


def validate(data):
    """Never hand the client a shape it cannot render."""
    if not isinstance(data, dict):
        return None

    try:
        score = int(data.get("overall_score", 0))
    except (TypeError, ValueError):
        return None

    corrected = data.get("corrected_answer")
    summary = data.get("summary")
    if not isinstance(corrected, str) or not isinstance(summary, str):
        return None

    categories = data.get("categories")
    if not isinstance(categories, dict):
        return None

    raw_categories = {}
    for key in CATEGORY_KEYS:
        try:
            raw_categories[key] = max(0, int(categories.get(key, 0)))
        except (TypeError, ValueError):
            raw_categories[key] = 0

    # Strict JSON schema fixes the shape but not the range, and the model
    # sometimes answers on a 0–10 scale. Rescale rather than draw a broken chart.
    peak = max(raw_categories.values(), default=0)
    factor = 10 if peak and peak <= 10 and score > 10 else 1
    clean_categories = {
        key: min(100, value * factor) for key, value in raw_categories.items()
    }

    mistakes = []
    for item in data.get("mistakes") or []:
        if not isinstance(item, dict):
            continue
        mistakes.append(
            {
                "original": str(item.get("original", ""))[:500],
                "correction": str(item.get("correction", ""))[:500],
                "type": str(item.get("type", "grammar"))[:40],
                "explanation": str(item.get("explanation", ""))[:800],
            }
        )
        if len(mistakes) >= MISTAKE_LIMIT:
            break

    cefr = data.get("cefr_estimate")
    return {
        "overall_score": max(0, min(100, score)),
        "cefr_estimate": cefr if cefr in CEFR_LEVELS else "",
        "is_relevant": bool(data.get("is_relevant", True)),
        "summary": summary[:1000],
        "corrected_answer": corrected[:2000],
        "mistakes": mistakes,
        "categories": clean_categories,
        "positive_feedback": [str(x)[:400] for x in (data.get("positive_feedback") or [])][:6],
        "improvement_tips": [str(x)[:400] for x in (data.get("improvement_tips") or [])][:6],
        "next_action": "retry" if data.get("next_action") == "retry" else "continue",
    }
