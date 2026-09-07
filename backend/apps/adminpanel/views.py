"""Back-office API.

Every endpoint is staff-only and re-derives ownership from the database; the
client's ids are inputs, never authority. Deletes refuse to run when learners
would lose data behind them.
"""

import logging
import re
import uuid
from datetime import datetime
from pathlib import Path

from django.conf import settings
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.accounts.models import User
from apps.accounts.permissions import IsStaff
from apps.core.exceptions import ApiError
from apps.core.i18n import TranslatedText
from apps.core.utils import slugify
from apps.courses.models import Category, Course, Enrollment, Instructor
from apps.learning.models import (
    LessonVideo,
    Part,
    Question,
    SpeakingAttempt,
    VideoProgress,
)

from .serializers import (
    category_row,
    course_detail,
    course_row,
    instructor_row,
    part_row,
    read_translated,
    video_row,
)

logger = logging.getLogger(__name__)

MAX_VIDEO_BYTES = 512 * 1024 * 1024
VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "m4v"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024
IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "avif"}
LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")


# ------------------------------------------------------------------ helpers ---


def _int(payload, key, default=0):
    try:
        return int(payload.get(key, default))
    except (TypeError, ValueError):
        raise ApiError(f"'{key}' must be a number.", code="invalid")


def _string_list(payload, key, current=None):
    value = payload.get(key)
    if value is None:
        return current if current is not None else []
    if isinstance(value, str):
        value = [line.strip() for line in value.splitlines()]
    if not isinstance(value, list):
        raise ApiError(f"'{key}' must be a list.", code="invalid")
    return [str(item).strip() for item in value if str(item).strip()]


def _unique_slug(model, base, *, current_id=None, **scope):
    """Slugs are part of public URLs, so collisions get a numeric suffix."""
    candidate = slugify(base) or "item"
    index = 2
    while True:
        existing = model.objects(slug=candidate, **scope).first()
        if not existing or str(existing.id) == str(current_id):
            return candidate
        candidate = f"{slugify(base)}-{index}"
        index += 1


def _title_seed(payload, fallback):
    title = payload.get("title") or {}
    if isinstance(title, dict):
        for key in ("en", "de", "fa"):
            if title.get(key):
                return title[key]
    return payload.get("title_de") or payload.get("name") or fallback


# ----------------------------------------------------------------- overview ---


@api_view(["GET"])
@permission_classes([IsStaff])
def overview(request):
    courses = Course.objects()
    return Response(
        {
            "courses": {
                "total": courses.count(),
                "published": Course.objects(is_published=True).count(),
            },
            "categories": Category.objects.count(),
            "instructors": Instructor.objects.count(),
            "parts": Part.objects.count(),
            "videos": LessonVideo.objects.count(),
            "speaking_videos": LessonVideo.objects(question__exists=True).count(),
            "students": User.objects(is_staff=False).count(),
            "enrollments": Enrollment.objects.count(),
            "speaking_attempts": SpeakingAttempt.objects.count(),
        }
    )


# --------------------------------------------------------------- categories ---


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def categories(request):
    if request.method == "POST":
        payload = request.data or {}
        kind = payload.get("kind", "course")
        if kind not in ("course", "podcast"):
            raise ApiError("Unknown category kind.", code="invalid")

        category = Category(
            kind=kind,
            slug=_unique_slug(Category, payload.get("slug") or _title_seed(payload, "category"), kind=kind),
            title=read_translated(payload.get("title")),
            description=read_translated(payload.get("description")),
            icon=(payload.get("icon") or "layers")[:40],
            color=(payload.get("color") or "#6d5efc")[:9],
            order=_int(payload, "order", Category.objects(kind=kind).count()),
        )
        category.save()
        return Response(category_row(category), status=201)

    kind = request.query_params.get("kind")
    query = Category.objects(kind=kind) if kind else Category.objects()
    return Response(
        {
            "results": [
                category_row(item, Course.objects(category=item).count())
                for item in query.order_by("kind", "order")
            ]
        }
    )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def category_detail(request, pk):
    category = Category.objects(id=pk).first()
    if not category:
        raise ApiError("Category not found.", status_code=404)

    if request.method == "DELETE":
        used = Course.objects(category=category).count()
        if used:
            raise ApiError(
                f"{used} course(s) still use this category.", code="in_use", status_code=409
            )
        category.delete()
        return Response(status=204)

    payload = request.data or {}
    if "title" in payload:
        category.title = read_translated(payload["title"], category.title)
    if "description" in payload:
        category.description = read_translated(payload["description"], category.description)
    if payload.get("slug"):
        category.slug = _unique_slug(
            Category, payload["slug"], current_id=category.id, kind=category.kind
        )
    for field in ("icon", "color"):
        if field in payload:
            setattr(category, field, str(payload[field])[:40])
    if "order" in payload:
        category.order = _int(payload, "order", category.order)
    category.save()
    return Response(category_row(category, Course.objects(category=category).count()))


# -------------------------------------------------------------- instructors ---


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def instructors(request):
    if request.method == "POST":
        payload = request.data or {}
        name = (payload.get("name") or "").strip()
        if not name:
            raise ApiError("A name is required.", fields={"name": "Required."})
        instructor = Instructor(
            slug=_unique_slug(Instructor, payload.get("slug") or name),
            name=name,
            avatar=(payload.get("avatar") or "")[:300],
            headline=read_translated(payload.get("headline")),
            bio=read_translated(payload.get("bio")),
            languages=_string_list(payload, "languages", ["de"]),
            is_featured=bool(payload.get("is_featured", False)),
        )
        instructor.save()
        return Response(instructor_row(instructor), status=201)

    return Response(
        {"results": [instructor_row(item) for item in Instructor.objects.order_by("name")]}
    )


