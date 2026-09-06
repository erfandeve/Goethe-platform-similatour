"""Video lessons and AI speaking practice.

Builds on the existing catalogue: a Course already carries pricing, access and
marketing copy, so this module only adds what the classroom needs — the ordered
parts, the video files themselves, the speaking prompt attached to a video, and
the per-user record of watching and speaking.
"""

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
from apps.courses.models import Course

CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")


class Part(Document):
    """A chapter of a course: an ordered group of lesson videos."""

    meta = {"collection": "parts", "indexes": [("course", "order"), "slug"]}

    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    slug = StringField(required=True)
    order = IntField(default=1)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    title_de = StringField(default="")
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    is_published = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def videos(self):
        return LessonVideo.objects(part=self, is_published=True).order_by("order")


class Question(EmbeddedDocument):
    """The speaking prompt a learner answers after watching the video."""

    prompt_de = StringField(required=True)
    prompt = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    hint = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    expected_points = ListField(StringField(), default=list)
    grammar_topics = ListField(StringField(), default=list)
    vocabulary = ListField(StringField(), default=list)
    min_words = IntField(default=3)


class LessonVideo(Document):
    meta = {
        "collection": "lesson_videos",
        "indexes": [("part", "order"), ("course", "order"), "slug"],
    }

    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    part = ReferenceField(Part, required=True, reverse_delete_rule=2)
    slug = StringField(required=True, unique=True)
    order = IntField(default=1)

    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    title_de = StringField(default="")
    scene_label = StringField(default="")          # "SZENE 4 – ANKUNFT IN FRANKFURT"
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    video_url = StringField(required=True)
    poster_url = StringField(default="")
    duration_seconds = IntField(default=0)
    cefr_level = StringField(choices=CEFR_LEVELS, default="A1")

    # Videos 1–3 of the demo course are watch-only; the speaking task starts at 4.
    question = EmbeddedDocumentField(Question)
    is_published = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def has_speaking_task(self):
        return bool(self.question and self.question.prompt_de)


class VideoProgress(Document):
    """Where a learner stands on one video."""

    meta = {
        "collection": "video_progress",
        "indexes": [
            # Unique: a learner has exactly one row per video. Without this a
            # position ping and a completion save racing each other insert two.
            {"fields": ("user", "video"), "unique": True},
            ("user", "course"),
            "-updated_at",
        ],
    }

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    part = ReferenceField(Part, required=True, reverse_delete_rule=2)
    video = ReferenceField(LessonVideo, required=True, reverse_delete_rule=2)

    position_seconds = FloatField(default=0.0)
    duration_seconds = FloatField(default=0.0)
    watched_seconds = FloatField(default=0.0)
    completed = BooleanField(default=False)
    completed_at = DateTimeField()
    speaking_done = BooleanField(default=False)
    best_score = IntField(default=0)
    last_score = IntField(default=0)
    attempts = IntField(default=0)
    updated_at = DateTimeField(default=datetime.utcnow)


class Mistake(EmbeddedDocument):
    original = StringField(default="")
    correction = StringField(default="")
    type = StringField(default="grammar")
    explanation = StringField(default="")


class SpeakingAttempt(Document):
    meta = {
        "collection": "speaking_attempts",
        "indexes": [("user", "video"), ("user", "course"), "-created_at"],
    }

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    part = ReferenceField(Part, required=True, reverse_delete_rule=2)
    video = ReferenceField(LessonVideo, required=True, reverse_delete_rule=2)

    question_de = StringField(default="")
    transcript = StringField(default="")
    score = IntField(default=0)
    cefr_estimate = StringField(default="")
    audio_path = StringField(default="")          # only when STORE_AUDIO is on
    audio_seconds = FloatField(default=0.0)

    processing_status = StringField(
        choices=("transcribing", "analyzing", "completed", "failed"), default="transcribing"
    )
    error = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def analysis(self):
        return AIAnalysis.objects(speaking_attempt=self).order_by("-created_at").first()


class AIAnalysis(Document):
    """The teacher's verdict on one spoken answer, as returned by the model."""

    meta = {"collection": "ai_analyses", "indexes": ["speaking_attempt", "-created_at"]}

    speaking_attempt = ReferenceField(SpeakingAttempt, required=True, reverse_delete_rule=2)
    overall_score = IntField(default=0)
    cefr_estimate = StringField(default="")
    is_relevant = BooleanField(default=True)
    summary = StringField(default="")
    corrected_answer = StringField(default="")
    mistakes = EmbeddedDocumentListField(Mistake, default=list)
    categories = DictField(default=dict)
    positive_feedback = ListField(StringField(), default=list)
    improvement_tips = ListField(StringField(), default=list)
    next_action = StringField(default="continue")

    model = StringField(default="")
    raw_response = DictField(default=dict)
    created_at = DateTimeField(default=datetime.utcnow)
