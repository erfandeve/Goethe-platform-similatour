from apps.core.i18n import t


def _iso(value):
    return value.isoformat() if value else None


def exam_card(exam, locale):
    return {
        "id": str(exam.id),
        "slug": exam.slug,
        "title": t(exam.title, locale),
        "subtitle": t(exam.subtitle, locale),
        "level": exam.level,
        "kind": exam.kind,
        "language": exam.language,
        "exam_board": exam.exam_board,
        "cover": exam.cover,
        "accent": exam.accent,
        "badge": exam.badge,
        "duration_minutes": exam.duration_minutes,
        "questions_count": exam.questions_count,
        "sections_count": len(exam.sections),
        "skills": [s.skill for s in exam.sections],
        "price": exam.price,
        "discount_price": exam.discount_price,
        "effective_price": exam.effective_price,
        "is_free": exam.is_free,
        "pass_score": exam.pass_score,
        "rating": exam.rating,
        "attempts_count": exam.attempts_count,
        "is_featured": exam.is_featured,
    }


def exam_detail(exam, locale, with_questions=False):
    data = exam_card(exam, locale)
    data["description"] = t(exam.description, locale)
    data["highlights"] = [t(h, locale) for h in exam.highlights]
    data["max_score"] = exam.max_score
    data["sections"] = [
        {
            "index": index,
            "skill": section.skill,
            "title": t(section.title, locale),
            "instructions": t(section.instructions, locale),
            "duration_minutes": section.duration_minutes,
            "questions_count": len(section.questions),
            **(
                {
                    "questions": [
                        question_item(q, locale, index, qi)
                        for qi, q in enumerate(section.questions)
                    ]
                }
                if with_questions
                else {}
            ),
        }
        for index, section in enumerate(exam.sections)
    ]
    return data


def question_item(question, locale, section_index, question_index):
    """Answer keys are never sent to the client while an attempt is open."""
    return {
        "key": f"{section_index}:{question_index}",
        "prompt": t(question.prompt, locale),
        "passage": t(question.passage, locale),
        "audio_url": question.audio_url,
        "image_url": question.image_url,
        "kind": question.kind,
        "points": question.points,
        "options": [t(o, locale) for o in question.options],
    }


def attempt_item(attempt, locale):
    exam = attempt.exam
    return {
        "id": str(attempt.id),
        "status": attempt.status,
        "score": attempt.score,
        "raw_score": attempt.raw_score,
        "max_score": attempt.max_score,
        "correct_count": attempt.correct_count,
        "passed": attempt.passed,
        "cefr_estimate": attempt.cefr_estimate,
        "started_at": _iso(attempt.started_at),
        "finished_at": _iso(attempt.finished_at),
        "duration_seconds": attempt.duration_seconds,
        "section_results": [
            {"skill": r.skill, "score": r.score, "max_score": r.max_score}
            for r in attempt.section_results
        ],
        "exam": exam_card(exam, locale) if exam else None,
    }


def attempt_review(attempt, locale):
    """Full answer key, only returned after the attempt is finished."""
    data = attempt_item(attempt, locale)
    exam = attempt.exam
    review = []
    for si, section in enumerate(exam.sections):
        for qi, question in enumerate(section.questions):
            key = f"{si}:{qi}"
            given = attempt.answers.get(key)
            review.append(
                {
                    "key": key,
                    "skill": section.skill,
                    "prompt": t(question.prompt, locale),
                    "options": [t(o, locale) for o in question.options],
                    "kind": question.kind,
                    "given": given,
                    "correct_index": question.correct_index,
                    "correct_indices": question.correct_indices,
                    "explanation": t(question.explanation, locale),
                    "is_correct": _is_correct(question, given),
                }
            )
    data["review"] = review
    return data


def _is_correct(question, given):
    if given is None:
        return False
    if question.kind == "multiple":
        return sorted(given or []) == sorted(question.correct_indices)
    if question.kind in ("essay", "audio_answer"):
        return None  # graded by a teacher
    return given == question.correct_index


# ---------------------------------------------------------------------------
# Goethe-format serialization
#
# `with_answers` is the switch that keeps the key on the server: the runner is
# always served with it off, and only a finished attempt turns it on.
# ---------------------------------------------------------------------------


def option_item(option):
    return {
        "key": option.key,
        "label": option.label,
        "text": option.text,
        "author": option.author,
        "image": option.image,
    }


