"""Thin HTTP layer over the two OpenAI endpoints this feature needs.

Everything about the key lives here and in settings; nothing above this module
ever sees it, and it is never logged.
"""

import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TRANSCRIPTIONS_URL = "https://api.openai.com/v1/audio/transcriptions"
RESPONSES_URL = "https://api.openai.com/v1/responses"

TRANSCRIBE_TIMEOUT = 90
ANALYZE_TIMEOUT = 120


class OpenAIError(RuntimeError):
    """Raised for any failure that should surface as a controlled API error."""

    def __init__(self, message, *, status=None):
        super().__init__(message)
        self.message = message
        self.status = status


def _auth_headers():
    key = settings.OPENAI_API_KEY
    if not key:
        raise OpenAIError("The speaking teacher is not configured on this server.")
    return {"Authorization": f"Bearer {key}"}


def transcribe(audio_bytes, filename, *, language="de", mime="audio/webm"):
    """POST /v1/audio/transcriptions — speech to German text."""
    try:
        response = requests.post(
            TRANSCRIPTIONS_URL,
            headers=_auth_headers(),
            files={"file": (filename, audio_bytes, mime)},
            data={"model": settings.OPENAI_TRANSCRIPTION_MODEL, "language": language},
            timeout=TRANSCRIBE_TIMEOUT,
        )
    except requests.Timeout:
        raise OpenAIError("Transcription timed out.", status=504)
    except requests.RequestException:
        # Never echo the exception: it can contain the request headers.
        logger.warning("transcription request failed")
        raise OpenAIError("Could not reach the transcription service.", status=502)

    if response.status_code != 200:
        logger.warning("transcription rejected with status %s", response.status_code)
        raise OpenAIError("Unable to transcribe audio.", status=502)

    try:
        return (response.json().get("text") or "").strip()
    except json.JSONDecodeError:
        raise OpenAIError("Unable to transcribe audio.", status=502)


def respond_json(*, instructions, user_input, schema, schema_name="analysis"):
    """POST /v1/responses with a strict JSON schema; returns the parsed object."""
    payload = {
        "model": settings.OPENAI_TEXT_MODEL,
        "input": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_input},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            }
        },
    }

    try:
        response = requests.post(
            RESPONSES_URL,
            headers={**_auth_headers(), "Content-Type": "application/json"},
            json=payload,
            timeout=ANALYZE_TIMEOUT,
        )
    except requests.Timeout:
        raise OpenAIError("The analysis timed out.", status=504)
    except requests.RequestException:
        logger.warning("responses request failed")
        raise OpenAIError("Could not reach the analysis service.", status=502)

    if response.status_code != 200:
        logger.warning("responses rejected with status %s", response.status_code)
        raise OpenAIError("The analysis service returned an error.", status=502)

    body = response.json()
    if body.get("status") != "completed":
        raise OpenAIError("The analysis did not complete.", status=502)

    text = _extract_output_text(body)
    if not text:
        raise OpenAIError("The analysis returned no content.", status=502)

    try:
        return json.loads(text), body
    except json.JSONDecodeError:
        raise OpenAIError("The analysis returned malformed data.", status=502)


def _extract_output_text(body):
    """Pull the assistant text out of a Responses payload."""
    if body.get("output_text"):
        return body["output_text"]
    for item in body.get("output") or []:
        if item.get("type") != "message":
            continue
        for chunk in item.get("content") or []:
            if chunk.get("type") == "output_text" and chunk.get("text"):
                return chunk["text"]
    return ""
