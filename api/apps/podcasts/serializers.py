from apps.core.i18n import t
from apps.courses.serializers import category_item


def _iso(value):
    return value.isoformat() if value else None


def podcast_card(podcast, locale):
    return {
        "id": str(podcast.id),
        "slug": podcast.slug,
        "title": t(podcast.title, locale),
        "tagline": t(podcast.tagline, locale),
        "cover": podcast.cover,
        "accent": podcast.accent,
        "host_name": podcast.host_name,
        "host_avatar": podcast.host_avatar,
        "level": podcast.level,
        "language": podcast.language,
        "tags": podcast.tags,
        "rating": podcast.rating,
        "plays": podcast.plays,
        "episodes_count": podcast.episodes_count,
        "is_featured": podcast.is_featured,
        "category": category_item(podcast.category, locale),
    }


def podcast_detail(podcast, locale, episodes=None):
    data = podcast_card(podcast, locale)
    data["description"] = t(podcast.description, locale)
    data["episodes"] = [episode_card(e, locale) for e in (episodes or [])]
    return data


def episode_card(episode, locale):
    podcast = episode.podcast
    return {
        "id": str(episode.id),
        "slug": episode.slug,
        "number": episode.number,
        "title": t(episode.title, locale),
        "description": t(episode.description, locale),
        "cover": episode.cover or (podcast.cover if podcast else ""),
        "duration_seconds": episode.duration_seconds,
        "level": episode.level,
        "plays": episode.plays,
        "is_premium": episode.is_premium,
        "published_at": _iso(episode.published_at),
        "podcast": {
            "slug": podcast.slug,
            "title": t(podcast.title, locale),
            "accent": podcast.accent,
            "host_name": podcast.host_name,
        }
        if podcast
        else None,
    }


def episode_detail(episode, locale, progress=None, bookmarked=False):
    data = episode_card(episode, locale)
    data.update(
        {
            "audio_url": episode.audio_url,
            "transcript": [
                {
                    "start": line.start,
                    "end": line.end,
                    "speaker": line.speaker,
                    "text": line.text,
                    "translation": t(line.translation, locale),
                }
                for line in episode.transcript
            ],
            "vocabulary": [
                {
                    "term": v.term,
                    "article": v.article,
                    "meaning": t(v.meaning, locale),
                    "example": v.example,
                }
                for v in episode.vocabulary
            ],
            "progress": progress,
            "bookmarked": bookmarked,
        }
    )
    return data
