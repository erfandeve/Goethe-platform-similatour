from datetime import datetime

from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.permissions import IsAuthenticated
from apps.core.exceptions import ApiError
from apps.core.pagination import paginate
from apps.core.utils import get_locale
from apps.courses.models import Category

from .models import Bookmark, Episode, ListenProgress, Podcast
from .serializers import episode_card, episode_detail, podcast_card, podcast_detail


@api_view(["GET"])
def podcast_list(request):
    locale = get_locale(request)
    params = request.query_params
    qs = Podcast.objects(is_published=True)

    if params.get("level"):
        qs = qs.filter(level__in=params["level"].split(","))
    if params.get("category"):
        cats = Category.objects(slug__in=params["category"].split(","), kind="podcast")
        qs = qs.filter(category__in=list(cats))
    search = (params.get("q") or "").strip()
    if search:
        qs = qs.filter(
            Q(title__fa__icontains=search)
            | Q(title__en__icontains=search)
            | Q(title__de__icontains=search)
            | Q(tags__icontains=search)
        )

    qs = qs.order_by("-is_featured", "-plays")
    items, meta = paginate(qs, request, default_size=12)
    return Response({"results": [podcast_card(p, locale) for p in items], "meta": meta})


@api_view(["GET"])
def podcast_detail_view(request, slug):
    locale = get_locale(request)
    podcast = Podcast.objects(slug=slug, is_published=True).first()
    if not podcast:
        raise ApiError("Podcast not found.", status_code=404)
    episodes = Episode.objects(podcast=podcast, is_published=True).order_by("-number")
    return Response(podcast_detail(podcast, locale, episodes))


@api_view(["GET"])
def episode_list(request):
    """Flat feed across every show — powers the podcast landing page."""
    locale = get_locale(request)
    params = request.query_params
    qs = Episode.objects(is_published=True)

    if params.get("level"):
        qs = qs.filter(level__in=params["level"].split(","))
    if params.get("podcast"):
        show = Podcast.objects(slug=params["podcast"]).first()
        qs = qs.filter(podcast=show) if show else qs.none()
    if params.get("free") == "true":
        qs = qs.filter(is_premium=False)

    order = "-plays" if params.get("sort") == "popular" else "-published_at"
    qs = qs.order_by(order)
    items, meta = paginate(qs, request, default_size=12)
    return Response({"results": [episode_card(e, locale) for e in items], "meta": meta})


@api_view(["GET"])
def episode_detail_view(request, slug):
    locale = get_locale(request)
    episode = Episode.objects(slug=slug, is_published=True).first()
    if not episode:
        raise ApiError("Episode not found.", status_code=404)

    progress, bookmarked = None, False
    user = getattr(request, "user", None)
    if user:
        record = ListenProgress.objects(user=user, episode=episode).first()
        if record:
            progress = {
                "position_seconds": record.position_seconds,
                "completed": record.completed,
            }
        bookmarked = bool(Bookmark.objects(user=user, episode=episode).first())

    data = episode_detail(episode, locale, progress, bookmarked)
    siblings = Episode.objects(
        podcast=episode.podcast, is_published=True, id__ne=episode.id
    ).order_by("-number")[:6]
    data["more_episodes"] = [episode_card(e, locale) for e in siblings]
    return Response(data)


@api_view(["POST"])
def episode_play(request, slug):
    episode = Episode.objects(slug=slug).first()
    if not episode:
        raise ApiError("Episode not found.", status_code=404)
    episode.plays += 1
    episode.save()
    if episode.podcast:
        episode.podcast.plays += 1
        episode.podcast.save()
    return Response({"plays": episode.plays})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_progress(request, slug):
    episode = Episode.objects(slug=slug).first()
    if not episode:
        raise ApiError("Episode not found.", status_code=404)
    data = request.data or {}
    record = ListenProgress.objects(user=request.user, episode=episode).first()
    if not record:
        record = ListenProgress(user=request.user, episode=episode)
    record.position_seconds = int(data.get("position_seconds", 0))
    record.completed = bool(data.get("completed", False))
    record.updated_at = datetime.utcnow()
    record.save()
    return Response(
        {"position_seconds": record.position_seconds, "completed": record.completed}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, slug):
    episode = Episode.objects(slug=slug).first()
    if not episode:
        raise ApiError("Episode not found.", status_code=404)
    existing = Bookmark.objects(user=request.user, episode=episode).first()
    if existing:
        existing.delete()
        return Response({"bookmarked": False})
    Bookmark(user=request.user, episode=episode).save()
    return Response({"bookmarked": True})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_library(request):
    locale = get_locale(request)
    bookmarks = Bookmark.objects(user=request.user).order_by("-created_at")
    in_progress = ListenProgress.objects(
        user=request.user, completed=False
    ).order_by("-updated_at")[:8]
    return Response(
        {
            "bookmarks": [
                episode_card(b.episode, locale) for b in bookmarks if b.episode
            ],
            "continue_listening": [
                {
                    **episode_card(p.episode, locale),
                    "position_seconds": p.position_seconds,
                }
                for p in in_progress
                if p.episode
            ],
        }
    )
