"""Back office for discount codes and the top-learners showcase."""

import secrets
from datetime import datetime

from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.models import User
from apps.accounts.permissions import IsStaff
from apps.billing.models import (
    COUPON_KINDS,
    COUPON_TARGETS,
    Coupon,
    CouponRedemption,
)
from apps.core.exceptions import ApiError

from .serializers import read_translated, translated

# ------------------------------------------------------------------ coupons

# No 0/O or 1/I, so a code read aloud or off a screenshot is typed right.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _iso(value):
    return value.isoformat() + "Z" if value else None


def _date(payload, key):
    """Accept ISO dates or datetimes; empty clears the bound."""
    raw = payload.get(key)
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        raise ApiError(f"'{key}' is not a valid date.", code="invalid", fields={key: "date"})


def _number(payload, key, *, minimum=0, maximum=None):
    try:
        value = int(payload.get(key) or 0)
    except (TypeError, ValueError):
        raise ApiError(f"'{key}' must be a number.", code="invalid", fields={key: "number"})
    if value < minimum or (maximum is not None and value > maximum):
        raise ApiError(f"'{key}' is out of range.", code="invalid", fields={key: "range"})
    return value


def _new_code():
    while True:
        code = "LX" + "".join(secrets.choice(CODE_ALPHABET) for _ in range(6))
        if not Coupon.objects(code=code).first():
            return code


def _coupon_row(coupon):
    return {
        "id": str(coupon.id),
        "code": coupon.code,
        "kind": coupon.kind,
        "value": coupon.value,
        "max_discount": coupon.max_discount,
        "min_total": coupon.min_total,
        "applies_to": coupon.applies_to,
        "starts_at": _iso(coupon.starts_at),
        "expires_at": _iso(coupon.expires_at),
        "max_uses": coupon.max_uses,
        "per_user_limit": coupon.per_user_limit,
        "used_count": coupon.used_count,
        "is_active": coupon.is_active,
        "note": coupon.note,
        "status": coupon.status,
        "created_at": _iso(coupon.created_at),
    }


def _apply_coupon(coupon, payload):
    if "code" in payload:
        code = Coupon.normalize(payload.get("code")) or _new_code()
        if not code.isalnum() or len(code) > 32:
            raise ApiError(
                "Codes are letters and digits only, up to 32.", code="invalid", fields={"code": "format"}
            )
        clash = Coupon.objects(code=code).first()
        if clash and clash.id != coupon.id:
            raise ApiError("This code already exists.", code="duplicate", fields={"code": "taken"})
        coupon.code = code

    if "kind" in payload:
        if payload["kind"] not in COUPON_KINDS:
            raise ApiError("Unknown discount kind.", code="invalid", fields={"kind": "choice"})
        coupon.kind = payload["kind"]
    if "value" in payload:
        coupon.value = _number(payload, "value", minimum=1)
    if coupon.kind == "percent" and not 1 <= coupon.value <= 100:
        raise ApiError("A percentage is between 1 and 100.", code="invalid", fields={"value": "range"})

    for key in ("max_discount", "min_total", "max_uses", "per_user_limit"):
        if key in payload:
            setattr(coupon, key, _number(payload, key))

    if "applies_to" in payload:
        targets = payload.get("applies_to") or []
        if not isinstance(targets, list) or any(t not in COUPON_TARGETS for t in targets):
            raise ApiError("Unknown item type.", code="invalid", fields={"applies_to": "choice"})
        coupon.applies_to = list(dict.fromkeys(targets))

    for key in ("starts_at", "expires_at"):
        if key in payload:
            setattr(coupon, key, _date(payload, key))
    if coupon.starts_at and coupon.expires_at and coupon.expires_at <= coupon.starts_at:
        raise ApiError(
            "The end date must be after the start date.", code="invalid", fields={"expires_at": "order"}
        )

    if "is_active" in payload:
        coupon.is_active = bool(payload["is_active"])
    if "note" in payload:
        coupon.note = str(payload.get("note") or "")[:300]


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def coupons(request):
    if request.method == "POST":
        payload = dict(request.data or {})
        payload.setdefault("code", "")
        coupon = Coupon()
        _apply_coupon(coupon, payload)
        coupon.save()
        return Response(_coupon_row(coupon), status=201)

    return Response(
        {
            "results": [_coupon_row(c) for c in Coupon.objects().order_by("-created_at")],
            "kinds": list(COUPON_KINDS),
            "targets": list(COUPON_TARGETS),
        }
    )


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def coupon_detail(request, pk):
    coupon = Coupon.objects(id=pk).first()
    if not coupon:
        raise ApiError("Coupon not found.", status_code=404)

    if request.method == "GET":
        uses = CouponRedemption.objects(coupon=coupon).order_by("-created_at")[:100]
        return Response(
            {
                **_coupon_row(coupon),
                "redemptions": [
                    {
                        "user": use.user.full_name if use.user else "—",
                        "email": use.user.email if use.user else "",
                        "order_code": use.order_code,
                        "amount": use.amount,
                        "created_at": _iso(use.created_at),
                    }
                    for use in uses
                ],
            }
        )

    if request.method == "DELETE":
        # A used code is part of order history; switch it off instead.
        if coupon.used_count:
            raise ApiError(
                "This code has been used; deactivate it instead of deleting it.",
                code="in_use",
                status_code=409,
            )
        coupon.delete()
        return Response(status=204)

    _apply_coupon(coupon, request.data or {})
    coupon.save()
    return Response(_coupon_row(coupon))


