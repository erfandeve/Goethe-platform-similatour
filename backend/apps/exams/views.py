from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.models import Notification
from apps.billing.models import active_perks
from apps.accounts.permissions import IsAuthenticated
from apps.core.exceptions import ApiError
from apps.core.pagination import paginate
from apps.core.utils import get_locale

from .models import Exam, ExamAccess, ExamAttempt, ExamCode, SectionResult
from .serializers import (
    attempt_item,
    code_item,
    attempt_review,
    exam_card,
    exam_detail,
    exam_modules,
    module_item,
    question_item,
)

CEFR_LADDER = ("A1", "A2", "B1", "B2", "C1")


@api_view(["GET"])
def exam_list(request):
    locale = get_locale(request)
    params = request.query_params
    qs = Exam.objects(is_published=True)

    if params.get("kind"):
        qs = qs.filter(kind__in=params["kind"].split(","))
    if params.get("level"):
        qs = qs.filter(level__in=params["level"].split(","))
    if params.get("free") == "true":
        qs = qs.filter(price=0)

    qs = qs.order_by("kind", "level")
    items, meta = paginate(qs, request, default_size=20)

    grouped = {"simulator": [], "frequent": []}
    for exam in items:
        grouped.setdefault(exam.kind, []).append(exam_card(exam, locale))

    return Response(
        {
            "results": [exam_card(e, locale) for e in items],
            "grouped": grouped,
            "meta": meta,
        }
    )


@api_view(["GET"])
def exam_detail_view(request, slug):
    locale = get_locale(request)
    exam = Exam.objects(slug=slug, is_published=True).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)
    data = exam_detail(exam, locale)
    data["format"] = exam.format
    data["modules"] = exam_modules(exam, locale)
    user = getattr(request, "user", None)
    data["has_access"] = bool(exam.is_free or (user and has_access(user, exam)))

    # Sittings the learner chooses between; the first one is covered by the
    # exam price, each extra one adds its own.
    owned_codes = (
        {access.exam_code for access in ExamAccess.objects(user=user, exam=str(exam.id))}
        if user
        else set()
    )
    unlocked_all = bool(user and {"exams", "exam_codes"} & active_perks(user))
    data["codes"] = [
        code_item(code, locale, owned=unlocked_all or str(code.id) in owned_codes)
        for code in ExamCode.objects(exam=exam, is_published=True).order_by("order")
    ]
    data["base_price"] = exam.effective_price
    if user:
        last = ExamAttempt.objects(user=user, exam=exam).order_by("-started_at").first()
        data["last_attempt"] = attempt_item(last, locale) if last else None
    return Response(data)


def has_access(user, exam, code=None):
    """A free exam, a subscription perk, or an actual purchase — in that order."""
    if exam.is_free:
        return True
    if not user:
        return False

    perks = active_perks(user)
    if "exams" in perks:
        return True
    if code is not None and "exam_codes" in perks:
        # The codes pass opens every sitting of an exam the learner can reach.
        return bool(ExamAccess.objects(user=user, exam=str(exam.id)).first())

    query = {"user": user, "exam": str(exam.id)}
    if ExamAccess.objects(**query, exam_code="").first():
        return True
    if code is not None:
        return bool(ExamAccess.objects(**query, exam_code=str(code.id)).first())
    return bool(ExamAccess.objects(**query).first())


def _paper_for(exam, code):
    """The modules a sitting actually uses.

    A code carries its own paper; until one is written it falls back to the
    exam's, so a freshly created code is still sittable.
    """
    return code.modules if (code and code.modules) else exam.modules


def _resolve_code(exam, code_id):
    """The requested sitting, checked against this exam."""
    if not code_id:
        return None
    code = ExamCode.objects(id=code_id, exam=exam, is_published=True).first()
    if not code:
        raise ApiError("Exam code not found.", status_code=404)
    return code


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_attempt(request, slug):
    locale = get_locale(request)
    exam = Exam.objects(slug=slug, is_published=True).first()
    if not exam:
        raise ApiError("Exam not found.", status_code=404)

    code = _resolve_code(exam, (request.data or {}).get("code"))
    if not has_access(request.user, exam, code=code):
        raise ApiError("Purchase this sitting to start it.", code="no_access", status_code=403)

    paper = _paper_for(exam, code)
    if paper:
        return start_module_attempt(request, exam, locale, code=code, paper=paper)

    attempt = ExamAttempt.objects(user=request.user, exam=exam, status="in_progress").first()
    if not attempt:
        attempt = ExamAttempt(user=request.user, exam=exam, max_score=exam.max_score)
        attempt.save()
        exam.attempts_count += 1
        exam.save()

    return Response(
        {
            "attempt": attempt_item(attempt, locale),
            "exam": exam_detail(exam, locale, with_questions=True),
        },
        status=201,
    )


