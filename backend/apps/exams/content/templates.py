"""Blank exam papers in the official shape of each level.

A template is the matching simulator with every word of content removed: the
modules, Teile, task types, working times, item numbers, option keys, replay
counts and reading times stay; texts, prompts, answers, audio files and
examples go. Starting a new exam or exam code from one means the back office
only fills in material — it cannot get the structure wrong.

Templates are derived from the same specs that build the simulators, so the
two can never drift apart.
"""

import copy

from apps.core.i18n import TranslatedText

LEVELS = ("A1", "A2", "B1", "B2", "C1")

# Labels that belong to the task format rather than to a particular paper.
GENERIC_LABELS = {"richtig", "falsch", "ja", "nein", "moderator", "0"}


def source_modules(level):
    """The simulator modules for a level, freshly built from their spec."""
    level = level.upper()
    if level == "B2":
        # B2's content is built by its own command from the transcribed Modellsatz.
        from apps.exams.management.commands.seed_b2 import Command

        command = Command()
        return [command.lesen(), command.hoeren(), command.schreiben()]

    from apps.exams.content.levels import a1, a2, b1, c1
    from apps.exams.content.levels._build import build_modules

    specs = {"A1": a1, "A2": a2, "B1": b1, "C1": c1}
    if level not in specs:
        raise KeyError(level)
    return build_modules(specs[level])


def _keep_label(label, key):
    """Format words stay; a person's name or an advert's title does not."""
    if not label:
        return key
    if label.lower() in GENERIC_LABELS or len(label) <= 2:
        return label
    return key


def _blank_option(option):
    option.label = _keep_label(option.label, option.key)
    # "Richtig"/"Ja" carry their wording as text too; anything else is content.
    option.text = option.label if option.label.lower() in GENERIC_LABELS else ""
    option.author = ""
    option.image = ""
    return option


def blank_modules(modules):
    """Strip the content out of built modules, keeping their structure."""
    out = copy.deepcopy(modules)
    for module in out:
        for part in module.parts:
            part.stimulus_title = ""
            part.stimulus_subtitle = ""
            part.stimulus_intro = ""
            part.stimulus_image = ""
            part.example_prompt = ""
            part.example_answer = ""

            for block in part.blocks:
                # Keep the slot and its label (a–j, the comment numbers) so the
                # editor shows how many texts the Teil needs and where they go.
                block.title = ""
                block.text = ""
                block.author = ""
                block.image = ""

            for option in part.options:
                _blank_option(option)

            for item in part.items:
                item.prompt = ""
                item.answer = ""
                item.explanation = TranslatedText()
                for option in item.options:
                    _blank_option(option)

            for track in part.audio:
                track.url = ""
    return out


def template_modules(level):
    return blank_modules(source_modules(level))


def outline(level):
    """What a template would create, for the back office to preview."""
    modules = source_modules(level)
    return {
        "level": level.upper(),
        "modules": [
            {
                "skill": module.skill,
                "duration_minutes": module.duration_minutes,
                "parts": [
                    {
                        "number": part.number,
                        "type": part.part_type,
                        "title": part.title.de if part.title else "",
                        "work_minutes": part.work_minutes,
                        "items": [part.items[0].number, part.items[-1].number]
                        if part.items
                        else [],
                        "tracks": len(part.audio),
                    }
                    for part in module.parts
                ],
            }
            for module in modules
        ],
    }