# ------------------------------------------------------------------ courses ---


def _counts(course):
    return (
        Part.objects(course=course).count(),
        LessonVideo.objects(course=course).count(),
    )


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def courses(request):
    if request.method == "POST":
        payload = request.data or {}
        course = Course(slug=_unique_slug(Course, payload.get("slug") or _title_seed(payload, "course")))
        _apply_course(course, payload)
        course.save()
        return Response(course_detail(course, parts=0, videos=0), status=201)

    search = (request.query_params.get("q") or "").strip().lower()
    rows = []
    for course in Course.objects().order_by("-created_at"):
        if search and search not in (
            f"{course.slug} {course.title.fa} {course.title.en} {course.title.de}".lower()
        ):
            continue
        parts, videos = _counts(course)
        rows.append(course_row(course, parts=parts, videos=videos))
    return Response({"results": rows})


def _apply_course(course, payload):
    if "title" in payload:
        course.title = read_translated(payload["title"], course.title)
    if "subtitle" in payload:
        course.subtitle = read_translated(payload["subtitle"], course.subtitle)
    if "description" in payload:
        course.description = read_translated(payload["description"], course.description)

    if "category" in payload:
        course.category = Category.objects(id=payload["category"]).first() if payload["category"] else None
    if "instructor" in payload:
        course.instructor = (
            Instructor.objects(id=payload["instructor"]).first() if payload["instructor"] else None
        )

    if payload.get("level") in LEVELS:
        course.level = payload["level"]
    for field in ("language", "format", "accent", "cover"):
        if field in payload:
            setattr(course, field, str(payload[field])[:300])
    for field in ("price", "discount_price", "duration_minutes", "sessions_count"):
        if field in payload:
            setattr(course, field, max(0, _int(payload, field, getattr(course, field))))
    for field in ("is_published", "is_featured", "is_bestseller"):
        if field in payload:
            setattr(course, field, bool(payload[field]))

    if "tags" in payload:
        course.tags = _string_list(payload, "tags", course.tags)
    for field in ("outcomes", "requirements"):
        if field in payload:
            items = payload[field]
            if not isinstance(items, list):
                raise ApiError(f"'{field}' must be a list.", code="invalid")
            setattr(course, field, [read_translated(item) for item in items])


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def course_detail_view(request, pk):
    course = Course.objects(id=pk).first()
    if not course:
        raise ApiError("Course not found.", status_code=404)

    if request.method == "DELETE":
        enrolled = Enrollment.objects(course=course).count()
        if enrolled:
            raise ApiError(
                f"{enrolled} learner(s) are enrolled; unpublish it instead.",
                code="in_use",
                status_code=409,
            )
        LessonVideo.objects(course=course).delete()
        Part.objects(course=course).delete()
        course.delete()
        return Response(status=204)

    if request.method == "PATCH":
        payload = request.data or {}
        if payload.get("slug"):
            course.slug = _unique_slug(Course, payload["slug"], current_id=course.id)
        _apply_course(course, payload)
        course.save()

    parts, videos = _counts(course)
    return Response(course_detail(course, parts=parts, videos=videos))


# -------------------------------------------------------------------- parts ---


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def course_parts(request, pk):
    course = Course.objects(id=pk).first()
    if not course:
        raise ApiError("Course not found.", status_code=404)

    if request.method == "POST":
        payload = request.data or {}
        part = Part(
            course=course,
            slug=_unique_slug(Part, payload.get("slug") or _title_seed(payload, "part"), course=course),
            order=_int(payload, "order", Part.objects(course=course).count() + 1),
            title=read_translated(payload.get("title")),
            title_de=(payload.get("title_de") or "")[:200],
            description=read_translated(payload.get("description")),
            is_published=bool(payload.get("is_published", True)),
        )
        part.save()
        return Response(part_row(part, []), status=201)

    rows = []
    for part in Part.objects(course=course).order_by("order"):
        videos = LessonVideo.objects(part=part).order_by("order")
        rows.append(part_row(part, list(videos)))
    parts_count, videos_count = _counts(course)
    return Response(
        {
            "course": course_detail(course, parts=parts_count, videos=videos_count),
            "results": rows,
        }
    )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def part_detail(request, pk):
    part = Part.objects(id=pk).first()
    if not part:
        raise ApiError("Part not found.", status_code=404)

    if request.method == "DELETE":
        videos = LessonVideo.objects(part=part).count()
        if videos:
            raise ApiError(
                f"Remove the {videos} lesson(s) in this part first.",
                code="in_use",
                status_code=409,
            )
        part.delete()
        return Response(status=204)

    payload = request.data or {}
    if "title" in payload:
        part.title = read_translated(payload["title"], part.title)
    if "description" in payload:
        part.description = read_translated(payload["description"], part.description)
    if "title_de" in payload:
        part.title_de = str(payload["title_de"])[:200]
    if payload.get("slug"):
        part.slug = _unique_slug(Part, payload["slug"], current_id=part.id, course=part.course)
    if "order" in payload:
        part.order = _int(payload, "order", part.order)
    if "is_published" in payload:
        part.is_published = bool(payload["is_published"])
    part.save()
    return Response(part_row(part, list(LessonVideo.objects(part=part).order_by("order"))))


