import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.accounts.permissions import IsAuthenticated
from apps.core.exceptions import ApiError
from apps.core.utils import get_locale
from apps.courses.models import Enrollment

from .access import course_parts, require_course, require_video
from .models import AIAnalysis, LessonVideo, Mistake, Part, SpeakingAttempt, VideoProgress
from .serializers import attempt_item, part_item, video_item
from .services.openai_client import OpenAIError, transcribe
from .services.speaking_teacher import analyse

logger = logging.getLogger(__name__)

# Audio guard rails: a minute of speech never approaches this, so anything
# larger is either a bug or an abuse attempt.
MAX_AUDIO_BYTES = 12 * 1024 * 1024
MIN_AUDIO_BYTES = 1024
# Browsers label recordings inconsistently (Safari alone reports audio/mp4,
# audio/x-m4a and audio/mp4a-latm), so the type is a hint and the filename
# extension is the fallback. Only when neither is recognised do we refuse.
ALLOWED_AUDIO_SUFFIX = {
    "audio/webm": "webm",
    "video/webm": "webm",
    "audio/ogg": "ogg",
    "application/ogg": "ogg",
    "audio/mp4": "mp4",
    "audio/mp4a-latm": "mp4",
    "audio/x-m4a": "m4a",
    "audio/m4a": "m4a",
    "audio/aac": "m4a",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/wave": "wav",
    "audio/flac": "flac",
}
ALLOWED_AUDIO_EXTENSIONS = {"webm", "ogg", "oga", "mp4", "m4a", "mp3", "mpga", "wav", "flac"}
MIN_TRANSCRIPT_CHARS = 2
DUPLICATE_WINDOW_SECONDS = 8


# --------------------------------------------------------------- classroom ---


