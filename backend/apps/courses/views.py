import random
import string
from datetime import datetime

from mongoengine.queryset.visitor import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.permissions import IsAuthenticated
from apps.accounts.models import Notification
from apps.accounts.views import credit_wallet
from apps.core.exceptions import ApiError
from apps.core.i18n import TranslatedText
from apps.core.pagination import paginate
from apps.core.utils import get_locale

from .models import (
    Cart,
    CartItem,
    Category,
    Course,
    Enrollment,
    Instructor,
    Order,
    OrderItem,
    Review,
)
from .serializers import (
    cart_detail,
    category_item,
    course_card,
    course_detail,
    enrollment_item,
    instructor_detail,
    order_item,
    review_item,
)

SORTS = {
    "newest": "-created_at",
    "popular": "-students_count",
    "rating": "-rating",
    "price_asc": "price",
    "price_desc": "-price",
}


@api_view(["GET"])
def course_list(request):
    locale = get_locale(request)
    params = request.query_params
    qs = Course.objects(is_published=True)

    for field in ("level", "language", "format"):
        values = [v for v in params.getlist(field) if v]
        if len(values) == 1 and "," in values[0]:
            values = values[0].split(",")
        if values:
            qs = qs.filter(**{f"{field}__in": values})

    category = params.get("category")
    if category:
        slugs = category.split(",")
        cats = Category.objects(slug__in=slugs, kind="course")
        qs = qs.filter(category__in=list(cats))

    if params.get("featured") == "true":
        qs = qs.filter(is_featured=True)
    if params.get("free") == "true":
        qs = qs.filter(price=0)

    for key, op in (("min_price", "price__gte"), ("max_price", "price__lte")):
        if params.get(key):
            try:
                qs = qs.filter(**{op: int(params[key])})
            except ValueError:
                pass

    search = (params.get("q") or "").strip()
    if search:
        qs = qs.filter(
            Q(title__fa__icontains=search)
            | Q(title__en__icontains=search)
            | Q(title__de__icontains=search)
            | Q(subtitle__en__icontains=search)
            | Q(tags__icontains=search)
        )

    qs = qs.order_by(SORTS.get(params.get("sort"), "-is_featured"), "-students_count")
    items, meta = paginate(qs, request)

    return Response(
        {
            "results": [course_card(c, locale) for c in items],
            "meta": meta,
            "facets": build_facets(locale),
        }
    )


def build_facets(locale):
    levels = Course.objects(is_published=True).item_frequencies("level")
    languages = Course.objects(is_published=True).item_frequencies("language")
    formats = Course.objects(is_published=True).item_frequencies("format")
    categories = []
    for cat in Category.objects(kind="course").order_by("order"):
        categories.append(
            {
                **category_item(cat, locale),
                "count": Course.objects(category=cat, is_published=True).count(),
            }
        )
    return {
        "levels": [{"value": k, "count": v} for k, v in sorted(levels.items()) if k],
        "languages": [{"value": k, "count": v} for k, v in languages.items() if k],
        "formats": [{"value": k, "count": v} for k, v in formats.items() if k],
        "categories": categories,
        "price_range": {
            "min": 0,
            "max": max([c.price for c in Course.objects(is_published=True)] or [0]),
        },
    }


@api_view(["GET"])
def course_detail_view(request, slug):
    locale = get_locale(request)
    course = Course.objects(slug=slug, is_published=True).first()
    if not course:
        raise ApiError("Course not found.", status_code=404)
    reviews = Review.objects(course=course).order_by("-created_at")[:8]
    data = course_detail(course, locale, reviews)
    related = Course.objects(
        level=course.level, is_published=True, id__ne=course.id
    ).order_by("-students_count")[:4]
    data["related"] = [course_card(c, locale) for c in related]
    if getattr(request, "user", None):
        data["is_enrolled"] = bool(
            Enrollment.objects(user=request.user, course=course).first()
        )
    return Response(data)


@api_view(["GET"])
def category_list(request):
    locale = get_locale(request)
    kind = request.query_params.get("kind", "course")
    cats = Category.objects(kind=kind).order_by("order")
    return Response(
        {
            "results": [
                {
                    **category_item(c, locale),
                    "count": Course.objects(category=c, is_published=True).count()
                    if kind == "course"
                    else 0,
                }
                for c in cats
            ]
        }
    )


