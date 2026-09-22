"""How far each learner has come, summed across courses, lessons and exams.

One aggregation per collection, grouped by user, then merged in Python — the
back office list and the public podium both read from here, so the numbers
the admin ranks by are the numbers visitors see.
"""

from apps.courses.models import Enrollment
from apps.exams.models import ExamAttempt
from apps.learning.models import SpeakingAttempt, VideoProgress

EMPTY = {
    "courses": 0,
    "course_progress": 0,      # average percent across enrolled courses
    "lessons_done": 0,         # finished lesson videos
    "speaking_answers": 0,
    "speaking_score": 0,       # average AI score, 0–100
    "exams_taken": 0,          # finished, auto-scored modules
    "exams_passed": 0,
    "exam_score": 0,           # average percent
    "best_exam_score": 0,
    "last_active": None,
    "points": 0,
}


def _latest(*values):
    present = [value for value in values if value]
    return max(present) if present else None


def points(stats):
    """A single number to sort by. Deliberately simple, so it can be explained:

    each finished lesson 10, each passed exam module 25, plus the average exam
    score, the average speaking score and the average course progress.
    """
    return (
        stats["lessons_done"] * 10
        + stats["exams_passed"] * 25
        + stats["exam_score"]
        + stats["speaking_score"]
        + stats["course_progress"]
    )


def standings(user_ids=None):
    """{user_id (str): stats} for the given users, or for everyone active."""
    match = {"user": {"$in": list(user_ids)}} if user_ids is not None else {}
    out = {}

    def row(user_id):
        return out.setdefault(str(user_id), dict(EMPTY))

    for doc in Enrollment.objects.aggregate([
        {"$match": match},
        {"$group": {
            "_id": "$user",
            "courses": {"$sum": 1},
            "progress": {"$avg": "$progress"},
            "last": {"$max": "$last_activity"},
        }},
    ]):
        stats = row(doc["_id"])
        stats["courses"] = doc["courses"]
        stats["course_progress"] = round(doc["progress"] or 0)
        stats["last_active"] = _latest(stats["last_active"], doc["last"])

    for doc in VideoProgress.objects.aggregate([
        {"$match": {**match, "completed": True}},
        {"$group": {"_id": "$user", "done": {"$sum": 1}, "last": {"$max": "$updated_at"}}},
    ]):
        stats = row(doc["_id"])
        stats["lessons_done"] = doc["done"]
        stats["last_active"] = _latest(stats["last_active"], doc["last"])

    for doc in SpeakingAttempt.objects.aggregate([
        {"$match": {**match, "processing_status": "completed"}},
        {"$group": {
            "_id": "$user",
            "n": {"$sum": 1},
            "score": {"$avg": "$score"},
            "last": {"$max": "$created_at"},
        }},
    ]):
        stats = row(doc["_id"])
        stats["speaking_answers"] = doc["n"]
        stats["speaking_score"] = round(doc["score"] or 0)
        stats["last_active"] = _latest(stats["last_active"], doc["last"])

    # Writing modules are graded by a person later and carry max_score 0;
    # counting them would drag every average towards zero.
    for doc in ExamAttempt.objects.aggregate([
        {"$match": {**match, "status": "finished", "max_score": {"$gt": 0}}},
        {"$group": {
            "_id": "$user",
            "n": {"$sum": 1},
            "passed": {"$sum": {"$cond": ["$passed", 1, 0]}},
            "score": {"$avg": "$score"},
            "best": {"$max": "$score"},
            "last": {"$max": "$finished_at"},
        }},
    ]):
        stats = row(doc["_id"])
        stats["exams_taken"] = doc["n"]
        stats["exams_passed"] = doc["passed"]
        stats["exam_score"] = round(doc["score"] or 0)
        stats["best_exam_score"] = doc["best"] or 0
        stats["last_active"] = _latest(stats["last_active"], doc["last"])

    for stats in out.values():
        stats["points"] = points(stats)
    return out


def stats_for(user_id, table):
    return table.get(str(user_id)) or dict(EMPTY)


def podium(locale):
    """The learners staff placed on the podium, for the public site.

    Only what a visitor should see: a first name and last initial, never an
    email or phone number.
    """
    from apps.accounts.models import User
    from apps.core.i18n import t

    users = list(User.objects(showcase_rank__gt=0, is_active=True).order_by("showcase_rank"))
    table = standings([user.id for user in users]) if users else {}
    out = []
    for user in users:
        stats = stats_for(user.id, table)
        last = (user.last_name or "").strip()
        name = (user.first_name or "").strip()
        # never fall back to the email: its local part is often a real name
        display = f"{name} {last[:1]}." if name and last else name
        out.append({
            "rank": user.showcase_rank,
            "name": display,
            "avatar": user.avatar,
            "level": user.current_level,
            "city": user.city,
            "note": t(user.showcase_note, locale),
            "stats": {
                "lessons_done": stats["lessons_done"],
                "exams_passed": stats["exams_passed"],
                "exam_score": stats["exam_score"],
                "course_progress": stats["course_progress"],
            },
        })
    return out