def _progress_map(user, course):
    return {
        str(record.video.id): record
        for record in VideoProgress.objects(user=user, course=course)
        if record.video
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def classroom(request, slug):
    """Everything the learning page needs for one course, in one request."""
    locale = get_locale(request)
    course = require_course(request.user, slug=slug)
    progress = _progress_map(request.user, course)

    parts = []
    total_videos = 0
    completed_videos = 0
    for part in course_parts(course):
        videos = list(part.videos)
        total_videos += len(videos)
        completed_videos += sum(
            1 for video in videos
            if (record := progress.get(str(video.id))) and record.completed
        )
        parts.append(part_item(part, locale, videos, progress))

    finished = [
        record for record in progress.values() if record.attempts and record.best_score
    ]
    average = round(sum(r.best_score for r in finished) / len(finished)) if finished else 0

    return Response(
        {
            "course": {
                "id": str(course.id),
                "slug": course.slug,
                "title": course.title.resolve(locale),
                "level": course.level,
                "accent": course.accent,
            },
            "parts": parts,
            "stats": {
                "total_videos": total_videos,
                "completed_videos": completed_videos,
                "speaking_attempts": SpeakingAttempt.objects(
                    user=request.user, course=course
                ).count(),
                "average_score": average,
                "percent": round(completed_videos / total_videos * 100) if total_videos else 0,
            },
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def course_parts_view(request, course_id):
    locale = get_locale(request)
    course = require_course(request.user, course_id=course_id)
    return Response(
        {"results": [part_item(part, locale) for part in course_parts(course)]}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def part_videos(request, part_id):
    locale = get_locale(request)
    part = Part.objects(id=part_id, is_published=True).first()
    if not part:
        raise ApiError("Part not found.", code="not_found", status_code=404)
    course = require_course(request.user, course_id=str(part.course.id))
    progress = _progress_map(request.user, course)
    return Response(
        {
            "results": [
                video_item(video, locale, progress.get(str(video.id)))
                for video in part.videos
            ]
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def progress_overview(request):
    records = VideoProgress.objects(user=request.user).order_by("-updated_at")[:100]
    return Response(
        {
            "results": [
                {
                    "course": str(r.course.id) if r.course else None,
                    "video": str(r.video.id) if r.video else None,
                    "position_seconds": r.position_seconds,
                    "completed": r.completed,
                    "best_score": r.best_score,
                    "attempts": r.attempts,
                }
                for r in records
            ]
        }
    )


def _progress_row(user, course, part, video):
    """Fetch-or-create atomically; two concurrent saves must not insert twice."""
    return VideoProgress.objects(user=user, video=video).modify(
        upsert=True,
        new=True,
        set_on_insert__user=user,
        set_on_insert__course=course,
        set_on_insert__part=part,
        set_on_insert__video=video,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_video_progress(request):
    data = request.data or {}
    video, part, course = require_video(request.user, data.get("video_id"))

    record = _progress_row(request.user, course, part, video)

    try:
        position = float(data.get("position_seconds", record.position_seconds))
        duration = float(data.get("duration_seconds", record.duration_seconds) or 0)
    except (TypeError, ValueError):
        raise ApiError("Position must be a number.", code="invalid")

    record.position_seconds = max(0.0, position)
    if duration:
        record.duration_seconds = duration
    record.watched_seconds = max(record.watched_seconds, record.position_seconds)

    if data.get("completed") and not record.completed:
        record.completed = True
        record.completed_at = datetime.utcnow()
    record.updated_at = datetime.utcnow()
    record.save()

    _touch_enrollment(request.user, course)
    return Response(
        {
            "position_seconds": record.position_seconds,
            "completed": record.completed,
            "course_percent": _course_percent(request.user, course),
        }
    )


def _touch_enrollment(user, course):
    """Keep the existing course progress in step with the classroom."""
    enrollment = Enrollment.objects(user=user, course=course).first()
    if not enrollment:
        return
    enrollment.last_activity = datetime.utcnow()
    enrollment.progress = _course_percent(user, course)
    enrollment.completed_lessons = VideoProgress.objects(
        user=user, course=course, completed=True
    ).count()
    enrollment.save()


def _course_percent(user, course):
    total = LessonVideo.objects(course=course, is_published=True).count()
    if not total:
        return 0
    done = VideoProgress.objects(user=user, course=course, completed=True).count()
    return round(done / total * 100)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_attempts(request):
    attempts = SpeakingAttempt.objects(user=request.user).order_by("-created_at")[:50]
    return Response({"results": [attempt_item(a) for a in attempts]})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def video_attempts(request, video_id):
    video, _, _ = require_video(request.user, video_id)
    attempts = SpeakingAttempt.objects(user=request.user, video=video).order_by("-created_at")[:20]
    return Response({"results": [attempt_item(a) for a in attempts]})


# ---------------------------------------------------------------------- AI ---


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def transcribe_view(request):
    """Browser audio in, German text out. The OpenAI key never leaves the server."""
    audio = request.FILES.get("audio")
    if not audio:
        raise ApiError("No audio was uploaded.", code="no_audio")

    size = audio.size or 0
    if size > MAX_AUDIO_BYTES:
        raise ApiError("The recording is too long.", code="audio_too_large", status_code=413)
    if size < MIN_AUDIO_BYTES:
        raise ApiError("The recording is too short.", code="audio_too_short")

    # A video id is optional here, but when present it must be one the learner owns.
    video_id = request.data.get("video_id")
    if video_id:
        require_video(request.user, video_id)

    mime = (audio.content_type or "audio/webm").split(";")[0].strip().lower()
    suffix = ALLOWED_AUDIO_SUFFIX.get(mime)
    if not suffix:
        extension = Path(audio.name or "").suffix.lstrip(".").lower()
        if extension in ALLOWED_AUDIO_EXTENSIONS:
            suffix = extension
        else:
            raise ApiError("This audio format is not supported.", code="audio_format")

    payload = audio.read()
    try:
        transcript = transcribe(
            payload,
            f"answer.{suffix}",
            language=(request.data.get("language") or "de")[:5],
            mime=mime,
        )
    except OpenAIError as error:
        return Response(
            {"success": False, "error": error.message},
            status=error.status or 502,
        )

    stored_path = ""
    if settings.STORE_AUDIO:
        stored_path = _store_audio(request.user, payload, suffix)

    return Response(
        {
            "success": True,
            "transcript": transcript,
            "audio_path": stored_path,
            "is_empty": len(transcript.strip()) < MIN_TRANSCRIPT_CHARS,
        }
    )


def _store_audio(user, payload, suffix):
    folder = Path(settings.MEDIA_ROOT) / "speaking" / str(user.id)
    folder.mkdir(parents=True, exist_ok=True)
    name = f"{uuid.uuid4().hex}.{suffix}"
    (folder / name).write_bytes(payload)
    return f"speaking/{user.id}/{name}"


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def analyze_view(request):
    """Grade a transcript against the lesson it belongs to."""
    locale = get_locale(request)
    data = request.data or {}
    transcript = (data.get("transcript") or "").strip()

    video, part, course = require_video(
        request.user,
        data.get("video_id"),
        course_id=data.get("course_id"),
        part_id=data.get("part_id"),
    )

    if not video.has_speaking_task:
        raise ApiError("This lesson has no speaking task.", code="no_task")

    # An empty transcript is not worth a model call.
    if len(transcript) < MIN_TRANSCRIPT_CHARS:
        return Response(
            {
                "success": False,
                "code": "empty_transcript",
                "error": "We could not understand your answer. Please try again.",
            },
            status=422,
        )
    if len(transcript) > 4000:
        transcript = transcript[:4000]

    recent = SpeakingAttempt.objects(
        user=request.user,
        video=video,
        created_at__gte=datetime.utcnow() - timedelta(seconds=DUPLICATE_WINDOW_SECONDS),
    ).order_by("-created_at").first()
    if recent and recent.transcript == transcript:
        # A double click or a re-render must not buy a second analysis.
        if recent.processing_status == "completed":
            return Response(
                {"success": True, "attempt": attempt_item(recent), "duplicate": True}
            )
        # The first request is still with the model; let the client keep waiting on it.
        return Response(
            {"success": False, "code": "in_progress", "error": "Analysis already running."},
            status=409,
        )

    question = video.question
    attempt = SpeakingAttempt(
        user=request.user,
        course=course,
        part=part,
        video=video,
        question_de=question.prompt_de,
        transcript=transcript,
        audio_path=(data.get("audio_path") or "")[:300],
        audio_seconds=float(data.get("audio_seconds") or 0),
        processing_status="analyzing",
    )
    attempt.save()

    history = [
        {"transcript": item.transcript, "score": item.score}
        for item in SpeakingAttempt.objects(
            user=request.user, video=video, processing_status="completed"
        ).order_by("-created_at")[:3]
    ]

    try:
        verdict, raw = analyse(
            course_title=course.title.de or course.title.en or course.slug,
            part_title=part.title_de or part.slug,
            video_title=video.scene_label or video.title_de or video.slug,
            question=question.prompt_de,
            cefr=video.cefr_level,
            grammar_topics=question.grammar_topics,
            vocabulary=question.vocabulary,
            expected_points=question.expected_points,
            transcript=transcript,
            previous_attempts=history,
            feedback_language=locale,
        )
    except OpenAIError as error:
        attempt.processing_status = "failed"
        attempt.error = error.message
        attempt.save()
        return Response(
            {"success": False, "error": error.message}, status=error.status or 502
        )

    analysis = AIAnalysis(
        speaking_attempt=attempt,
        overall_score=verdict["overall_score"],
        cefr_estimate=verdict["cefr_estimate"],
        is_relevant=verdict["is_relevant"],
        summary=verdict["summary"],
        corrected_answer=verdict["corrected_answer"],
        mistakes=[Mistake(**item) for item in verdict["mistakes"]],
        categories=verdict["categories"],
        positive_feedback=verdict["positive_feedback"],
        improvement_tips=verdict["improvement_tips"],
        next_action=verdict["next_action"],
        model=settings.OPENAI_TEXT_MODEL,
        raw_response={
            "id": raw.get("id"),
            "model": raw.get("model"),
            "usage": raw.get("usage"),
            "prompt_version": verdict.get("prompt_version"),
        },
    )
    analysis.save()

    attempt.score = verdict["overall_score"]
    attempt.cefr_estimate = verdict["cefr_estimate"]
    attempt.processing_status = "completed"
    attempt.save()

    _record_speaking_progress(request.user, course, part, video, verdict["overall_score"])

    return Response({"success": True, "attempt": attempt_item(attempt), "locale": locale})


def _record_speaking_progress(user, course, part, video, score):
    record = _progress_row(user, course, part, video)
    record.attempts += 1
    record.last_score = score
    record.best_score = max(record.best_score, score)
    record.speaking_done = True
    record.updated_at = datetime.utcnow()
    record.save()
    _touch_enrollment(user, course)
