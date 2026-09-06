from apps.core.i18n import t


def _iso(value):
    return value.isoformat() if value else None


def plan_item(plan, locale, *, owned=False):
    return {
        "id": str(plan.id),
        "slug": plan.slug,
        "title": t(plan.title, locale),
        "description": t(plan.description, locale),
        "highlights": [t(item, locale) for item in plan.highlights],
        "perks": plan.perks,
        "price": plan.price,
        "duration_days": plan.duration_days,
        "accent": plan.accent,
        "badge": plan.badge,
        "is_featured": plan.is_featured,
        "owned": owned,
    }


def subscription_item(subscription, locale):
    plan = subscription.plan
    return {
        "id": str(subscription.id),
        "plan": plan_item(plan, locale) if plan else None,
        "started_at": _iso(subscription.started_at),
        "expires_at": _iso(subscription.expires_at),
        "is_valid": subscription.is_valid,
    }
