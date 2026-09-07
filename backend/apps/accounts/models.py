from datetime import datetime

import bcrypt
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")


class NotificationPrefs(EmbeddedDocument):
    email = BooleanField(default=True)
    sms = BooleanField(default=False)
    product_news = BooleanField(default=True)


class User(Document):
    meta = {
        "collection": "users",
        "indexes": ["email", "phone", "-created_at"],
    }

    email = EmailField(required=True, unique=True)
    phone = StringField(max_length=20)
    password_hash = StringField(required=True)

    first_name = StringField(max_length=80, default="")
    last_name = StringField(max_length=80, default="")
    avatar = StringField(default="")
    bio = StringField(default="")
    birth_date = StringField(default="")  # ISO date, kept as string for calendar flexibility
    country = StringField(default="")
    city = StringField(default="")

    native_language = StringField(default="fa")
    preferred_locale = StringField(choices=("fa", "en", "de"), default="fa")
    current_level = StringField(choices=LEVELS, default="A1")
    target_level = StringField(choices=LEVELS, default="B1")

    wallet_balance = IntField(default=0)  # Rial
    prefs = EmbeddedDocumentField(NotificationPrefs, default=NotificationPrefs)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    email_verified = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()

    # DRF's request.user contract
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.email.split("@")[0]

    def set_password(self, raw):
        self.password_hash = bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw):
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(raw.encode(), self.password_hash.encode())
        except ValueError:
            return False

    @property
    def profile_completion(self):
        checks = [
            bool(self.first_name),
            bool(self.last_name),
            bool(self.phone),
            bool(self.avatar),
            bool(self.birth_date),
            bool(self.city),
            bool(self.bio),
            self.email_verified,
        ]
        return round(sum(checks) / len(checks) * 100)


class WalletTransaction(Document):
    meta = {"collection": "wallet_transactions", "indexes": ["user", "-created_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    amount = IntField(required=True)  # positive = credit, negative = debit
    balance_after = IntField(default=0)
    kind = StringField(
        choices=("topup", "purchase", "refund", "bonus", "withdraw"), default="topup"
    )
    title = StringField(default="")
    reference = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)


class Notification(Document):
    meta = {"collection": "notifications", "indexes": ["user", "-created_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    title = StringField(required=True)
    body = StringField(default="")
    kind = StringField(
        choices=("system", "course", "exam", "payment", "podcast"), default="system"
    )
    link = StringField(default="")
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)


class Message(Document):
    """Direct messages between a student and the academy staff/teachers."""

    meta = {"collection": "messages", "indexes": ["user", "-created_at"]}

    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    sender_name = StringField(default="Lexora")
    sender_role = StringField(choices=("staff", "teacher", "student"), default="staff")
    sender_avatar = StringField(default="")
    subject = StringField(default="")
    body = StringField(default="")
    thread = StringField(default="")
    attachments = ListField(StringField(), default=list)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
