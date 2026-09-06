"""Subscriptions: one payment that unlocks a whole tier of the catalogue.

A plan lists what it opens up. Access checks ask the subscription first and fall
back to per-item purchases, so buying a single exam still works exactly as before.
"""

from datetime import datetime, timedelta

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocumentField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from apps.accounts.models import User
from apps.core.i18n import TranslatedText

# What a plan may unlock. Tiers are additive in practice but stored explicitly,
# so a new plan can mix them without code changes.
PERKS = (
    "exam_codes",   # every sitting of the exams the learner can open
    "exams",        # every exam
    "courses",      # every course
    "speaking",     # the AI speaking courses
    "podcasts",     # premium episodes
)


class Plan(Document):
    meta = {"collection": "plans", "indexes": ["slug", "order"]}

    slug = StringField(required=True, unique=True)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    perks = ListField(StringField(choices=PERKS), default=list)
    highlights = ListField(EmbeddedDocumentField(TranslatedText), default=list)

    price = IntField(default=0)          # Rial
    duration_days = IntField(default=365)
    accent = StringField(default="#6d5efc")
    badge = StringField(default="")
    order = IntField(default=0)
    is_published = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    def grants(self, perk):
        return perk in self.perks


class Subscription(Document):
    meta = {"collection": "subscriptions", "indexes": [("user", "-expires_at"), "-created_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    plan = ReferenceField(Plan, required=True, reverse_delete_rule=2)
    order_code = StringField(default="")
    started_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField(required=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    @property
    def is_valid(self):
        return self.is_active and self.expires_at > datetime.utcnow()

    @classmethod
    def start(cls, user, plan, order_code=""):
        """Extend a running subscription rather than stacking a second one."""
        current = cls.objects(user=user, plan=plan, is_active=True).order_by("-expires_at").first()
        base = (
            current.expires_at
            if current and current.expires_at > datetime.utcnow()
            else datetime.utcnow()
        )
        if current and current.expires_at > datetime.utcnow():
            current.expires_at = base + timedelta(days=plan.duration_days)
            current.save()
            return current
        return cls.objects.create(
            user=user,
            plan=plan,
            order_code=order_code,
            expires_at=base + timedelta(days=plan.duration_days),
        )


def active_perks(user):
    """Every perk the learner currently holds, across all their plans."""
    if not user:
        return set()
    perks = set()
    for subscription in Subscription.objects(user=user, is_active=True):
        if subscription.is_valid and subscription.plan:
            perks.update(subscription.plan.perks)
    return perks


def has_perk(user, perk):
    return perk in active_perks(user)
