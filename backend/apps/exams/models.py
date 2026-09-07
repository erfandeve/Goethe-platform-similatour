from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from apps.accounts.models import User
from apps.core.i18n import TranslatedText

LEVELS = ("A1", "A2", "B1", "B2", "C1")
# "frequent" = پرتکرار: recycled real-exam material, offered for B2 and C1 only.
KINDS = ("simulator", "frequent")
SKILLS = ("listening", "reading", "writing", "speaking", "grammar")


class Question(EmbeddedDocument):
    prompt = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    passage = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    audio_url = StringField(default="")
    image_url = StringField(default="")
    kind = StringField(
        choices=("single", "multiple", "true_false", "gap", "essay", "audio_answer"),
        default="single",
    )
    options = ListField(EmbeddedDocumentField(TranslatedText), default=list)
    correct_index = IntField(default=0)
    correct_indices = ListField(IntField(), default=list)
    explanation = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    points = IntField(default=1)


class ExamSection(EmbeddedDocument):
    skill = StringField(choices=SKILLS, default="reading")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    instructions = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    duration_minutes = IntField(default=20)
    questions = EmbeddedDocumentListField(Question, default=list)


# ---------------------------------------------------------------------------
# Goethe-format content
#
# The official digital exam is built from "Teile" that each pair one stimulus
# (an article, a set of forum posts, an audio track…) with a list of numbered
# items. The shapes below model that directly instead of flattening everything
# into single-choice questions, so the UI can render each Teil the way the real
# exam does.
# ---------------------------------------------------------------------------

PART_TYPES = (
    "match_person",     # Lesen 1: statements → one of four people
    "gap_drag",         # Lesen 2: drag sentences into numbered gaps
    "mcq",              # Lesen 3 / Hören 2-4: question with its own options
    "match_heading",    # Lesen 4: headings → opinion boxes a–h
    "match_paragraph",  # Lesen 5: paragraphs → headings a–h
    "listening_mixed",  # Hören 1: richtig/falsch and 3-option items per track
    "writing",          # Schreiben 1-2: free text
)

MODULE_SKILLS = ("lesen", "hoeren", "schreiben", "sprechen")


class ExamOption(EmbeddedDocument):
    key = StringField(required=True)          # "a" … "h", or "richtig"/"falsch"
    label = StringField(default="")           # what the learner sees as the choice
    text = StringField(default="")            # full sentence, when the option is a sentence
    author = StringField(default="")          # "Amelie, Bonn"
    image = StringField(default="")


class ExamItem(EmbeddedDocument):
    number = IntField(required=True)          # the printed item number, 1…30
    prompt = StringField(default="")
    options = EmbeddedDocumentListField(ExamOption, default=list)  # empty → use the part pool
    answer = StringField(default="")          # option key; never leaves the server mid-attempt
    explanation = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    points = IntField(default=1)
    audio_index = IntField()                  # which track of the part this item belongs to


class StimulusBlock(EmbeddedDocument):
    """One unit of the reading/listening material shown on the left panel."""

    kind = StringField(
        choices=("paragraph", "person", "statement", "heading", "section", "bullet"),
        default="paragraph",
    )
    label = StringField(default="")           # "a", "§ 28"
    title = StringField(default="")           # "Erik"
    text = StringField(default="")
    author = StringField(default="")          # "Amelie, Bonn"
    image = StringField(default="")


class AudioTrack(EmbeddedDocument):
    label = StringField(default="")           # "Aufgabe 1 und 2"
    url = StringField(default="")
    plays = IntField(default=1)               # how often the recording may be heard
    pre_read_seconds = IntField(default=15)   # reading time before playback starts
    covers = ListField(IntField(), default=list)  # item numbers this track answers


class ExamPart(EmbeddedDocument):
    number = IntField(default=1)
    part_type = StringField(choices=PART_TYPES, default="mcq")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    instructions = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    work_minutes = IntField(default=10)

    stimulus_title = StringField(default="")
    stimulus_subtitle = StringField(default="")
    stimulus_image = StringField(default="")
    stimulus_intro = StringField(default="")
    blocks = EmbeddedDocumentListField(StimulusBlock, default=list)

    options = EmbeddedDocumentListField(ExamOption, default=list)
    items = EmbeddedDocumentListField(ExamItem, default=list)
    audio = EmbeddedDocumentListField(AudioTrack, default=list)

    example_prompt = StringField(default="")
    example_answer = StringField(default="")
    min_words = IntField()                    # writing tasks only


