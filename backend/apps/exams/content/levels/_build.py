"""Turn a level's declarative spec into Goethe-format exam documents.

Every simulator is described as plain data — parts, stimulus blocks, items —
and this builder is the only place that knows how those become embedded
documents. Adding a level means writing a spec, not more construction code.
"""

from apps.core.i18n import tt
from apps.exams.models import (
    AudioTrack,
    ExamItem,
    ExamModule,
    ExamOption,
    ExamPart,
    StimulusBlock,
)

# The two option pools nearly every listening and A1/A2 reading task uses.
TRUE_FALSE = [("richtig", "Richtig"), ("falsch", "Falsch")]


def opts(pairs):
    """`[("a", "text"), …]` → options whose visible label is the key."""
    return [ExamOption(key=key, label=key, text=text) for key, text in pairs]


def choice(pairs):
    """`[("richtig", "Richtig"), …]` → options that show their own wording.

    A third element is the option's picture, which A1 tasks lean on.
    """
    return [
        ExamOption(
            key=row[0], label=row[1], text=row[1], image=row[2] if len(row) > 2 else ""
        )
        for row in pairs
    ]


def _blocks(rows):
    """`(kind, label, title, text)` rows; author 5th, image 6th, both optional."""
    out = []
    for row in rows:
        kind, label, title, text = row[:4]
        author = row[4] if len(row) > 4 else ""
        image = row[5] if len(row) > 5 else ""
        out.append(
            StimulusBlock(
                kind=kind, label=label, title=title, text=text, author=author, image=image
            )
        )
    return out


def _items(rows, pool=None):
    """`(number, prompt, choices|None, answer, (fa, en, de) explanation)`.

    `choices` of None means the item uses the part's shared option pool — the
    pattern for matching tasks, where every item picks from the same people.
    """
    out = []
    for row in rows:
        number, prompt, choices, answer = row[:4]
        explanation = row[4] if len(row) > 4 else None
        item = ExamItem(number=number, prompt=prompt, answer=answer)
        if choices:
            item.options = choice(choices) if choices is not pool else opts(choices)
        if explanation:
            item.explanation = tt(*explanation)
        out.append(item)
    return out


def build_part(spec, number):
    part = ExamPart(
        number=number,
        part_type=spec["type"],
        title=tt(*spec["title"]),
        instructions=tt(*spec["instructions"]),
        work_minutes=spec.get("minutes", 10),
        stimulus_title=spec.get("stimulus_title", ""),
        stimulus_subtitle=spec.get("stimulus_subtitle", ""),
        stimulus_intro=spec.get("stimulus_intro", ""),
        stimulus_image=spec.get("stimulus_image", ""),
        blocks=_blocks(spec.get("blocks", [])),
        options=opts(spec["pool"]) if spec.get("pool") else [],
        items=_items(spec.get("items", []), spec.get("pool")),
        example_prompt=spec.get("example_prompt", ""),
        example_answer=spec.get("example_answer", ""),
        min_words=spec.get("min_words"),
    )
    if spec.get("tracks"):
        part.audio = [
            AudioTrack(
                label=label,
                url=url,
                plays=plays,
                pre_read_seconds=pre_read,
                covers=covers,
            )
            for label, url, plays, pre_read, covers in spec["tracks"]
        ]
    return part


def build_module(spec):
    module = ExamModule(
        skill=spec["skill"],
        title=tt(*spec["title"]),
        intro=tt(*spec["intro"]),
        duration_minutes=spec["duration"],
        parts=[build_part(part, index + 1) for index, part in enumerate(spec["parts"])],
    )
    module.max_points = spec.get(
        "max_points", sum(len(part.items) for part in module.parts)
    )
    return module


def build_modules(level):
    """A level module exposes LESEN / HOEREN / SCHREIBEN specs."""
    return [build_module(spec) for spec in (level.LESEN, level.HOEREN, level.SCHREIBEN)]
