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

LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
LANGUAGES = ("de", "en", "fr", "tr", "es")
FORMATS = ("self_paced", "live", "hybrid", "private")


class Instructor(Document):
    meta = {"collection": "instructors", "indexes": ["slug"]}

    slug = StringField(required=True, unique=True)
    name = StringField(required=True)
    avatar = StringField(default="")
    headline = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    bio = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    languages = ListField(StringField(), default=list)
    rating = FloatField(default=5.0)
    students = IntField(default=0)
    is_featured = BooleanField(default=False)


class Category(Document):
    meta = {"collection": "categories", "indexes": ["slug", "kind"]}

    slug = StringField(required=True, unique_with="kind")
    kind = StringField(choices=("course", "podcast"), default="course")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    icon = StringField(default="")
    color = StringField(default="#6d5efc")
    order = IntField(default=0)


class Lesson(EmbeddedDocument):
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    duration_minutes = IntField(default=0)
    kind = StringField(choices=("video", "audio", "quiz", "live", "pdf"), default="video")
    is_preview = BooleanField(default=False)
    asset = StringField(default="")


class Section(EmbeddedDocument):
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    lessons = EmbeddedDocumentListField(Lesson, default=list)


class Course(Document):
    meta = {
        "collection": "courses",
        "indexes": ["slug", "level", "language", "category", "-created_at", "-students_count"],
    }

    slug = StringField(required=True, unique=True)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    subtitle = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    category = ReferenceField(Category)
    instructor = ReferenceField(Instructor)
    language = StringField(choices=LANGUAGES, default="de")
    level = StringField(choices=LEVELS, default="A1")
    format = StringField(choices=FORMATS, default="self_paced")

    cover = StringField(default="")
    accent = StringField(default="#6d5efc")
    trailer_url = StringField(default="")

    price = IntField(default=0)  # Rial
    discount_price = IntField(default=0)
    duration_minutes = IntField(default=0)
    sessions_count = IntField(default=0)

    curriculum = EmbeddedDocumentListField(Section, default=list)
    outcomes = ListField(EmbeddedDocumentField(TranslatedText), default=list)
    requirements = ListField(EmbeddedDocumentField(TranslatedText), default=list)
    tags = ListField(StringField(), default=list)

    rating = FloatField(default=0.0)
    reviews_count = IntField(default=0)
    students_count = IntField(default=0)

    is_published = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    is_bestseller = BooleanField(default=False)
    starts_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def lessons_count(self):
        # Courses built in the back office keep their lessons in LessonVideo;
        # `curriculum` is the older embedded outline some catalogue entries use.
        from apps.learning.models import LessonVideo

        real = LessonVideo.objects(course=self, is_published=True).count()
        return real or sum(len(section.lessons) for section in self.curriculum)

    @property
    def parts_count(self):
        from apps.learning.models import Part

        real = Part.objects(course=self, is_published=True).count()
        return real or len(self.curriculum)


class Enrollment(Document):
    meta = {"collection": "enrollments", "indexes": [("user", "course"), "-last_activity"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    progress = IntField(default=0)  # percent
    completed_lessons = IntField(default=0)
    minutes_spent = IntField(default=0)
    certificate_url = StringField(default="")
    enrolled_at = DateTimeField(default=datetime.utcnow)
    last_activity = DateTimeField(default=datetime.utcnow)


class Review(Document):
    meta = {"collection": "reviews", "indexes": ["course", "-created_at"]}

    course = ReferenceField(Course, required=True, reverse_delete_rule=2)
    user = ReferenceField(User, reverse_delete_rule=2)
    author_name = StringField(default="")
    rating = IntField(default=5, min_value=1, max_value=5)
    body = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)


class CartItem(EmbeddedDocument):
    item_type = StringField(choices=("course", "exam", "exam_code", "plan"), default="course")
    item_id = StringField(required=True)
    slug = StringField(default="")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    cover = StringField(default="")
    price = IntField(default=0)
    quantity = IntField(default=1)
    added_at = DateTimeField(default=datetime.utcnow)


class Cart(Document):
    meta = {"collection": "carts", "indexes": ["user"]}

    user = ReferenceField(User, required=True, unique=True, reverse_delete_rule=2)
    items = EmbeddedDocumentListField(CartItem, default=list)
    coupon = StringField(default="")
    updated_at = DateTimeField(default=datetime.utcnow)

    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items)

    @property
    def discount(self):
        # Single demo coupon until the promotions phase lands.
        return int(self.subtotal * 0.15) if self.coupon.upper() == "GOTEH15" else 0

    @property
    def total(self):
        return max(self.subtotal - self.discount, 0)


class OrderItem(EmbeddedDocument):
    item_type = StringField(default="course")
    item_id = StringField(default="")
    slug = StringField(default="")
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    price = IntField(default=0)
    quantity = IntField(default=1)


class Order(Document):
    meta = {"collection": "orders", "indexes": ["user", "-created_at", "code"]}

    code = StringField(required=True, unique=True)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    items = EmbeddedDocumentListField(OrderItem, default=list)
    subtotal = IntField(default=0)
    discount = IntField(default=0)
    total = IntField(default=0)
    payment_method = StringField(choices=("wallet", "gateway"), default="wallet")
    status = StringField(choices=("pending", "paid", "failed", "refunded"), default="pending")
    created_at = DateTimeField(default=datetime.utcnow)
    paid_at = DateTimeField()