class ExamModule(EmbeddedDocument):
    skill = StringField(choices=MODULE_SKILLS, default="lesen")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    intro = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    duration_minutes = IntField(default=60)
    max_points = IntField(default=30)
    parts = EmbeddedDocumentListField(ExamPart, default=list)

    @property
    def items_count(self):
        return sum(len(part.items) for part in self.parts)


class Exam(Document):
    meta = {
        "collection": "exams",
        "indexes": ["slug", "level", "kind", "-created_at"],
    }

    slug = StringField(required=True, unique=True)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    subtitle = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    level = StringField(choices=LEVELS, default="A1")
    kind = StringField(choices=KINDS, default="simulator")
    language = StringField(default="de")
    exam_board = StringField(default="Goethe-Zertifikat")

    cover = StringField(default="")
    accent = StringField(default="#6d5efc")
    badge = StringField(default="")

    duration_minutes = IntField(default=90)
    pass_score = IntField(default=60)
    price = IntField(default=0)
    discount_price = IntField(default=0)

    sections = EmbeddedDocumentListField(ExamSection, default=list)
    # Goethe-format content; when present it replaces `sections` in the runner.
    modules = EmbeddedDocumentListField(ExamModule, default=list)
    highlights = ListField(EmbeddedDocumentField(TranslatedText), default=list)

    rating = FloatField(default=0.0)
    attempts_count = IntField(default=0)
    is_published = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def is_free(self):
        return self.effective_price == 0

    @property
    def format(self):
        return "goethe" if self.modules else "simple"

    @property
    def questions_count(self):
        if self.modules:
            return sum(module.items_count for module in self.modules)
        return sum(len(s.questions) for s in self.sections)

    @property
    def max_score(self):
        if self.modules:
            return sum(
                item.points
                for module in self.modules
                for part in module.parts
                if part.part_type != "writing"
                for item in part.items
            )
        return sum(q.points for s in self.sections for q in s.questions)


class ExamCode(Document):
    """A sitting of an exam, the way candidates buy it.

    A learner picks which code(s) to take. The exam's own price covers the first
    one; each additional code costs `extra_price` on top. Every code carries its
    own question set, so two people with different codes sit different papers.
    """

    meta = {"collection": "exam_codes", "indexes": [("exam", "order"), "code", "-created_at"]}

    exam = ReferenceField("Exam", required=True, reverse_delete_rule=2)
    code = StringField(required=True)          # e.g. "B2-2024-01"
    label = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    order = IntField(default=1)

    # Zero means "included in the exam price"; the first chosen code is free.
    extra_price = IntField(default=0)

    modules = EmbeddedDocumentListField(ExamModule, default=list)
    is_published = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def items_count(self):
        return sum(module.items_count for module in self.modules)

    @property
    def max_score(self):
        return sum(
            item.points
            for module in self.modules
            for part in module.parts
            if part.part_type != "writing"
            for item in part.items
        )


class ExamAccess(Document):
    """Purchased access to a paid exam."""

    meta = {"collection": "exam_access", "indexes": [("user", "exam")]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    exam = StringField(required=True)  # Exam id as string, mirrors cart item ids
    exam_code = StringField(default="")  # ExamCode id; empty means the whole exam
    order_code = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)


class SectionResult(EmbeddedDocument):
    skill = StringField(default="reading")
    score = IntField(default=0)
    max_score = IntField(default=0)


class ExamAttempt(Document):
    meta = {"collection": "exam_attempts", "indexes": ["user", "exam", "-started_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    exam = ReferenceField(Exam, required=True, reverse_delete_rule=2)
    module = StringField(default="")  # "lesen" | "hoeren" | … ; empty for legacy exams
    exam_code = StringField(default="")  # which sitting was taken
    status = StringField(choices=("in_progress", "finished", "abandoned"), default="in_progress")

    answers = DictField(default=dict)  # {"<section>:<question>": answer}
    score = IntField(default=0)       # percentage
    raw_score = IntField(default=0)
    max_score = IntField(default=0)
    correct_count = IntField(default=0)
    section_results = EmbeddedDocumentListField(SectionResult, default=list)
    passed = BooleanField(default=False)
    cefr_estimate = StringField(default="")

    started_at = DateTimeField(default=datetime.utcnow)
    finished_at = DateTimeField()
    duration_seconds = IntField(default=0)