@api_view(["GET"])
def instructor_list(request):
    locale = get_locale(request)
    items = Instructor.objects.order_by("-is_featured", "-students")
    return Response({"results": [instructor_detail(i, locale) for i in items]})


# --- Cart --------------------------------------------------------------------


def get_cart(user):
    cart = Cart.objects(user=user).first()
    if not cart:
        cart = Cart(user=user)
        cart.save()
    return cart


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_view(request):
    return Response(cart_detail(get_cart(request.user), get_locale(request)))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_add(request):
    from apps.exams.models import Exam

    locale = get_locale(request)
    data = request.data or {}
    item_type = data.get("item_type", "course")
    slug = data.get("slug")
    cart = get_cart(request.user)

    if item_type == "course":
        obj = Course.objects(slug=slug, is_published=True).first()
        if not obj:
            raise ApiError("Course not found.", status_code=404)
        if Enrollment.objects(user=request.user, course=obj).first():
            raise ApiError("You are already enrolled in this course.", code="already_enrolled")
        price, cover, title = obj.effective_price, obj.cover, obj.title

    elif item_type == "exam":
        obj = Exam.objects(slug=slug, is_published=True).first()
        if not obj:
            raise ApiError("Exam not found.", status_code=404)
        price, cover, title = obj.effective_price, obj.cover, obj.title

    elif item_type == "exam_code":
        from apps.exams.models import ExamCode

        obj = ExamCode.objects(id=data.get("id"), is_published=True).first()
        if not obj:
            raise ApiError("Exam code not found.", status_code=404)
        # Each sitting is priced on its own, so buying a second code costs
        # whatever that code is worth rather than a discount off the first.
        exam = obj.exam
        price = obj.effective_price
        cover, title = exam.cover, obj.label if obj.label.de or obj.label.fa else exam.title

    elif item_type == "plan":
        from apps.billing.models import Plan

        obj = Plan.objects(slug=slug, is_published=True).first()
        if not obj:
            raise ApiError("Plan not found.", status_code=404)
        price, cover, title = obj.price, "", obj.title

    else:
        raise ApiError("Unsupported item type.")

    if any(i.item_id == str(obj.id) for i in cart.items):
        raise ApiError("Item is already in your cart.", code="duplicate_item")

    cart.items.append(
        CartItem(
            item_type=item_type,
            item_id=str(obj.id),
            # A code has no slug of its own; link back to the exam it belongs to.
            slug=getattr(obj, "slug", None) or (obj.exam.slug if item_type == "exam_code" else ""),
            title=title,
            cover=cover,
            price=price,
        )
    )
    cart.updated_at = datetime.utcnow()
    cart.save()
    return Response(cart_detail(cart, locale), status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_remove(request):
    cart = get_cart(request.user)
    item_id = (request.data or {}).get("item_id")
    cart.items = [i for i in cart.items if i.item_id != item_id]
    cart.updated_at = datetime.utcnow()
    cart.save()
    return Response(cart_detail(cart, get_locale(request)))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_coupon(request):
    cart = get_cart(request.user)
    code = ((request.data or {}).get("coupon") or "").strip().upper()
    if code and code != "GOTEH15":
        raise ApiError("Coupon code is not valid.", code="invalid_coupon")
    cart.coupon = code
    cart.save()
    return Response(cart_detail(cart, get_locale(request)))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    locale = get_locale(request)
    user = request.user
    cart = get_cart(user)
    if not cart.items:
        raise ApiError("Your cart is empty.", code="empty_cart")

    total = cart.total
    method = (request.data or {}).get("payment_method", "wallet")
    if method == "wallet" and user.wallet_balance < total:
        raise ApiError(
            "Wallet balance is not enough.",
            code="insufficient_funds",
            fields={"needed": total - user.wallet_balance},
        )

    order = Order(
        code="GO-" + "".join(random.choices(string.digits, k=8)),
        user=user,
        items=[
            OrderItem(
                item_type=i.item_type,
                item_id=i.item_id,
                slug=i.slug,
                title=i.title,
                price=i.price,
                quantity=i.quantity,
            )
            for i in cart.items
        ],
        subtotal=cart.subtotal,
        discount=cart.discount,
        total=total,
        payment_method=method,
        status="paid",
        paid_at=datetime.utcnow(),
    )
    order.save()

    if method == "wallet" and total:
        credit_wallet(user, -total, "purchase", f"Order {order.code}", reference=order.code)

    for item in cart.items:
        if item.item_type == "course":
            course = Course.objects(id=item.item_id).first()
            if course and not Enrollment.objects(user=user, course=course).first():
                Enrollment(user=user, course=course).save()
                course.students_count += 1
                course.save()

        elif item.item_type == "exam":
            from apps.exams.models import ExamAccess

            if not ExamAccess.objects(user=user, exam=item.item_id, exam_code="").first():
                ExamAccess(user=user, exam=item.item_id, order_code=order.code).save()

        elif item.item_type == "exam_code":
            from apps.exams.models import ExamAccess, ExamCode

            code = ExamCode.objects(id=item.item_id).first()
            if code and not ExamAccess.objects(
                user=user, exam=str(code.exam.id), exam_code=str(code.id)
            ).first():
                ExamAccess(
                    user=user,
                    exam=str(code.exam.id),
                    exam_code=str(code.id),
                    order_code=order.code,
                ).save()

        elif item.item_type == "plan":
            from apps.billing.models import Plan, Subscription

            plan = Plan.objects(id=item.item_id).first()
            if plan:
                Subscription.start(user, plan, order_code=order.code)

    Notification(
        user=user,
        title=f"Order {order.code} confirmed",
        body="Your purchase is complete. Everything is now available in your panel.",
        kind="payment",
        link="/dashboard/orders",
    ).save()

    cart.items = []
    cart.coupon = ""
    cart.save()
    return Response(order_item(order, locale), status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list(request):
    locale = get_locale(request)
    qs = Order.objects(user=request.user).order_by("-created_at")
    items, meta = paginate(qs, request, default_size=10)
    return Response({"results": [order_item(o, locale) for o in items], "meta": meta})


# --- Enrollments -------------------------------------------------------------


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_courses(request):
    locale = get_locale(request)
    qs = Enrollment.objects(user=request.user).order_by("-last_activity")
    items, meta = paginate(qs, request, default_size=12)
    return Response({"results": [enrollment_item(e, locale) for e in items], "meta": meta})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enroll_free(request, slug):
    course = Course.objects(slug=slug, is_published=True).first()
    if not course:
        raise ApiError("Course not found.", status_code=404)
    if course.effective_price > 0:
        raise ApiError("This course is not free.", code="not_free")
    enrollment = Enrollment.objects(user=request.user, course=course).first()
    if not enrollment:
        enrollment = Enrollment(user=request.user, course=course)
        enrollment.save()
        course.students_count += 1
        course.save()
    return Response(enrollment_item(enrollment, get_locale(request)), status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_progress(request, slug):
    course = Course.objects(slug=slug).first()
    enrollment = Enrollment.objects(user=request.user, course=course).first()
    if not enrollment:
        raise ApiError("You are not enrolled in this course.", status_code=404)
    data = request.data or {}
    if "progress" in data:
        enrollment.progress = max(0, min(100, int(data["progress"])))
    if "completed_lessons" in data:
        enrollment.completed_lessons = int(data["completed_lessons"])
    if "minutes_spent" in data:
        enrollment.minutes_spent += int(data["minutes_spent"])
    enrollment.last_activity = datetime.utcnow()
    enrollment.save()
    return Response(enrollment_item(enrollment, get_locale(request)))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request, slug):
    course = Course.objects(slug=slug).first()
    if not course:
        raise ApiError("Course not found.", status_code=404)
    data = request.data or {}
    review = Review(
        course=course,
        user=request.user,
        author_name=request.user.full_name,
        rating=max(1, min(5, int(data.get("rating", 5)))),
        body=(data.get("body") or "").strip(),
    )
    review.save()
    ratings = [r.rating for r in Review.objects(course=course)]
    course.rating = round(sum(ratings) / len(ratings), 1)
    course.reviews_count = len(ratings)
    course.save()
    return Response(review_item(review), status=201)
