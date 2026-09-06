import re
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.core.exceptions import ApiError
from apps.core.pagination import paginate

from .auth import decode, issue_tokens
from .models import Message, Notification, User, WalletTransaction
from .permissions import IsAuthenticated
from .serializers import (
    message_item,
    notification_item,
    transaction_item,
    user_detail,
)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
EDITABLE_FIELDS = (
    "first_name",
    "last_name",
    "phone",
    "avatar",
    "bio",
    "birth_date",
    "country",
    "city",
    "native_language",
    "preferred_locale",
    "current_level",
    "target_level",
)


@api_view(["POST"])
def register(request):
    data = request.data or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    errors = {}

    if not EMAIL_RE.match(email):
        errors["email"] = "Enter a valid email address."
    if len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."
    if email and User.objects(email=email).first():
        errors["email"] = "This email is already registered."
    if errors:
        raise ApiError("Validation failed.", code="invalid", fields=errors)

    user = User(
        email=email,
        first_name=(data.get("first_name") or "").strip(),
        last_name=(data.get("last_name") or "").strip(),
        phone=(data.get("phone") or "").strip(),
        preferred_locale=data.get("locale") if data.get("locale") in ("fa", "en", "de") else "fa",
    )
    user.set_password(password)
    user.save()

    Notification(
        user=user,
        title="Willkommen bei GOTEH!",
        body="Your account is ready. Take the free placement test to find your level.",
        kind="system",
        link="/exams",
    ).save()

    return Response({"user": user_detail(user), "tokens": issue_tokens(user)}, status=201)


@api_view(["POST"])
def login(request):
    data = request.data or {}
    email = (data.get("email") or "").strip().lower()
    user = User.objects(email=email).first()
    if not user or not user.check_password(data.get("password") or ""):
        raise ApiError("Email or password is incorrect.", code="invalid_credentials", status_code=401)
    if not user.is_active:
        raise ApiError("This account is disabled.", code="disabled", status_code=403)

    user.last_login = datetime.utcnow()
    user.save()
    return Response({"user": user_detail(user), "tokens": issue_tokens(user)})


@api_view(["POST"])
def refresh(request):
    token = (request.data or {}).get("refresh")
    if not token:
        raise ApiError("Refresh token is required.", status_code=400)
    payload = decode(token, expected_type="refresh")
    user = User.objects(id=payload["sub"], is_active=True).first()
    if not user:
        raise ApiError("User not found.", status_code=401)
    return Response({"tokens": issue_tokens(user)})


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    if request.method == "PATCH":
        data = request.data or {}
        for field in EDITABLE_FIELDS:
            if field in data:
                setattr(user, field, data[field])
        prefs = data.get("prefs")
        if isinstance(prefs, dict) and user.prefs:
            for key in ("email", "sms", "product_news"):
                if key in prefs:
                    setattr(user.prefs, key, bool(prefs[key]))
        user.save()
    return Response(user_detail(user))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    data = request.data or {}
    if not request.user.check_password(data.get("current_password") or ""):
        raise ApiError(
            "Current password is incorrect.",
            fields={"current_password": "Incorrect password."},
        )
    new_password = data.get("new_password") or ""
    if len(new_password) < 8:
        raise ApiError(
            "Password too short.",
            fields={"new_password": "Password must be at least 8 characters."},
        )
    request.user.set_password(new_password)
    request.user.save()
    return Response({"detail": "Password updated."})


# --- Wallet ------------------------------------------------------------------


