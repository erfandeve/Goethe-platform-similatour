"""Back-office shapes.

The catalogue stores every user-facing string in three languages, so the editor
gets the raw `{fa, en, de}` object rather than a resolved string — otherwise a
save would quietly flatten the other two translations.
"""

from apps.core.i18n import TranslatedText


def _iso(value):
    return value.isoformat() if value else None


def translated(field):
    return {"fa": field.fa, "en": field.en, "de": field.de} if field else {"fa": "", "en": "", "de": ""}


def read_translated(payload, current=None):
    """Merge an incoming `{fa, en, de}` patch onto the stored value."""
    base = current or TranslatedText()
    if not isinstance(payload, dict):
        return base
    return TranslatedText(
        fa=payload.get("fa", base.fa) or "",
        en=payload.get("en", base.en) or "",
        de=payload.get("de", base.de) or "",
    )


def category_row(category, course_count=0):
    return {
        "id": str(category.id),
        "slug": category.slug,
        "kind": category.kind,
        "title": translated(category.title),
        "description": translated(category.description),
        "icon": category.icon,
        "color": category.color,
        "order": category.order,
        "course_count": course_count,
    }


def instructor_row(instructor):
    return {
        "id": str(instructor.id),
        "slug": instructor.slug,
        "name": instructor.name,
        "avatar": instructor.avatar,
        "headline": translated(instructor.headline),
        "bio": translated(instructor.bio),
        "languages": instructor.languages,
        "rating": instructor.rating,
        "students": instructor.students,
        "is_featured": instructor.is_featured,
    }


def course_row(course, *, parts=0, videos=0):
    return {
        "id": str(course.id),
        "slug": course.slug,
        "title": translated(course.title),
        "subtitle": translated(course.subtitle),
        "level": course.level,
        "language": course.language,
        "format": course.format,
        "accent": course.accent,
        "cover": course.cover,
        "price": course.price,
        "discount_price": course.discount_price,
        "duration_minutes": course.duration_minutes,
        "students_count": course.students_count,
        "is_published": course.is_published,
        "is_featured": course.is_featured,
        "is_bestseller": course.is_bestseller,
        "category": str(course.category.id) if course.category else None,
        "category_slug": course.category.slug if course.category else "",
        "instructor": str(course.instructor.id) if course.instructor else None,
        "parts_count": parts,
        "videos_count": videos,
        "created_at": _iso(course.created_at),
    }


def course_detail(course, *, parts=0, videos=0):
    data = course_row(course, parts=parts, videos=videos)
    data.update(
        {
            "description": translated(course.description),
            "tags": course.tags,
            "outcomes": [translated(item) for item in course.outcomes],
            "requirements": [translated(item) for item in course.requirements],
            "sessions_count": course.sessions_count,
        }
    )
    return data


def question_payload(question):
    if not question:
        return None
    return {
        "prompt_de": question.prompt_de,
        "prompt": translated(question.prompt),
        "hint": translated(question.hint),
        "expected_points": question.expected_points,
        "grammar_topics": question.grammar_topics,
        "vocabulary": question.vocabulary,
        "min_words": question.min_words,
    }


def video_row(video):
    return {
        "id": str(video.id),
        "slug": video.slug,
        "order": video.order,
        "title": translated(video.title),
        "title_de": video.title_de,
        "scene_label": video.scene_label,
        "description": translated(video.description),
        "video_url": video.video_url,
        "poster_url": video.poster_url,
        "duration_seconds": video.duration_seconds,
        "cefr_level": video.cefr_level,
        "is_published": video.is_published,
        "has_speaking_task": video.has_speaking_task,
        "question": question_payload(video.question),
        "part": str(video.part.id) if video.part else None,
    }


def part_row(part, videos=None):
    data = {
        "id": str(part.id),
        "slug": part.slug,
        "order": part.order,
        "title": translated(part.title),
        "title_de": part.title_de,
        "description": translated(part.description),
        "is_published": part.is_published,
        "course": str(part.course.id) if part.course else None,
    }
    if videos is not None:
        data["videos"] = [video_row(video) for video in videos]
        data["videos_count"] = len(data["videos"])
    return data


# ---------------------------------------------------------------- exams ---


