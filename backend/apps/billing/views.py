from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.permissions import IsAuthenticated
from apps.core.utils import get_locale

from .models import Plan, Subscription, active_perks
from .serializers import plan_item, subscription_item


@api_view(["GET"])
def plans(request):
    """The subscription tiers, with the viewer's own plans marked as owned."""
    locale = get_locale(request)
    user = getattr(request, "user", None)
    mine = (
        {
            str(subscription.plan.id)
            for subscription in Subscription.objects(user=user, is_active=True)
            if subscription.is_valid and subscription.plan
        }
        if user
        else set()
    )

    return Response(
        {
            "results": [
                plan_item(plan, locale, owned=str(plan.id) in mine)
                for plan in Plan.objects(is_published=True).order_by("order")
            ],
            "perks": sorted(active_perks(user)) if user else [],
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscriptions(request):
    locale = get_locale(request)
    records = Subscription.objects(user=request.user).order_by("-expires_at")
    return Response(
        {
            "results": [subscription_item(item, locale) for item in records],
            "perks": sorted(active_perks(request.user)),
        }
    )