@api_view(["POST"])
@permission_classes([IsStaff])
def reorder_parts(request):
    for position, part_id in enumerate((request.data or {}).get("ids") or [], start=1):
        Part.objects(id=part_id).update_one(set__order=position)
    return Response({"ok": True})


# ------------------------------------------------------------------- videos ---


@api_view(["POST"])
@permission_classes([IsStaff])
def part_videos(request, pk):
    part = Part.objects(id=pk).first()
    if not part:
        raise ApiError("Part not found.", status_code=404)

    payload = request.data or {}
    video_url = (payload.get("video_url") or "").strip()
    if not video_url:
        raise ApiError("Upload a video file first.", fields={"video_url": "Required."})

    video = LessonVideo(
        course=part.course,
        part=part,
        slug=_unique_slug(
            LessonVideo, payload.get("slug") or _title_seed(payload, "lesson")
        ),
        order=_int(payload, "order", LessonVideo.objects(part=part).count() + 1),
        video_url=video_url,
    )
    _apply_video(video, payload)
    video.save()
    return Response(video_row(video), status=201)


def _apply_video(video, payload):
    if "title" in payload:
        video.title = read_translated(payload["title"], video.title)
    if "description" in payload:
        video.description = read_translated(payload["description"], video.description)
    for field in ("title_de", "scene_label"):
        if field in payload:
            setattr(video, field, str(payload[field])[:250])
    # A lesson always keeps a video, but its poster may be cleared.
    if payload.get("video_url"):
        video.video_url = str(payload["video_url"])[:500]
    if "poster_url" in payload:
        video.poster_url = str(payload["poster_url"] or "")[:500]
    if "duration_seconds" in payload:
        video.duration_seconds = max(0, _int(payload, "duration_seconds", video.duration_seconds))
    if payload.get("cefr_level") in LEVELS:
        video.cefr_level = payload["cefr_level"]
    if "is_published" in payload:
        video.is_published = bool(payload["is_published"])

    # The speaking prompt is what the AI teacher grades against.
    if "question" in payload:
        question = payload["question"]
        if not question or not (question.get("prompt_de") or "").strip():
            video.question = None
        else:
            current = video.question or Question(prompt_de="")
            video.question = Question(
                prompt_de=question["prompt_de"].strip()[:600],
                prompt=read_translated(question.get("prompt"), current.prompt),
                hint=read_translated(question.get("hint"), current.hint),
                expected_points=_string_list(question, "expected_points", current.expected_points),
                grammar_topics=_string_list(question, "grammar_topics", current.grammar_topics),
                vocabulary=_string_list(question, "vocabulary", current.vocabulary),
                min_words=max(1, int(question.get("min_words") or current.min_words or 2)),
            )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def video_detail(request, pk):
    video = LessonVideo.objects(id=pk).first()
    if not video:
        raise ApiError("Lesson not found.", status_code=404)

    if request.method == "DELETE":
        # Learner history outlives the lesson, so refuse rather than orphan it.
        attempts = SpeakingAttempt.objects(video=video).count()
        if attempts:
            raise ApiError(
                f"{attempts} speaking attempt(s) reference this lesson; unpublish it instead.",
                code="in_use",
                status_code=409,
            )
        VideoProgress.objects(video=video).delete()
        video.delete()
        return Response(status=204)

    payload = request.data or {}
    if payload.get("slug"):
        video.slug = _unique_slug(LessonVideo, payload["slug"], current_id=video.id)
    if payload.get("part"):
        target = Part.objects(id=payload["part"], course=video.course).first()
        if not target:
            raise ApiError("That part belongs to another course.", code="mismatch")
        video.part = target
    if "order" in payload:
        video.order = _int(payload, "order", video.order)
    _apply_video(video, payload)
    video.save()
    return Response(video_row(video))


@api_view(["POST"])
@permission_classes([IsStaff])
def reorder_videos(request):
    for position, video_id in enumerate((request.data or {}).get("ids") or [], start=1):
        LessonVideo.objects(id=video_id).update_one(set__order=position)
    return Response({"ok": True})


# ------------------------------------------------------------------ uploads ---


@api_view(["POST"])
@permission_classes([IsStaff])
@parser_classes([MultiPartParser])
def upload_video(request):
    """Store a lesson video under MEDIA_ROOT and hand back its public path."""
    upload = request.FILES.get("file")
    if not upload:
        raise ApiError("No file was uploaded.", code="no_file")
    if (upload.size or 0) > MAX_VIDEO_BYTES:
        raise ApiError("The file is larger than 512 MB.", code="too_large", status_code=413)

    extension = Path(upload.name or "").suffix.lstrip(".").lower()
    if extension not in VIDEO_EXTENSIONS:
        raise ApiError("Use an MP4, WebM or MOV file.", code="bad_format")

    course_slug = slugify(request.data.get("course_slug") or "library")
    folder = Path(settings.MEDIA_ROOT) / "courses" / course_slug / "videos"
    folder.mkdir(parents=True, exist_ok=True)

    stem = slugify(Path(upload.name).stem)[:60] or "lesson"
    name = f"{stem}-{uuid.uuid4().hex[:8]}.{extension}"
    with open(folder / name, "wb") as handle:
        for chunk in upload.chunks():
            handle.write(chunk)

    url = f"/media/courses/{course_slug}/videos/{name}"
    return Response(
        {"url": url, "duration_seconds": _mp4_duration(folder / name), "size": upload.size},
        status=201,
    )


