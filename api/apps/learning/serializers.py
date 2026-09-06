from apps.core.i18n import t


def _iso(value):
    return value.isoformat() if value else None


def question_item(question, locale):
    if not question:
        return None
    return {
        "prompt_de": question.prompt_de,
        "prompt": t(question.prompt, locale),
        "hint": t(question.hint, locale),
        "expected_points": question.expected_points,
        "grammar_topics": question.grammar_topics,
        "vocabulary": question.vocabulary,
        "min_words": question.min_words,
    }


def video_item(video, locale, progress=None):
    return {
        "id": str(video.id),
        "slug": video.slug,
        "order": video.order,
        "title": t(video.title, locale),
        "title_de": video.title_de,
        "scene_label": video.scene_label,
        "description": t(video.description, locale),
        "video_url": video.video_url,
        "poster_url": video.poster_url,
        "duration_seconds": video.duration_seconds,
        "cefr_level": video.cefr_level,
        "has_speaking_task": video.has_speaking_task,
        "question": question_item(video.question, locale),
        "progress": progress_item(progress) if progress else None,
    }


def progress_item(progress):
    return {
        "position_seconds": progress.position_seconds,
        "completed": progress.completed,
        "speaking_done": progress.speaking_done,
        "best_score": progress.best_score,
        "last_score": progress.last_score,
        "attempts": progress.attempts,
        "updated_at": _iso(progress.updated_at),
    }


def part_item(part, locale, videos=None, progress_map=None):
    data = {
        "id": str(part.id),
        "slug": part.slug,
        "order": part.order,
        "title": t(part.title, locale),
        "title_de": part.title_de,
        "description": t(part.description, locale),
    }
    if videos is not None:
        progress_map = progress_map or {}
        data["videos"] = [
            video_item(video, locale, progress_map.get(str(video.id))) for video in videos
        ]
    return data


def analysis_item(analysis):
    if not analysis:
        return None
    return {
        "overall_score": analysis.overall_score,
        "cefr_estimate": analysis.cefr_estimate,
        "is_relevant": analysis.is_relevant,
        "summary": analysis.summary,
        "corrected_answer": analysis.corrected_answer,
        "mistakes": [
            {
                "original": m.original,
                "correction": m.correction,
                "type": m.type,
                "explanation": m.explanation,
            }
            for m in analysis.mistakes
        ],
        "categories": analysis.categories,
        "positive_feedback": analysis.positive_feedback,
        "improvement_tips": analysis.improvement_tips,
        "next_action": analysis.next_action,
    }


def attempt_item(attempt, *, with_analysis=True):
    data = {
        "id": str(attempt.id),
        "video_id": str(attempt.video.id) if attempt.video else None,
        "question_de": attempt.question_de,
        "transcript": attempt.transcript,
        "score": attempt.score,
        "cefr_estimate": attempt.cefr_estimate,
        "processing_status": attempt.processing_status,
        "created_at": _iso(attempt.created_at),
    }
    if with_analysis:
        data["analysis"] = analysis_item(attempt.analysis)
    return data
