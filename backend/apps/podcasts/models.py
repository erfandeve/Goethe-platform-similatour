from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
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
from apps.courses.models import Category

LEVELS = ("A1", "A2", "B1", "B2", "C1")


class Podcast(Document):
    meta = {"collection": "podcasts", "indexes": ["slug", "level", "category"]}

    slug = StringField(required=True, unique=True)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    tagline = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    category = ReferenceField(Category)
    host_name = StringField(default="")
    host_avatar = StringField(default="")
    cover = StringField(default="")
    accent = StringField(default="#6d5efc")

    language = StringField(default="de")
    level = StringField(choices=LEVELS, default="A2")
    tags = ListField(StringField(), default=list)

    rating = FloatField(default=0.0)
    plays = IntField(default=0)
    is_featured = BooleanField(default=False)
    is_published = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def episodes_count(self):
        return Episode.objects(podcast=self, is_published=True).count()


class TranscriptLine(EmbeddedDocument):
    start = FloatField(default=0.0)  # seconds
    end = FloatField(default=0.0)
    speaker = StringField(default="")
    text = StringField(default="")           # original (German)
    translation = EmbeddedDocumentField(TranslatedText, default=TranslatedText)


class VocabItem(EmbeddedDocument):
    term = StringField(default="")
    article = StringField(default="")
    meaning = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    example = StringField(default="")


class Episode(Document):
    meta = {"collection": "episodes", "indexes": ["slug", "podcast", "-published_at"]}

    slug = StringField(required=True, unique=True)
    podcast = ReferenceField(Podcast, required=True, reverse_delete_rule=2)
    number = IntField(default=1)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    audio_url = StringField(default="")
    cover = StringField(default="")
    duration_seconds = IntField(default=0)
    level = StringField(choices=LEVELS, default="A2")

    transcript = EmbeddedDocumentListField(TranscriptLine, default=list)
    vocabulary = EmbeddedDocumentListField(VocabItem, default=list)

    plays = IntField(default=0)
    is_premium = BooleanField(default=False)
    is_published = BooleanField(default=True)
    published_at = DateTimeField(default=datetime.utcnow)


class ListenProgress(Document):
    meta = {"collection": "listen_progress", "indexes": [("user", "episode"), "-updated_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    episode = ReferenceField(Episode, required=True, reverse_delete_rule=2)
    position_seconds = IntField(default=0)
    completed = BooleanField(default=False)
    updated_at = DateTimeField(default=datetime.utcnow)


class Bookmark(Document):
    meta = {"collection": "bookmarks", "indexes": [("user", "episode")]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    episode = ReferenceField(Episode, required=True, reverse_delete_rule=2)
    created_at = DateTimeField(default=datetime.utcnow)