@api_view(["POST"])
@permission_classes([IsStaff])
@parser_classes([MultiPartParser])
def upload_image(request):
    """Store a cover image and hand back its public path.

    `folder` groups uploads (courses, exams, podcasts…) so the media directory
    stays browsable; it is slugified, never taken as a raw path.
    """
    upload = request.FILES.get("file")
    if not upload:
        raise ApiError("No file was uploaded.", code="no_file")
    if (upload.size or 0) > MAX_IMAGE_BYTES:
        raise ApiError("The image is larger than 8 MB.", code="too_large", status_code=413)

    extension = Path(upload.name or "").suffix.lstrip(".").lower()
    if extension == "jpeg":
        extension = "jpg"
    if extension not in IMAGE_EXTENSIONS:
        raise ApiError("Use a JPG, PNG, WebP or AVIF image.", code="bad_format")

    group = slugify(request.data.get("folder") or "covers")
    folder = Path(settings.MEDIA_ROOT) / "covers" / group
    folder.mkdir(parents=True, exist_ok=True)

    stem = slugify(Path(upload.name).stem)[:60] or "cover"
    name = f"{stem}-{uuid.uuid4().hex[:8]}.{extension}"
    with open(folder / name, "wb") as handle:
        for chunk in upload.chunks():
            handle.write(chunk)

    return Response({"url": f"/media/covers/{group}/{name}", "size": upload.size}, status=201)


def _mp4_duration(path):
    """Read the mvhd atom so the editor can prefill the length without ffmpeg."""
    import struct

    try:
        data = path.read_bytes()
    except OSError:
        return 0
    index = data.find(b"mvhd")
    if index < 0:
        return 0
    head = index + 4
    try:
        version = data[head]
        if version == 1:
            timescale, duration = struct.unpack(">IQ", data[head + 20 : head + 32])
        else:
            timescale, duration = struct.unpack(">II", data[head + 12 : head + 20])
        return round(duration / timescale) if timescale else 0
    except (struct.error, IndexError):
        return 0


# -------------------------------------------------------------------- exams ---

from apps.exams.models import (
    AudioTrack,  # noqa: E402  (kept beside the exam endpoints)
    Exam,
    ExamAttempt,
    ExamItem,
    ExamModule,
    ExamOption,
    ExamPart,
    StimulusBlock,
)

from .serializers import exam_detail, exam_row  # noqa: E402

EXAM_KINDS = ("simulator", "frequent")
PART_TYPES = (
    "match_person",
    "gap_drag",
    "mcq",
    "match_heading",
    "match_paragraph",
    "listening_mixed",
    "writing",
)
MODULE_SKILLS = ("lesen", "hoeren", "schreiben", "sprechen")


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def exams(request):
    if request.method == "POST":
        payload = request.data or {}
        exam = Exam(slug=_unique_slug(Exam, payload.get("slug") or _title_seed(payload, "exam")))
        _apply_exam(exam, payload)
        exam.save()
        return Response(exam_detail(exam), status=201)

    return Response(
        {"results": [exam_row(exam) for exam in Exam.objects().order_by("kind", "level")]}
    )


def _apply_exam(exam, payload):
    for field in ("title", "subtitle", "description"):
        if field in payload:
            setattr(exam, field, read_translated(payload[field], getattr(exam, field)))
    if payload.get("level") in LEVELS:
        exam.level = payload["level"]
    if payload.get("kind") in EXAM_KINDS:
        exam.kind = payload["kind"]
    for field in ("exam_board", "accent", "badge", "cover"):
        if field in payload:
            setattr(exam, field, str(payload[field])[:200])
    for field in ("duration_minutes", "pass_score", "price", "discount_price"):
        if field in payload:
            setattr(exam, field, max(0, _int(payload, field, getattr(exam, field))))
    for field in ("is_published", "is_featured"):
        if field in payload:
            setattr(exam, field, bool(payload[field]))
    if "highlights" in payload and isinstance(payload["highlights"], list):
        exam.highlights = [read_translated(item) for item in payload["highlights"]]


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def exam_detail_view(request, pk):
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)

    if request.method == "DELETE":
        attempts = ExamAttempt.objects(exam=exam).count()
        if attempts:
            raise ApiError(
                f"{attempts} attempt(s) reference this exam; unpublish it instead.",
                code="in_use",
                status_code=409,
            )
        exam.delete()
        return Response(status=204)

    if request.method == "PATCH":
        payload = request.data or {}
        if payload.get("slug"):
            exam.slug = _unique_slug(Exam, payload["slug"], current_id=exam.id)
        _apply_exam(exam, payload)
        exam.save()

    return Response(exam_detail(exam))


def _module_at(exam, index):
    try:
        return exam.modules[int(index)]
    except (IndexError, ValueError, TypeError):
        raise ApiError("Module not found.", status_code=404)


def _part_at(module, index):
    try:
        return module.parts[int(index)]
    except (IndexError, ValueError, TypeError):
        raise ApiError("Part not found.", status_code=404)