def credit_wallet(user, amount, kind, title, reference=""):
    user.wallet_balance = int(user.wallet_balance or 0) + int(amount)
    if user.wallet_balance < 0:
        raise ApiError("Insufficient balance.", code="insufficient_funds")
    user.save()
    tx = WalletTransaction(
        user=user,
        amount=int(amount),
        balance_after=user.wallet_balance,
        kind=kind,
        title=title,
        reference=reference,
    )
    tx.save()
    return tx


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet(request):
    qs = WalletTransaction.objects(user=request.user).order_by("-created_at")
    items, meta = paginate(qs, request, default_size=15)
    return Response(
        {
            "balance": request.user.wallet_balance,
            "transactions": [transaction_item(tx) for tx in items],
            "meta": meta,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wallet_topup(request):
    """Mock gateway: real PSP callback replaces this in the payment phase."""
    try:
        amount = int((request.data or {}).get("amount", 0))
    except (TypeError, ValueError):
        raise ApiError("Amount must be a number.")
    if amount < 100000:
        raise ApiError("Minimum top-up is 100,000 Rial.", fields={"amount": "Too small."})
    tx = credit_wallet(request.user, amount, "topup", "Wallet top-up")
    return Response({"balance": request.user.wallet_balance, "transaction": transaction_item(tx)})


# --- Notifications & messages ------------------------------------------------


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notifications(request):
    qs = Notification.objects(user=request.user).order_by("-created_at")
    items, meta = paginate(qs, request, default_size=20)
    return Response(
        {
            "results": [notification_item(n) for n in items],
            "unread": Notification.objects(user=request.user, is_read=False).count(),
            "meta": meta,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_read(request, pk):
    n = Notification.objects(id=pk, user=request.user).first()
    if not n:
        raise ApiError("Notification not found.", status_code=404)
    n.is_read = True
    n.save()
    return Response(notification_item(n))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notifications_read_all(request):
    Notification.objects(user=request.user, is_read=False).update(set__is_read=True)
    return Response({"detail": "All notifications marked as read."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def messages(request):
    qs = Message.objects(user=request.user).order_by("-created_at")
    items, meta = paginate(qs, request, default_size=20)
    return Response(
        {
            "results": [message_item(m) for m in items],
            "unread": Message.objects(user=request.user, is_read=False).count(),
            "meta": meta,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def message_read(request, pk):
    m = Message.objects(id=pk, user=request.user).first()
    if not m:
        raise ApiError("Message not found.", status_code=404)
    m.is_read = True
    m.save()
    return Response(message_item(m))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def message_send(request):
    data = request.data or {}
    body = (data.get("body") or "").strip()
    if not body:
        raise ApiError("Message body is required.", fields={"body": "Required."})
    m = Message(
        user=request.user,
        sender_name=request.user.full_name,
        sender_role="student",
        subject=(data.get("subject") or "Support request").strip(),
        thread=(data.get("thread") or "support").strip(),
        body=body,
        is_read=True,
    )
    m.save()
    return Response(message_item(m), status=201)


# --- Dashboard ---------------------------------------------------------------


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    from apps.courses.models import Enrollment
    from apps.courses.serializers import enrollment_item
    from apps.exams.models import ExamAttempt
    from apps.exams.serializers import attempt_item
    from apps.core.utils import get_locale

    locale = get_locale(request)
    user = request.user
    enrollments = list(Enrollment.objects(user=user).order_by("-last_activity")[:6])
    attempts = list(ExamAttempt.objects(user=user).order_by("-started_at")[:6])

    finished = [a for a in attempts if a.status == "finished"]
    avg_score = round(sum(a.score for a in finished) / len(finished)) if finished else 0
    minutes = sum(e.minutes_spent for e in Enrollment.objects(user=user))

    return Response(
        {
            "user": user_detail(user),
            "stats": {
                "courses": Enrollment.objects(user=user).count(),
                "completed_courses": Enrollment.objects(user=user, progress=100).count(),
                "exams_taken": ExamAttempt.objects(user=user, status="finished").count(),
                "average_score": avg_score,
                "minutes_spent": minutes,
                "streak_days": user_streak(user),
                "wallet_balance": user.wallet_balance,
            },
            "enrollments": [enrollment_item(e, locale) for e in enrollments],
            "attempts": [attempt_item(a, locale) for a in attempts],
            "unread_notifications": Notification.objects(user=user, is_read=False).count(),
            "unread_messages": Message.objects(user=user, is_read=False).count(),
        }
    )


def user_streak(user):
    """Consecutive days with any learning activity, counted back from today."""
    from apps.courses.models import Enrollment

    days = {
        e.last_activity.date()
        for e in Enrollment.objects(user=user)
        if e.last_activity
    }
    if not days:
        return 0
    streak, cursor = 0, datetime.utcnow().date()
    while cursor in days:
        streak += 1
        cursor = cursor.fromordinal(cursor.toordinal() - 1)
    return streak
