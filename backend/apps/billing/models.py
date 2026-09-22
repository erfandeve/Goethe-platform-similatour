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


# --------------------------------------------------------------- discounts

COUPON_KINDS = ("percent", "amount")
# What a code may discount; an empty list means every item in the cart.
COUPON_TARGETS = ("course", "exam", "exam_code", "plan")


class CouponError(Exception):
    """Why a code cannot be used right now; `code` is what the client translates."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class Coupon(Document):
    """A discount code the back office hands out.

    `max_uses` caps redemptions across everyone (0 = unlimited) and
    `per_user_limit` caps them per learner (0 = unlimited). `used_count` only
    ever moves inside `redeem()`, with a conditional update, so two learners
    checking out at once cannot push a code past its cap.
    """

    meta = {"collection": "coupons", "indexes": ["code", "-created_at"]}

    code = StringField(required=True, unique=True)
    kind = StringField(choices=COUPON_KINDS, default="percent")
    value = IntField(default=10)            # percent (1–100) or Rial off
    max_discount = IntField(default=0)      # Rial cap on a percent code; 0 = none
    min_total = IntField(default=0)         # smallest eligible subtotal, Rial
    applies_to = ListField(StringField(choices=COUPON_TARGETS), default=list)

    starts_at = DateTimeField()
    expires_at = DateTimeField()
    max_uses = IntField(default=0)
    per_user_limit = IntField(default=1)
    used_count = IntField(default=0)

    is_active = BooleanField(default=True)
    note = StringField(default="")          # who it was for, why — staff only
    created_at = DateTimeField(default=datetime.utcnow)

    @staticmethod
    def normalize(code):
        return (code or "").strip().upper().replace(" ", "")

    @classmethod
    def lookup(cls, code):
        code = cls.normalize(code)
        return cls.objects(code=code).first() if code else None

    @property
    def status(self):
        """One word for the back office list."""
        now = datetime.utcnow()
        if not self.is_active:
            return "inactive"
        if self.starts_at and self.starts_at > now:
            return "scheduled"
        if self.expires_at and self.expires_at <= now:
            return "expired"
        if self.max_uses and self.used_count >= self.max_uses:
            return "used_up"
        return "active"

    def eligible_subtotal(self, items):
        return sum(
            item.price * item.quantity
            for item in items
            if not self.applies_to or item.item_type in self.applies_to
        )

    def discount_for(self, items):
        """Rial off these items; never more than what they cost."""
        base = self.eligible_subtotal(items)
        if base <= 0:
            return 0
        if self.kind == "percent":
            off = base * max(0, min(self.value, 100)) // 100
            if self.max_discount:
                off = min(off, self.max_discount)
        else:
            off = self.value
        return max(0, min(off, base))

    def check(self, user, items):
        """Raise CouponError unless `user` may use this code on `items`."""
        state = self.status
        if state == "inactive":
            raise CouponError("invalid_coupon", "Coupon code is not valid.")
        if state == "scheduled":
            raise CouponError("coupon_not_started", "This code is not active yet.")
        if state == "expired":
            raise CouponError("coupon_expired", "This code has expired.")
        if state == "used_up":
            raise CouponError("coupon_used_up", "This code has been fully used.")
        if self.per_user_limit and user is not None:
            mine = CouponRedemption.objects(coupon=self, user=user).count()
            if mine >= self.per_user_limit:
                raise CouponError("coupon_already_used", "You have already used this code.")
        if self.eligible_subtotal(items) <= 0:
            raise CouponError("coupon_not_applicable", "This code does not apply to your cart.")
        if self.min_total and sum(i.price * i.quantity for i in items) < self.min_total:
            raise CouponError(
                "coupon_min_total", "Your cart total is below this code's minimum."
            )
        return self.discount_for(items)

    def redeem(self, user, order_code, amount):
        """Count one use; False if the cap was reached a moment ago."""
        query = Coupon.objects(id=self.id, is_active=True)
        if self.max_uses:
            query = query.filter(used_count__lt=self.max_uses)
        if not query.update_one(inc__used_count=1):
            return False
        CouponRedemption(coupon=self, user=user, order_code=order_code, amount=amount).save()
        self.reload()
        return True


class CouponRedemption(Document):
    meta = {"collection": "coupon_redemptions", "indexes": [("coupon", "user"), "-created_at"]}

    coupon = ReferenceField(Coupon, required=True, reverse_delete_rule=2)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    order_code = StringField(default="")
    amount = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