def start_module_attempt(request, exam, locale, *, code=None, paper=None):
    """Open (or resume) an attempt at one module of a Goethe-format exam."""
    paper = paper if paper is not None else exam.modules
    skill = (request.data or {}).get("module") or paper[0].skill
    module = next((m for m in paper if m.skill == skill), None)
    if not module:
        raise ApiError("Unknown exam module.", status_code=404)
    if module.skill == "sprechen":
        raise ApiError("The speaking module is held with an examiner.", code="offline_module")

    # An unfinished attempt is only resumable on the same paper it was opened on.
    code_id = str(code.id) if code else ""
    attempt = ExamAttempt.objects(
        user=request.user, exam=exam, module=skill, exam_code=code_id, status="in_progress"
    ).first()
    if not attempt:
        attempt = ExamAttempt(
            user=request.user,
            exam=exam,
            module=skill,
            exam_code=code_id,
            max_score=module_max_points(module),
        )
        attempt.save()
        exam.attempts_count += 1
        exam.save()

    return Response(
        {
            "attempt": attempt_item(attempt, locale),
            "exam": {
                **exam_card(exam, locale),
                "format": "goethe",
                "duration_minutes": module.duration_minutes,
            },
            "module": module_item(module, locale, with_parts=True, with_answers=False),
        },
        status=201,
    )


