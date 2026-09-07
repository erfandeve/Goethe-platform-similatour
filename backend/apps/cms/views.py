"""Public reads for the editable content."""

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.core.exceptions import ApiError
from apps.core.utils import get_locale

from .models import Article, HomeSection
from .serializers import article_card, article_detail


@api_view(["GET"])
def articles(request):
    locale = get_locale(request)
    rows = Article.objects(is_published=True).order_by("order", "-published_at")
    return Response({"results": [article_card(a, locale) for a in rows]})


@api_view(["GET"])
def article(request, slug):
    locale = get_locale(request)
    found = Article.objects(slug=slug, is_published=True).first()
    if not found:
        raise ApiError("Article not found.", status_code=404)

    related = [
        article_card(a, locale)
        for a in Article.objects(slug__in=found.related, is_published=True)
    ]
    return Response({**article_detail(found, locale), "related": related})


def published_sections(locale):
    """Used by the home payload so the page arrives in one request."""
    from .serializers import section_public

    rows = HomeSection.objects(is_published=True).order_by("order")
    return [section_public(section, locale) for section in rows]
