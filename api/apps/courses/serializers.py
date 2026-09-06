from apps.core.i18n import t


def _iso(value):
    return value.isoformat() if value else None


def instructor_item(instructor, locale):
    if not instructor:
        return None
    return {
        "id": str(instructor.id),
        "slug": instructor.slug,
        "name": instructor.name,
        "avatar": instructor.avatar,
        "headline": t(instructor.headline, locale),
        "rating": instructor.rating,
        "students": instructor.students,
    }


def instructor_detail(instructor, locale):
    data = instructor_item(instructor, locale) or {}
    if instructor:
        data["bio"] = t(instructor.bio, locale)
        data["languages"] = instructor.languages
    return data


def category_item(category, locale):
    if not category:
        return None
    return {
        "id": str(category.id),
        "slug": category.slug,
        "kind": category.kind,
        "title": t(category.title, locale),
        "description": t(category.description, locale),
        "icon": category.icon,
        "color": category.color,
    }


def course_card(course, locale):
    return {
        "id": str(course.id),
        "slug": course.slug,
        "title": t(course.title, locale),
        "subtitle": t(course.subtitle, locale),
        "cover": course.cover,
        "accent": course.accent,
        "level": course.level,
        "language": course.language,
        "format": course.format,
        "price": course.price,
        "discount_price": course.discount_price,
        "effective_price": course.effective_price,
        "duration_minutes": course.duration_minutes,
        "lessons_count": course.lessons_count,
        "parts_count": course.parts_count,
        "sessions_count": course.sessions_count,
        "rating": course.rating,
        "reviews_count": course.reviews_count,
        "students_count": course.students_count,
        "is_featured": course.is_featured,
        "is_bestseller": course.is_bestseller,
        "tags": course.tags,
        "category": category_item(course.category, locale),
        "instructor": instructor_item(course.instructor, locale),
    }


def course_detail(course, locale, reviews=None):
    data = course_card(course, locale)
    data.update(
        {
            "description": t(course.description, locale),
            "trailer_url": course.trailer_url,
            "starts_at": _iso(course.starts_at),
            "created_at": _iso(course.created_at),
            "outcomes": [t(o, locale) for o in course.outcomes],
            "requirements": [t(r, locale) for r in course.requirements],
            "instructor": instructor_detail(course.instructor, locale),
            "curriculum": course_curriculum(course, locale),
            "reviews": [review_item(r) for r in (reviews or [])],
        }
    )
    return data


def course_curriculum(course, locale):
    """The chapter list, preferring real lessons over the embedded outline."""
    from apps.learning.models import LessonVideo, Part

    parts = list(Part.objects(course=course, is_published=True).order_by("order"))
    if parts:
        return [
            {
                "title": t(part.title, locale) or part.title_de or part.slug,
                "lessons": [
                    {
                        "title": t(video.title, locale) or video.title_de or video.slug,
                        "duration_minutes": round((video.duration_seconds or 0) / 60) or 1,
                        "kind": "video",
                        "is_preview": video.order <= 1,
                    }
                    for video in LessonVideo.objects(
                        part=part, is_published=True
                    ).order_by("order")
                ],
            }
            for part in parts
        ]

    return [
        {
            "title": t(section.title, locale),
            "lessons": [
                {
                    "title": t(lesson.title, locale),
                    "duration_minutes": lesson.duration_minutes,
                    "kind": lesson.kind,
                    "is_preview": lesson.is_preview,
                }
                for lesson in section.lessons
            ],
        }
        for section in course.curriculum
    ]


def review_item(review):
    return {
        "id": str(review.id),
        "author_name": review.author_name,
        "rating": review.rating,
        "body": review.body,
        "created_at": _iso(review.created_at),
    }


def enrollment_item(enrollment, locale):
    course = enrollment.course
    return {
        "id": str(enrollment.id),
        "progress": enrollment.progress,
        "completed_lessons": enrollment.completed_lessons,
        "minutes_spent": enrollment.minutes_spent,
        "certificate_url": enrollment.certificate_url,
        "enrolled_at": _iso(enrollment.enrolled_at),
        "last_activity": _iso(enrollment.last_activity),
        "course": course_card(course, locale) if course else None,
    }


def cart_item(item, locale):
    return {
        "item_type": item.item_type,
        "item_id": item.item_id,
        "slug": item.slug,
        "title": t(item.title, locale),
        "cover": item.cover,
        "price": item.price,
        "quantity": item.quantity,
    }


def cart_detail(cart, locale):
    return {
        "items": [cart_item(i, locale) for i in cart.items],
        "count": sum(i.quantity for i in cart.items),
        "subtotal": cart.subtotal,
        "discount": cart.discount,
        "total": cart.total,
        "coupon": cart.coupon,
    }


def order_item(order, locale):
    return {
        "id": str(order.id),
        "code": order.code,
        "items": [
            {
                "item_type": i.item_type,
                "slug": i.slug,
                "title": t(i.title, locale),
                "price": i.price,
                "quantity": i.quantity,
            }
            for i in order.items
        ],
        "subtotal": order.subtotal,
        "discount": order.discount,
        "total": order.total,
        "status": order.status,
        "payment_method": order.payment_method,
        "created_at": _iso(order.created_at),
        "paid_at": _iso(order.paid_at),
    }