def module_max_points(module):
    return sum(
        item.points
        for part in module.parts
        if part.part_type != "writing"
        for item in part.items
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_answers(request, pk):
    attempt = ExamAttempt.objects(id=pk, user=request.user).first()
    if not attempt:
        raise ApiError("Attempt not found.", status_code=404)
    if attempt.status != "in_progress":
        raise ApiError("This attempt is already finished.", code="finished")
    answers = (request.data or {}).get("answers") or {}
    attempt.answers.update(answers)
    attempt.save()
    return Response({"saved": len(attempt.answers)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_attempt(request, pk):
    locale = get_locale(request)
    attempt = ExamAttempt.objects(id=pk, user=request.user).first()
    if not attempt:
        raise ApiError("Attempt not found.", status_code=404)
    if attempt.status == "finished":
        return Response(attempt_review(attempt, locale))

    answers = (request.data or {}).get("answers")
    if answers:
        attempt.answers.update(answers)

    exam = attempt.exam
    code = ExamCode.objects(id=attempt.exam_code).first() if attempt.exam_code else None
    if _paper_for(exam, code):
        return submit_module_attempt(attempt, exam, locale, request.user)

    raw, maximum, correct = 0, 0, 0
    results = []

    for si, section in enumerate(exam.sections):
        s_raw, s_max = 0, 0
        for qi, question in enumerate(section.questions):
            if question.kind in ("essay", "audio_answer"):
                continue  # teacher-graded, excluded from the auto score entirely
            s_max += question.points
            given = attempt.answers.get(f"{si}:{qi}")
            if question.kind == "multiple":
                ok = sorted(given or []) == sorted(question.correct_indices)
            else:
                ok = given == question.correct_index
            if ok:
                s_raw += question.points
                correct += 1
        results.append(SectionResult(skill=section.skill, score=s_raw, max_score=s_max))
        raw += s_raw
        maximum += s_max

    percentage = round(raw / maximum * 100) if maximum else 0
    attempt.raw_score = raw
    attempt.max_score = maximum
    attempt.correct_count = correct
    attempt.score = percentage
    attempt.section_results = results
    attempt.passed = percentage >= exam.pass_score
    attempt.cefr_estimate = estimate_cefr(exam.level, percentage)
    attempt.status = "finished"
    attempt.finished_at = datetime.utcnow()
    attempt.duration_seconds = int((attempt.finished_at - attempt.started_at).total_seconds())
    attempt.save()

    if attempt.passed and CEFR_LADDER.index(exam.level) >= CEFR_LADDER.index(
        request.user.current_level
    ):
        request.user.current_level = exam.level
        request.user.save()

    Notification(
        user=request.user,
        title="Exam result is ready",
        body=f"You scored {percentage}% — estimated level {attempt.cefr_estimate}.",
        kind="exam",
        link=f"/dashboard/exams/{attempt.id}",
    ).save()

    return Response(attempt_review(attempt, locale))


def submit_module_attempt(attempt, exam, locale, user):
    """Grade one Goethe module: every item except free writing is auto-scored."""
    from .serializers import module_review

    code = ExamCode.objects(id=attempt.exam_code).first() if attempt.exam_code else None
    module = next((m for m in _paper_for(exam, code) if m.skill == attempt.module), None)
    if not module:
        raise ApiError("Unknown exam module.", status_code=404)

    raw, maximum, correct = 0, 0, 0
    for part_index, part in enumerate(module.parts):
        if part.part_type == "writing":
            continue
        for item in part.items:
            maximum += item.points
            given = attempt.answers.get(f"{module.skill}:{part_index}:{item.number}")
            if given is not None and str(given) == item.answer:
                raw += item.points
                correct += 1

    percentage = round(raw / maximum * 100) if maximum else 0
    attempt.raw_score = raw
    attempt.max_score = maximum
    attempt.correct_count = correct
    attempt.score = percentage
    attempt.section_results = [
        SectionResult(skill=SKILL_ALIASES.get(module.skill, "reading"), score=raw, max_score=maximum)
    ]
    attempt.passed = percentage >= exam.pass_score
    attempt.cefr_estimate = estimate_cefr(exam.level, percentage)
    attempt.status = "finished"
    attempt.finished_at = datetime.utcnow()
    attempt.duration_seconds = int((attempt.finished_at - attempt.started_at).total_seconds())
    attempt.save()

    Notification(
        user=user,
        title=f"{module.title.de or module.skill.title()} — Ergebnis",
        body=f"{percentage}% ({raw}/{maximum}) · {attempt.cefr_estimate}",
        kind="exam",
        link="/dashboard/exams",
    ).save()

    return Response(
        {
            **attempt_item(attempt, locale),
            "module": module.skill,
            "review": module_review(module, attempt.answers, locale),
        }
    )


# The learner-facing modules keep their German names; the stored SectionResult
# reuses the platform's existing skill vocabulary.
SKILL_ALIASES = {
    "lesen": "reading",
    "hoeren": "listening",
    "schreiben": "writing",
    "sprechen": "speaking",
}


def estimate_cefr(exam_level, percentage):
    index = CEFR_LADDER.index(exam_level)
    if percentage >= 85:
        return CEFR_LADDER[min(index + 1, len(CEFR_LADDER) - 1)]
    if percentage >= 60:
        return exam_level
    return CEFR_LADDER[max(index - 1, 0)]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_attempts(request):
    locale = get_locale(request)
    qs = ExamAttempt.objects(user=request.user).order_by("-started_at")
    items, meta = paginate(qs, request, default_size=12)
    return Response({"results": [attempt_item(a, locale) for a in items], "meta": meta})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def attempt_detail(request, pk):
    locale = get_locale(request)
    attempt = ExamAttempt.objects(id=pk, user=request.user).first()
    if not attempt:
        raise ApiError("Attempt not found.", status_code=404)
    exam = attempt.exam
    code = ExamCode.objects(id=attempt.exam_code).first() if attempt.exam_code else None
    paper = _paper_for(exam, code)
    if paper:
        from .serializers import module_review

        module = next((m for m in paper if m.skill == attempt.module), None)
        return Response(
            {
                **attempt_item(attempt, locale),
                "module": attempt.module,
                "review": module_review(module, attempt.answers, locale)
                if module and attempt.status == "finished"
                else [],
            }
        )

    if attempt.status != "finished":
        return Response(
            {
                "attempt": attempt_item(attempt, locale),
                "questions": [
                    question_item(q, locale, si, qi)
                    for si, s in enumerate(exam.sections)
                    for qi, q in enumerate(s.questions)
                ],
            }
        )
    return Response(attempt_review(attempt, locale))