def block_item(block):
    return {
        "kind": block.kind,
        "label": block.label,
        "title": block.title,
        "text": block.text,
        "author": block.author,
        "image": block.image,
    }


def part_item(part, module_skill, part_index, locale, with_answers=False):
    return {
        "index": part_index,
        "number": part.number,
        "type": part.part_type,
        "title": t(part.title, locale),
        "title_de": part.title.de if part.title else "",
        "instructions": t(part.instructions, locale),
        "instructions_de": part.instructions.de if part.instructions else "",
        "work_minutes": part.work_minutes,
        "stimulus": {
            "title": part.stimulus_title,
            "subtitle": part.stimulus_subtitle,
            "image": part.stimulus_image,
            "intro": part.stimulus_intro,
            "blocks": [block_item(block) for block in part.blocks],
        },
        "options": [option_item(option) for option in part.options],
        "audio": [
            {
                "index": index,
                "label": track.label,
                "url": track.url,
                "plays": track.plays,
                "pre_read_seconds": track.pre_read_seconds,
                "covers": track.covers,
            }
            for index, track in enumerate(part.audio)
        ],
        "example": {"prompt": part.example_prompt, "answer": part.example_answer},
        "min_words": part.min_words,
        "items": [
            {
                "key": f"{module_skill}:{part_index}:{item.number}",
                "number": item.number,
                "prompt": item.prompt,
                "points": item.points,
                "audio_index": item.audio_index,
                "options": [option_item(option) for option in item.options],
                **(
                    {
                        "answer": item.answer,
                        "explanation": t(item.explanation, locale),
                    }
                    if with_answers
                    else {}
                ),
            }
            for item in part.items
        ],
    }


def module_item(module, locale, with_parts=False, with_answers=False):
    data = {
        "skill": module.skill,
        "title": t(module.title, locale),
        "intro": t(module.intro, locale),
        "duration_minutes": module.duration_minutes,
        "max_points": module.max_points,
        "parts_count": len(module.parts),
        "items_count": module.items_count,
    }
    if with_parts:
        data["parts"] = [
            part_item(part, module.skill, index, locale, with_answers)
            for index, part in enumerate(module.parts)
        ]
    return data


def exam_modules(exam, locale):
    return [module_item(module, locale) for module in exam.modules]


def module_review(module, answers, locale):
    """Per-item breakdown returned once an attempt is finished."""
    rows = []
    for part_index, part in enumerate(module.parts):
        pool = {option.key: option for option in part.options}
        for item in part.items:
            given = answers.get(f"{module.skill}:{part_index}:{item.number}")
            local = {option.key: option for option in item.options}
            lookup = local or pool

            def label_for(key):
                option = lookup.get(str(key)) if key is not None else None
                if not option:
                    return str(key) if key is not None else ""
                return option.label or option.text or option.key

            if part.part_type == "writing":
                rows.append(
                    {
                        "key": f"{module.skill}:{part_index}:{item.number}",
                        "number": item.number,
                        "part": part.number,
                        "type": part.part_type,
                        "prompt": item.prompt or t(part.title, locale),
                        "given_text": given or "",
                        "is_correct": None,
                    }
                )
                continue

            rows.append(
                {
                    "key": f"{module.skill}:{part_index}:{item.number}",
                    "number": item.number,
                    "part": part.number,
                    "type": part.part_type,
                    "prompt": item.prompt,
                    "given": given,
                    "given_label": label_for(given),
                    "answer": item.answer,
                    "answer_label": label_for(item.answer),
                    "explanation": t(item.explanation, locale),
                    "is_correct": given is not None and str(given) == item.answer,
                }
            )
    return rows


def code_item(code, locale, *, owned=False):
    """A sitting a learner can pick on the product page."""
    return {
        "id": str(code.id),
        "code": code.code,
        "label": t(code.label, locale) or code.code,
        "description": t(code.description, locale),
        "order": code.order,
        # What this sitting costs on its own; the picker adds them up.
        "price": code.effective_price,
        "extra_price": code.extra_price,
        "items_count": code.items_count,
        "modules": [module.skill for module in code.modules],
        # The paper this sitting actually runs: its own if it has one, else the
        # exam's, so a code created without questions is still sittable.
        "paper": [
            module_item(module, locale)
            for module in (code.modules or (code.exam.modules if code.exam else []))
        ],
        "owned": owned,
    }