@api_view(["POST"])
@permission_classes([IsStaff])
def exam_modules(request, pk):
    """Add a module (Lesen, Hören, …) to an exam."""
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)

    payload = request.data or {}
    skill = payload.get("skill")
    if skill not in MODULE_SKILLS:
        raise ApiError("Unknown module.", code="invalid")
    if any(module.skill == skill for module in exam.modules):
        raise ApiError("That module already exists.", code="duplicate", status_code=409)

    exam.modules.append(
        ExamModule(
            skill=skill,
            title=read_translated(payload.get("title")),
            intro=read_translated(payload.get("intro")),
            duration_minutes=max(1, _int(payload, "duration_minutes", 60)),
            max_points=max(0, _int(payload, "max_points", 30)),
        )
    )
    exam.save()
    return Response(exam_detail(exam), status=201)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def exam_module_detail(request, pk, index):
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)
    module = _module_at(exam, index)

    if request.method == "DELETE":
        exam.modules.remove(module)
        exam.save()
        return Response(exam_detail(exam))

    payload = request.data or {}
    for field in ("title", "intro"):
        if field in payload:
            setattr(module, field, read_translated(payload[field], getattr(module, field)))
    for field in ("duration_minutes", "max_points"):
        if field in payload:
            setattr(module, field, max(0, _int(payload, field, getattr(module, field))))
    exam.save()
    return Response(exam_detail(exam))


@api_view(["POST"])
@permission_classes([IsStaff])
def exam_parts(request, pk, index):
    """Add a Teil to a module."""
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)
    module = _module_at(exam, index)

    payload = request.data or {}
    part_type = payload.get("type", "mcq")
    if part_type not in PART_TYPES:
        raise ApiError("Unknown task type.", code="invalid")

    module.parts.append(
        ExamPart(
            number=_int(payload, "number", len(module.parts) + 1),
            part_type=part_type,
            title=read_translated(payload.get("title")),
            instructions=read_translated(payload.get("instructions")),
            work_minutes=max(1, _int(payload, "work_minutes", 10)),
        )
    )
    exam.save()
    return Response(exam_detail(exam), status=201)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def exam_part_detail(request, pk, index, part_index):
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)
    module = _module_at(exam, index)
    part = _part_at(module, part_index)

    if request.method == "DELETE":
        module.parts.remove(part)
        exam.save()
        return Response(exam_detail(exam))

    payload = request.data or {}
    for field in ("title", "instructions"):
        if field in payload:
            setattr(part, field, read_translated(payload[field], getattr(part, field)))
    for field in ("stimulus_title", "stimulus_subtitle", "stimulus_intro",
                  "example_prompt", "example_answer"):
        if field in payload:
            setattr(part, field, str(payload[field])[:4000])
    if "work_minutes" in payload:
        part.work_minutes = max(1, _int(payload, "work_minutes", part.work_minutes))
    if payload.get("type") in PART_TYPES:
        part.part_type = payload["type"]

    # Shared option pool, used by the matching task types.
    if "options" in payload and isinstance(payload["options"], list):
        part.options = [
            ExamOption(
                key=str(option.get("key", ""))[:20],
                label=str(option.get("label", ""))[:200],
                text=str(option.get("text", ""))[:2000],
                author=str(option.get("author", ""))[:200],
            )
            for option in payload["options"]
            if str(option.get("key", "")).strip()
        ]

    if "blocks" in payload and isinstance(payload["blocks"], list):
        part.blocks = [
            StimulusBlock(
                kind=str(block.get("kind", "paragraph"))[:20],
                label=str(block.get("label", ""))[:40],
                title=str(block.get("title", ""))[:200],
                text=str(block.get("text", ""))[:8000],
                author=str(block.get("author", ""))[:200],
            )
            for block in payload["blocks"]
        ]

    # Listening tracks: which file, how often it may be heard, and how long the
    # learner reads before it starts.
    if "audio" in payload and isinstance(payload["audio"], list):
        part.audio = [
            AudioTrack(
                label=str(track.get("label", ""))[:120],
                url=str(track.get("url", ""))[:400],
                plays=max(1, min(3, int(track.get("plays") or 1))),
                pre_read_seconds=max(0, min(300, int(track.get("pre_read_seconds") or 0))),
                covers=[int(n) for n in (track.get("covers") or []) if str(n).strip().isdigit()],
            )
            for track in payload["audio"]
            if str(track.get("url", "")).strip()
        ]

    if "min_words" in payload:
        value = payload["min_words"]
        part.min_words = max(0, _int(payload, "min_words", 0)) if value not in (None, "") else None

    exam.save()
    return Response(exam_detail(exam))


@api_view(["PUT"])
@permission_classes([IsStaff])
def exam_items(request, pk, index, part_index):
    """Replace the question list of one Teil, answer keys included."""
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)
    module = _module_at(exam, index)
    part = _part_at(module, part_index)

    incoming = (request.data or {}).get("items")
    if not isinstance(incoming, list):
        raise ApiError("'items' must be a list.", code="invalid")

    items = []
    for position, raw in enumerate(incoming, start=1):
        options = [
            ExamOption(
                key=str(option.get("key", ""))[:20],
                label=str(option.get("label", ""))[:200],
                text=str(option.get("text", ""))[:2000],
            )
            for option in (raw.get("options") or [])
            if str(option.get("key", "")).strip()
        ]
        answer = str(raw.get("answer", "")).strip()

        # An answer that matches no option would be unscoreable.
        pool = {option.key for option in (options or part.options)}
        if answer and pool and answer not in pool:
            raise ApiError(
                f"Question {raw.get('number', position)}: the answer key is not one of the options.",
                code="invalid_answer",
            )

        items.append(
            ExamItem(
                number=_int(raw, "number", position),
                prompt=str(raw.get("prompt", ""))[:2000],
                options=options,
                answer=answer,
                points=max(0, _int(raw, "points", 1)),
                audio_index=raw.get("audio_index"),
                explanation=read_translated(raw.get("explanation")),
            )
        )

    part.items = items
    exam.save()
    return Response(exam_detail(exam))


