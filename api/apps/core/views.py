from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.courses.models import Category, Course, Instructor
from apps.courses.serializers import category_item, course_card, instructor_detail
from apps.exams.models import Exam
from apps.exams.serializers import exam_card
from apps.podcasts.models import Episode, Podcast
from apps.podcasts.serializers import episode_card, podcast_card

from .utils import get_locale


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "goteh-api"})


@api_view(["GET"])
def home(request):
    """Everything the landing page needs, in one request."""
    locale = get_locale(request)

    featured = Course.objects(is_published=True, is_featured=True).order_by("-students_count")[:6]
    newest = Course.objects(is_published=True).order_by("-created_at")[:8]
    exams = Exam.objects(is_published=True).order_by("kind", "level")
    podcasts = Podcast.objects(is_published=True).order_by("-is_featured", "-plays")[:4]
    episodes = Episode.objects(is_published=True).order_by("-published_at")[:6]

    return Response(
        {
            "featured_courses": [course_card(c, locale) for c in featured],
            "newest_courses": [course_card(c, locale) for c in newest],
            "simulators": [exam_card(e, locale) for e in exams if e.kind == "simulator"],
            "frequent_exams": [exam_card(e, locale) for e in exams if e.kind == "frequent"],
            "podcasts": [podcast_card(p, locale) for p in podcasts],
            "latest_episodes": [episode_card(e, locale) for e in episodes],
            "categories": [
                {
                    **category_item(c, locale),
                    "count": Course.objects(category=c, is_published=True).count(),
                }
                for c in Category.objects(kind="course").order_by("order")
            ],
            "instructors": [
                instructor_detail(i, locale)
                for i in Instructor.objects(is_featured=True).order_by("-students")[:4]
            ],
            "stats": {
                "students": sum(c.students_count for c in Course.objects(is_published=True)),
                "courses": Course.objects(is_published=True).count(),
                "exams": exams.count(),
                "episodes": Episode.objects(is_published=True).count(),
            },
        }
    )


@api_view(["GET"])
def sitemap_feed(request):
    """Slugs + timestamps for the Next.js sitemap builder."""
    return Response(
        {
            "courses": [
                {"slug": c.slug, "updated": c.created_at.isoformat() if c.created_at else None}
                for c in Course.objects(is_published=True).only("slug", "created_at")
            ],
            "exams": [
                {"slug": e.slug, "updated": e.created_at.isoformat() if e.created_at else None}
                for e in Exam.objects(is_published=True).only("slug", "created_at")
            ],
            "podcasts": [
                {"slug": p.slug, "updated": p.created_at.isoformat() if p.created_at else None}
                for p in Podcast.objects(is_published=True).only("slug", "created_at")
            ],
            "episodes": [
                {"slug": e.slug, "updated": e.published_at.isoformat() if e.published_at else None}
                for e in Episode.objects(is_published=True).only("slug", "published_at")
            ],
        }
    )