def exam_row(exam):
    return {
        "id": str(exam.id),
        "slug": exam.slug,
        "title": translated(exam.title),
        "subtitle": translated(exam.subtitle),
        "level": exam.level,
        "kind": exam.kind,
        "exam_board": exam.exam_board,
        "accent": exam.accent,
        "badge": exam.badge,
        "cover": exam.cover,
        "duration_minutes": exam.duration_minutes,
        "pass_score": exam.pass_score,
        "price": exam.price,
        "discount_price": exam.discount_price,
        "is_published": exam.is_published,
        "is_featured": exam.is_featured,
        "format": exam.format,
        "questions_count": exam.questions_count,
        "modules_count": len(exam.modules),
        "attempts_count": exam.attempts_count,
    }


def exam_option_row(option):
    return {
        "key": option.key,
        "label": option.label,
        "text": option.text,
        "author": option.author,
        "image": option.image,
    }


def exam_item_row(item):
    """Includes the answer key — this shape never leaves the back office."""
    return {
        "number": item.number,
        "prompt": item.prompt,
        "answer": item.answer,
        "points": item.points,
        "audio_index": item.audio_index,
        "explanation": translated(item.explanation),
        "options": [exam_option_row(option) for option in item.options],
    }


def exam_part_row(part, index):
    return {
        "index": index,
        "number": part.number,
        "type": part.part_type,
        "title": translated(part.title),
        "instructions": translated(part.instructions),
        "work_minutes": part.work_minutes,
        "stimulus_title": part.stimulus_title,
        "stimulus_subtitle": part.stimulus_subtitle,
        "stimulus_intro": part.stimulus_intro,
        "stimulus_image": part.stimulus_image,
        "blocks": [
            {
                "kind": block.kind,
                "label": block.label,
                "title": block.title,
                "text": block.text,
                "author": block.author,
                "image": block.image,
            }
            for block in part.blocks
        ],
        "options": [exam_option_row(option) for option in part.options],
        "audio": [
            {"label": track.label, "url": track.url, "plays": track.plays,
             "pre_read_seconds": track.pre_read_seconds, "covers": track.covers}
            for track in part.audio
        ],
        "items": [exam_item_row(item) for item in part.items],
        "example_prompt": part.example_prompt,
        "example_answer": part.example_answer,
        "min_words": part.min_words,
        # What still has to be filled in before learners can sit this Teil.
        "missing_answers": 0
        if part.part_type == "writing"
        else sum(1 for item in part.items if not item.answer),
        "missing_audio": sum(1 for track in part.audio if not track.url),
        # a picture block is filled by its image, not by text
        "empty_blocks": sum(
            1 for block in part.blocks if not block.text.strip() and not block.image
        ),
    }


def exam_module_row(module, index):
    return {
        "index": index,
        "skill": module.skill,
        "title": translated(module.title),
        "intro": translated(module.intro),
        "duration_minutes": module.duration_minutes,
        "max_points": module.max_points,
        "parts": [exam_part_row(part, i) for i, part in enumerate(module.parts)],
    }


def exam_detail(exam):
    data = exam_row(exam)
    data["description"] = translated(exam.description)
    data["highlights"] = [translated(item) for item in exam.highlights]
    data["modules"] = [exam_module_row(module, i) for i, module in enumerate(exam.modules)]
    return data


# ------------------------------------------------------------- podcasts ---


def podcast_row(podcast, episodes=0):
    return {
        "id": str(podcast.id),
        "slug": podcast.slug,
        "title": translated(podcast.title),
        "tagline": translated(podcast.tagline),
        "description": translated(podcast.description),
        "cover": podcast.cover,
        "accent": podcast.accent,
        "host_name": podcast.host_name,
        "level": podcast.level,
        "language": podcast.language,
        "tags": podcast.tags,
        "category": str(podcast.category.id) if podcast.category else None,
        "is_published": podcast.is_published,
        "is_featured": podcast.is_featured,
        "plays": podcast.plays,
        "episodes_count": episodes,
    }


def episode_row(episode):
    return {
        "id": str(episode.id),
        "slug": episode.slug,
        "number": episode.number,
        "title": translated(episode.title),
        "description": translated(episode.description),
        "audio_url": episode.audio_url,
        "cover": episode.cover,
        "duration_seconds": episode.duration_seconds,
        "level": episode.level,
        "is_premium": episode.is_premium,
        "is_published": episode.is_published,
        "podcast": str(episode.podcast.id) if episode.podcast else None,
        "transcript": [
            {
                "start": line.start,
                "end": line.end,
                "speaker": line.speaker,
                "text": line.text,
                "translation": translated(line.translation),
            }
            for line in episode.transcript
        ],
        "vocabulary": [
            {
                "term": item.term,
                "article": item.article,
                "meaning": translated(item.meaning),
                "example": item.example,
            }
            for item in episode.vocabulary
        ],
    }