# ----------------------------------------------------------------- podcasts ---

from apps.podcasts.models import (  # noqa: E402  (kept beside the podcast endpoints)
    Bookmark,
    Episode,
    ListenProgress,
    Podcast,
    TranscriptLine,
    VocabItem,
)

from .serializers import episode_row, podcast_row  # noqa: E402

AUDIO_EXTENSIONS = {"mp3", "m4a", "wav", "ogg", "webm", "aac"}
MAX_AUDIO_UPLOAD_BYTES = 128 * 1024 * 1024


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def podcasts(request):
    if request.method == "POST":
        payload = request.data or {}
        podcast = Podcast(
            slug=_unique_slug(Podcast, payload.get("slug") or _title_seed(payload, "podcast"))
        )
        _apply_podcast(podcast, payload)
        podcast.save()
        return Response(podcast_row(podcast, 0), status=201)

    rows = [
        podcast_row(item, Episode.objects(podcast=item).count())
        for item in Podcast.objects().order_by("-is_featured", "slug")
    ]
    return Response({"results": rows})


def _apply_podcast(podcast, payload):
    for field in ("title", "tagline", "description"):
        if field in payload:
            setattr(podcast, field, read_translated(payload[field], getattr(podcast, field)))
    if "category" in payload:
        podcast.category = (
            Category.objects(id=payload["category"]).first() if payload["category"] else None
        )
    for field in ("cover", "accent", "host_name", "host_avatar", "language"):
        if field in payload:
            setattr(podcast, field, str(payload[field])[:300])
    if payload.get("level") in LEVELS:
        podcast.level = payload["level"]
    if "tags" in payload:
        podcast.tags = _string_list(payload, "tags", podcast.tags)
    for field in ("is_published", "is_featured"):
        if field in payload:
            setattr(podcast, field, bool(payload[field]))


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def podcast_detail(request, pk):
    podcast = Podcast.objects(id=pk).first()
    if not podcast:
        raise ApiError("Podcast not found.", status_code=404)

    if request.method == "DELETE":
        episodes = Episode.objects(podcast=podcast).count()
        if episodes:
            raise ApiError(
                f"Remove the {episodes} episode(s) first.", code="in_use", status_code=409
            )
        podcast.delete()
        return Response(status=204)

    if request.method == "PATCH":
        payload = request.data or {}
        if payload.get("slug"):
            podcast.slug = _unique_slug(Podcast, payload["slug"], current_id=podcast.id)
        _apply_podcast(podcast, payload)
        podcast.save()

    return Response(podcast_row(podcast, Episode.objects(podcast=podcast).count()))


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def podcast_episodes(request, pk):
    podcast = Podcast.objects(id=pk).first()
    if not podcast:
        raise ApiError("Podcast not found.", status_code=404)

    if request.method == "POST":
        payload = request.data or {}
        if not (payload.get("audio_url") or "").strip():
            raise ApiError("Upload an audio file first.", fields={"audio_url": "Required."})

        episode = Episode(
            podcast=podcast,
            slug=_unique_slug(
                Episode, payload.get("slug") or _title_seed(payload, f"{podcast.slug}-episode")
            ),
            number=_int(payload, "number", Episode.objects(podcast=podcast).count() + 1),
            audio_url=str(payload["audio_url"])[:500],
        )
        _apply_episode(episode, payload)
        episode.save()
        return Response(episode_row(episode), status=201)

    episodes = Episode.objects(podcast=podcast).order_by("number")
    return Response(
        {
            "podcast": podcast_row(podcast, episodes.count()),
            "results": [episode_row(episode) for episode in episodes],
        }
    )


def _apply_episode(episode, payload):
    for field in ("title", "description"):
        if field in payload:
            setattr(episode, field, read_translated(payload[field], getattr(episode, field)))
    if payload.get("audio_url"):
        episode.audio_url = str(payload["audio_url"])[:500]
    if "cover" in payload:
        episode.cover = str(payload["cover"] or "")[:500]
    if "duration_seconds" in payload:
        episode.duration_seconds = max(0, _int(payload, "duration_seconds", episode.duration_seconds))
    if payload.get("level") in LEVELS:
        episode.level = payload["level"]
    for field in ("is_premium", "is_published"):
        if field in payload:
            setattr(episode, field, bool(payload[field]))

    # The transcript drives the synced reader, so it is replaced wholesale.
    if "transcript" in payload and isinstance(payload["transcript"], list):
        episode.transcript = [
            TranscriptLine(
                start=float(line.get("start") or 0),
                end=float(line.get("end") or 0),
                speaker=str(line.get("speaker", ""))[:80],
                text=str(line.get("text", ""))[:2000],
                translation=read_translated(line.get("translation")),
            )
            for line in payload["transcript"]
            if str(line.get("text", "")).strip()
        ]

    if "vocabulary" in payload and isinstance(payload["vocabulary"], list):
        episode.vocabulary = [
            VocabItem(
                term=str(item.get("term", ""))[:120],
                article=str(item.get("article", ""))[:10],
                meaning=read_translated(item.get("meaning")),
                example=str(item.get("example", ""))[:500],
            )
            for item in payload["vocabulary"]
            if str(item.get("term", "")).strip()
        ]


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def episode_detail(request, pk):
    episode = Episode.objects(id=pk).first()
    if not episode:
        raise ApiError("Episode not found.", status_code=404)

    if request.method == "DELETE":
        ListenProgress.objects(episode=episode).delete()
        Bookmark.objects(episode=episode).delete()
        episode.delete()
        return Response(status=204)

    payload = request.data or {}
    if payload.get("slug"):
        episode.slug = _unique_slug(Episode, payload["slug"], current_id=episode.id)
    if "number" in payload:
        episode.number = _int(payload, "number", episode.number)
    _apply_episode(episode, payload)
    episode.save()
    return Response(episode_row(episode))