# ------------------------------------------------------------ top learners

SORTS = {
    "points": lambda row: row["stats"]["points"],
    "exam_score": lambda row: row["stats"]["exam_score"],
    "course_progress": lambda row: row["stats"]["course_progress"],
    "lessons": lambda row: row["stats"]["lessons_done"],
    "last_active": lambda row: row["stats"]["last_active"] or datetime.min,
    "joined": lambda row: row["joined"] or datetime.min,
}


def _learner_row(user, stats):
    return {
        "id": str(user.id),
        "name": user.full_name,
        "email": user.email,
        "avatar": user.avatar,
        "level": user.current_level,
        "target_level": user.target_level,
        "city": user.city,
        "joined": user.created_at,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "showcase_rank": user.showcase_rank,
        "showcase_note": translated(user.showcase_note),
        "stats": stats,
    }


def _serialize(row):
    stats = dict(row["stats"])
    stats["last_active"] = _iso(stats["last_active"])
    return {**row, "joined": _iso(row["joined"]), "stats": stats}


@api_view(["GET"])
@permission_classes([IsStaff])
def learners(request):
    """Every learner with their progress, searchable and sortable.

    Stats come from one aggregation per collection, so ranking the whole list
    costs the same as ranking a page.
    """
    from apps.learning.standing import EMPTY, standings

    query = (request.query_params.get("q") or "").strip()
    sort = request.query_params.get("sort") or "points"
    if sort not in SORTS:
        sort = "points"
    try:
        page = max(1, int(request.query_params.get("page") or 1))
    except ValueError:
        page = 1
    size = 25

    users = User.objects()
    if query:
        users = users.filter(
            Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone__icontains=query)
        )

    table = standings()
    rows = [_learner_row(user, table.get(str(user.id)) or dict(EMPTY)) for user in users]
    rows.sort(key=SORTS[sort], reverse=True)
    total = len(rows)
    chunk = rows[(page - 1) * size : page * size]

    podium = [
        _learner_row(user, table.get(str(user.id)) or dict(EMPTY))
        for user in User.objects(showcase_rank__gt=0).order_by("showcase_rank")
    ]

    return Response(
        {
            "results": [_serialize(row) for row in chunk],
            "podium": [_serialize(row) for row in podium],
            "meta": {"page": page, "size": size, "total": total, "pages": max(1, -(-total // size))},
            "sort": sort,
        }
    )


@api_view(["PATCH"])
@permission_classes([IsStaff])
def learner_showcase(request, pk):
    """Place a learner on the podium (rank 1–3) or take them off (0).

    A rank belongs to one learner at a time: giving it to someone moves the
    previous holder off the podium rather than leaving two "first places".
    """
    user = User.objects(id=pk).first()
    if not user:
        raise ApiError("Learner not found.", status_code=404)
    payload = request.data or {}

    if "rank" in payload:
        rank = _number(payload, "rank", minimum=0, maximum=3)
        if rank:
            User.objects(showcase_rank=rank, id__ne=user.id).update(set__showcase_rank=0)
        user.showcase_rank = rank
    if "note" in payload:
        user.showcase_note = read_translated(payload["note"], user.showcase_note)
    user.save()

    from apps.learning.standing import standings, stats_for

    return Response(_serialize(_learner_row(user, stats_for(user.id, standings([user.id])))))
