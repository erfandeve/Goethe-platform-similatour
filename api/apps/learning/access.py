"""Server-side authorisation for the classroom.

The client sends ids; none of them are trusted. Every lookup re-derives the
course from the database and checks the learner actually owns it.
"""

from apps.billing.models import active_perks
from apps.core.exceptions import ApiError
from apps.courses.models import Course, Enrollment

from .models import LessonVideo, Part


def require_course(user, *, slug=None, course_id=None):
    course = None
    if slug:
        course = Course.objects(slug=slug, is_published=True).first()
    elif course_id:
        course = Course.objects(id=course_id, is_published=True).first()
    if not course:
        raise ApiError("Course not found.", code="not_found", status_code=404)

    if Enrollment.objects(user=user, course=course).first():
        return course

    # A subscription stands in for an enrolment while it is valid.
    perks = active_perks(user)
    if "courses" in perks or ("speaking" in perks and _has_speaking(course)):
        return course

    raise ApiError(
        "You do not have access to this course.", code="no_access", status_code=403
    )


def _has_speaking(course):
    from .models import LessonVideo

    return bool(LessonVideo.objects(course=course, question__exists=True).first())


def require_video(user, video_id, *, course_id=None, part_id=None):
    """Resolve a video and prove it belongs to a course the learner owns."""
    video = LessonVideo.objects(id=video_id, is_published=True).first()
    if not video:
        raise ApiError("Lesson not found.", code="not_found", status_code=404)

    course = require_course(user, course_id=str(video.course.id))

    # The ids the client supplied must agree with the stored relationships.
    if course_id and str(course.id) != str(course_id):
        raise ApiError("This lesson belongs to another course.", code="mismatch", status_code=403)
    if part_id and str(video.part.id) != str(part_id):
        raise ApiError("This lesson belongs to another part.", code="mismatch", status_code=403)
    if str(video.part.course.id) != str(course.id):
        raise ApiError("Lesson is not part of this course.", code="mismatch", status_code=403)

    return video, video.part, course


def course_parts(course):
    return Part.objects(course=course, is_published=True).order_by("order")