@api_view(["POST"])
@permission_classes([IsStaff])
@parser_classes([MultiPartParser])
def upload_audio(request):
    """Store an episode's audio and hand back its public path."""
    upload = request.FILES.get("file")
    if not upload:
        raise ApiError("No file was uploaded.", code="no_file")
    if (upload.size or 0) > MAX_AUDIO_UPLOAD_BYTES:
        raise ApiError("The file is larger than 128 MB.", code="too_large", status_code=413)

    extension = Path(upload.name or "").suffix.lstrip(".").lower()
    if extension not in AUDIO_EXTENSIONS:
        raise ApiError("Use an MP3, M4A, WAV or OGG file.", code="bad_format")

    group = slugify(request.data.get("folder") or "library")
    folder = Path(settings.MEDIA_ROOT) / "podcasts" / "audio" / group
    folder.mkdir(parents=True, exist_ok=True)

    stem = slugify(Path(upload.name).stem)[:60] or "episode"
    name = f"{stem}-{uuid.uuid4().hex[:8]}.{extension}"
    with open(folder / name, "wb") as handle:
        for chunk in upload.chunks():
            handle.write(chunk)

    return Response(
        {"url": f"/media/podcasts/audio/{group}/{name}", "size": upload.size}, status=201
    )


# ------------------------------------------------------------- exam codes ---

from apps.exams.models import ExamCode  # noqa: E402


def _code_row(code):
    return {
        "id": str(code.id),
        "code": code.code,
        "label": translated(code.label),
        "description": translated(code.description),
        "order": code.order,
        "extra_price": code.extra_price,
        "is_published": code.is_published,
        "items_count": code.items_count,
        "modules": [exam_module_row(m, i) for i, m in enumerate(code.modules)],
        "exam": str(code.exam.id) if code.exam else None,
    }


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def exam_codes(request, pk):
    """The sittings of one exam. Each carries its own question set."""
    exam = Exam.objects(id=pk).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)

    if request.method == "POST":
        payload = request.data or {}
        name = (payload.get("code") or "").strip()
        if not name:
            raise ApiError("A code is required.", fields={"code": "Required."})
        if ExamCode.objects(exam=exam, code=name).first():
            raise ApiError("That code already exists for this exam.", code="duplicate",
                           status_code=409)

        code = ExamCode(
            exam=exam,
            code=name[:60],
            label=read_translated(payload.get("label")),
            description=read_translated(payload.get("description")),
            order=_int(payload, "order", ExamCode.objects(exam=exam).count() + 1),
            extra_price=max(0, _int(payload, "extra_price", 0)),
            is_published=bool(payload.get("is_published", True)),
        )
        code.save()
        return Response(_code_row(code), status=201)

    codes = ExamCode.objects(exam=exam).order_by("order")
    return Response({"exam": exam_row(exam), "results": [_code_row(c) for c in codes]})


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def exam_code_detail(request, pk):
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)

    if request.method == "DELETE":
        taken = ExamAttempt.objects(exam_code=str(code.id)).count()
        if taken:
            raise ApiError(
                f"{taken} attempt(s) used this code; unpublish it instead.",
                code="in_use",
                status_code=409,
            )
        code.delete()
        return Response(status=204)

    if request.method == "PATCH":
        payload = request.data or {}
        if payload.get("code"):
            name = str(payload["code"]).strip()[:60]
            clash = ExamCode.objects(exam=code.exam, code=name).first()
            if clash and str(clash.id) != str(code.id):
                raise ApiError("That code already exists.", code="duplicate", status_code=409)
            code.code = name
        for field in ("label", "description"):
            if field in payload:
                setattr(code, field, read_translated(payload[field], getattr(code, field)))
        if "order" in payload:
            code.order = _int(payload, "order", code.order)
        if "extra_price" in payload:
            code.extra_price = max(0, _int(payload, "extra_price", code.extra_price))
        if "is_published" in payload:
            code.is_published = bool(payload["is_published"])
        code.save()

    return Response(_code_row(code))


def _code_module_at(code, index):
    try:
        return code.modules[int(index)]
    except (IndexError, ValueError, TypeError):
        raise ApiError("Module not found.", status_code=404)


@api_view(["POST"])
@permission_classes([IsStaff])
def exam_code_modules(request, pk):
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)

    payload = request.data or {}
    skill = payload.get("skill")
    if skill not in MODULE_SKILLS:
        raise ApiError("Unknown module.", code="invalid")
    if any(module.skill == skill for module in code.modules):
        raise ApiError("That module already exists.", code="duplicate", status_code=409)

    code.modules.append(
        ExamModule(
            skill=skill,
            title=read_translated(payload.get("title")),
            duration_minutes=max(1, _int(payload, "duration_minutes", 60)),
            max_points=max(0, _int(payload, "max_points", 30)),
        )
    )
    code.save()
    return Response(_code_row(code), status=201)


