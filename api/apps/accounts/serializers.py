"""Hand-rolled serializers.

mongoengine documents don't play well with DRF ModelSerializer, so responses are
built as plain dicts. Keeps the API shape explicit and easy to grep.
"""


def _iso(value):
    return value.isoformat() if value else None


def user_public(user):
    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "avatar": user.avatar,
        "current_level": user.current_level,
    }


def user_detail(user):
    return {
        "id": str(user.id),
        "email": user.email,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "avatar": user.avatar,
        "bio": user.bio,
        "birth_date": user.birth_date,
        "country": user.country,
        "city": user.city,
        "native_language": user.native_language,
        "preferred_locale": user.preferred_locale,
        "current_level": user.current_level,
        "target_level": user.target_level,
        "wallet_balance": user.wallet_balance,
        "profile_completion": user.profile_completion,
        "email_verified": user.email_verified,
        "is_staff": user.is_staff,
        "prefs": {
            "email": user.prefs.email if user.prefs else True,
            "sms": user.prefs.sms if user.prefs else False,
            "product_news": user.prefs.product_news if user.prefs else True,
        },
        "created_at": _iso(user.created_at),
        "last_login": _iso(user.last_login),
    }


def transaction_item(tx):
    return {
        "id": str(tx.id),
        "amount": tx.amount,
        "balance_after": tx.balance_after,
        "kind": tx.kind,
        "title": tx.title,
        "reference": tx.reference,
        "created_at": _iso(tx.created_at),
    }


def notification_item(n):
    return {
        "id": str(n.id),
        "title": n.title,
        "body": n.body,
        "kind": n.kind,
        "link": n.link,
        "is_read": n.is_read,
        "created_at": _iso(n.created_at),
    }


def message_item(m):
    return {
        "id": str(m.id),
        "sender_name": m.sender_name,
        "sender_role": m.sender_role,
        "sender_avatar": m.sender_avatar,
        "subject": m.subject,
        "body": m.body,
        "thread": m.thread,
        "attachments": m.attachments,
        "is_read": m.is_read,
        "created_at": _iso(m.created_at),
    }