@api_view(["DELETE"])
@permission_classes([IsStaff])
def exam_code_module_detail(request, pk, index):
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)
    code.modules.remove(_code_module_at(code, index))
    code.save()
    return Response(_code_row(code))


@api_view(["POST"])
@permission_classes([IsStaff])
def exam_code_parts(request, pk, index):
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)
    module = _code_module_at(code, index)

    payload = request.data or {}
    part_type = payload.get("type", "mcq")
    if part_type not in PART_TYPES:
        raise ApiError("Unknown task type.", code="invalid")

    module.parts.append(
        ExamPart(
            number=_int(payload, "number", len(module.parts) + 1),
            part_type=part_type,
            title=read_translated(payload.get("title")),
            instructions=read_translated(payload.get("instructions")),
            work_minutes=max(1, _int(payload, "work_minutes", 10)),
        )
    )
    code.save()
    return Response(_code_row(code), status=201)


@api_view(["DELETE"])
@permission_classes([IsStaff])
def exam_code_part_detail(request, pk, index, part_index):
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)
    module = _code_module_at(code, index)
    try:
        module.parts.pop(int(part_index))
    except (IndexError, ValueError):
        raise ApiError("Part not found.", status_code=404)
    code.save()
    return Response(_code_row(code))


@api_view(["PUT"])
@permission_classes([IsStaff])
def exam_code_items(request, pk, index, part_index):
    """Replace the questions of one Teil inside a code's paper."""
    code = ExamCode.objects(id=pk).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)
    module = _code_module_at(code, index)
    try:
        part = module.parts[int(part_index)]
    except (IndexError, ValueError):
        raise ApiError("Part not found.", status_code=404)

    part.items = _build_items((request.data or {}).get("items"), part)
    code.save()
    return Response(_code_row(code))


def _build_items(incoming, part):
    """Shared question builder: validates that every answer names a real option."""
    if not isinstance(incoming, list):
        raise ApiError("'items' must be a list.", code="invalid")

    items = []
    for position, raw in enumerate(incoming, start=1):
        options = [
            ExamOption(
                key=str(option.get("key", ""))[:20],
                label=str(option.get("label", ""))[:200],
                text=str(option.get("text", ""))[:2000],
            )
            for option in (raw.get("options") or [])
            if str(option.get("key", "")).strip()
        ]
        answer = str(raw.get("answer", "")).strip()
        pool = {option.key for option in (options or part.options)}
        if answer and pool and answer not in pool:
            raise ApiError(
                f"Question {raw.get('number', position)}: the answer key is not one of the options.",
                code="invalid_answer",
            )
        items.append(
            ExamItem(
                number=_int(raw, "number", position),
                prompt=str(raw.get("prompt", ""))[:2000],
                options=options,
                answer=answer,
                points=max(0, _int(raw, "points", 1)),
                audio_index=raw.get("audio_index"),
                explanation=read_translated(raw.get("explanation")),
            )
        )
    return items


# --------------------------------------------------------------- plans ---

from apps.billing.models import PERKS, Plan, Subscription  # noqa: E402


def _plan_row(plan):
    return {
        "id": str(plan.id),
        "slug": plan.slug,
        "title": translated(plan.title),
        "description": translated(plan.description),
        "highlights": [translated(item) for item in plan.highlights],
        "perks": plan.perks,
        "price": plan.price,
        "duration_days": plan.duration_days,
        "accent": plan.accent,
        "badge": plan.badge,
        "order": plan.order,
        "is_published": plan.is_published,
        "is_featured": plan.is_featured,
        "subscribers": Subscription.objects(plan=plan, is_active=True).count(),
    }


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def plans(request):
    if request.method == "POST":
        payload = request.data or {}
        plan = Plan(slug=_unique_slug(Plan, payload.get("slug") or _title_seed(payload, "plan")))
        _apply_plan(plan, payload)
        plan.save()
        return Response(_plan_row(plan), status=201)

    return Response(
        {
            "results": [_plan_row(plan) for plan in Plan.objects().order_by("order")],
            "perks": list(PERKS),
        }
    )


def _apply_plan(plan, payload):
    for field in ("title", "description"):
        if field in payload:
            setattr(plan, field, read_translated(payload[field], getattr(plan, field)))
    if "perks" in payload and isinstance(payload["perks"], list):
        plan.perks = [perk for perk in payload["perks"] if perk in PERKS]
    if "highlights" in payload and isinstance(payload["highlights"], list):
        plan.highlights = [read_translated(item) for item in payload["highlights"]]
    for field in ("price", "duration_days", "order"):
        if field in payload:
            setattr(plan, field, max(0, _int(payload, field, getattr(plan, field))))
    for field in ("accent", "badge"):
        if field in payload:
            setattr(plan, field, str(payload[field])[:60])
    for field in ("is_published", "is_featured"):
        if field in payload:
            setattr(plan, field, bool(payload[field]))


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def plan_detail(request, pk):
    plan = Plan.objects(id=pk).first()
    if not plan:
        raise ApiError("Plan not found.", status_code=404)

    if request.method == "DELETE":
        active = Subscription.objects(plan=plan, is_active=True).count()
        if active:
            raise ApiError(
                f"{active} learner(s) are on this plan; unpublish it instead.",
                code="in_use",
                status_code=409,
            )
        plan.delete()
        return Response(status=204)

    payload = request.data or {}
    if payload.get("slug"):
        plan.slug = _unique_slug(Plan, payload["slug"], current_id=plan.id)
    _apply_plan(plan, payload)
    plan.save()
    return Response(_plan_row(plan))
