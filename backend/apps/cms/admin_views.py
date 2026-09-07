"""Back-office CRUD for the home page sections and the articles.

Staff only. Writes merge onto what is stored, so an editor working in one
language never wipes the other two.
"""

from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.permissions import IsStaff
from apps.adminpanel.serializers import read_translated
from apps.core.exceptions import ApiError
from apps.core.utils import slugify

from .models import (
    BLOCK_TYPES,
    SECTION_KINDS,
    Article,
    ArticleBlock,
    FaqItem,
    HomeSection,
    SectionItem,
    TableRow,
)
from .serializers import article_row, section_row


def _int(payload, key, default=0):
    try:
        return int(payload.get(key, default))
    except (TypeError, ValueError):
        raise ApiError(f"'{key}' must be a number.", code="invalid")


def _unique_key(model, field, seed, exclude=None):
    base = slugify(seed) or "item"
    candidate, suffix = base, 2
    while True:
        query = model.objects(**{field: candidate})
        if exclude:
            query = query.filter(id__ne=exclude)
        if not query.first():
            return candidate
        candidate, suffix = f"{base}-{suffix}", suffix + 1


# --------------------------------------------------------- home sections ---


def _apply_section(section, payload):
    for field in ("eyebrow", "title", "subtitle", "body", "image_alt", "cta_label"):
        if field in payload:
            setattr(section, field, read_translated(payload[field], getattr(section, field)))

    if "kind" in payload:
        if payload["kind"] not in SECTION_KINDS:
            raise ApiError(f"Unknown section kind '{payload['kind']}'.", code="invalid")
        section.kind = payload["kind"]

    if "items" in payload and isinstance(payload["items"], list):
        section.items = [
            SectionItem(
                title=read_translated(item.get("title")),
                body=read_translated(item.get("body")),
                icon=str(item.get("icon", ""))[:40],
            )
            for item in payload["items"]
        ]

    if "image_side" in payload and payload["image_side"] in ("start", "end"):
        section.image_side = payload["image_side"]

    for field in ("image", "cta_href", "accent"):
        if field in payload:
            setattr(section, field, str(payload[field] or "")[:300])

    if "order" in payload:
        section.order = _int(payload, "order", section.order)
    if "is_published" in payload:
        section.is_published = bool(payload["is_published"])


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def sections(request):
    if request.method == "POST":
        payload = request.data or {}
        seed = payload.get("key") or (payload.get("title") or {}).get("en") or "section"
        section = HomeSection(key=_unique_key(HomeSection, "key", seed))
        _apply_section(section, payload)
        if not section.order:
            last = HomeSection.objects().order_by("-order").first()
            section.order = (last.order + 10) if last else 10
        section.save()
        return Response(section_row(section), status=201)

    return Response(
        {
            "results": [section_row(s) for s in HomeSection.objects().order_by("order")],
            "kinds": list(SECTION_KINDS),
        }
    )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsStaff])
def section_detail(request, pk):
    section = HomeSection.objects(id=pk).first()
    if not section:
        raise ApiError("Section not found.", status_code=404)

    if request.method == "DELETE":
        section.delete()
        return Response(status=204)

    _apply_section(section, request.data or {})
    section.save()
    return Response(section_row(section))


@api_view(["POST"])
@permission_classes([IsStaff])
def reorder_sections(request):
    for index, pk in enumerate(request.data.get("ids", [])):
        HomeSection.objects(id=pk).update_one(set__order=(index + 1) * 10)
    return Response({"results": [section_row(s) for s in HomeSection.objects().order_by("order")]})


# ---------------------------------------------------------------- articles ---


def _block(payload):
    kind = payload.get("type", "p")
    if kind not in BLOCK_TYPES:
        raise ApiError(f"Unknown block type '{kind}'.", code="invalid")

    block = ArticleBlock(
        type=kind,
        text=read_translated(payload.get("text")),
        anchor=str(payload.get("anchor", ""))[:80],
        title=read_translated(payload.get("title")),
        label=read_translated(payload.get("label")),
        caption=read_translated(payload.get("caption")),
        href=str(payload.get("href", ""))[:300],
        items=[read_translated(item) for item in payload.get("items", []) or []],
        head=[read_translated(cell) for cell in payload.get("head", []) or []],
        rows=[
            TableRow(cells=[read_translated(cell) for cell in row or []])
            for row in payload.get("rows", []) or []
        ],
    )
    # A heading needs a stable anchor for the table of contents to link to.
    if kind == "h2" and not block.anchor:
        seed = block.text.en or block.text.de or block.text.fa
        block.anchor = slugify(seed) or "section"
    return block


def _apply_article(article, payload):
    for field in (
        "title",
        "meta_title",
        "meta_description",
        "excerpt",
        "focus_keyword",
        "keywords",
    ):
        if field in payload:
            setattr(article, field, read_translated(payload[field], getattr(article, field)))

    if "body" in payload and isinstance(payload["body"], list):
        article.body = [_block(block) for block in payload["body"]]

    if "faq" in payload and isinstance(payload["faq"], list):
        article.faq = [
            FaqItem(
                question=read_translated(item.get("question")),
                answer=read_translated(item.get("answer")),
            )
            for item in payload["faq"]
        ]

    if "related" in payload and isinstance(payload["related"], list):
        article.related = [str(slug) for slug in payload["related"] if slug][:4]

    if "cover" in payload:
        article.cover = str(payload["cover"] or "")[:300]
    for field in ("reading_minutes", "order"):
        if field in payload:
            setattr(article, field, max(0, _int(payload, field, getattr(article, field))))
    if "is_published" in payload:
        article.is_published = bool(payload["is_published"])

    article.updated_at = datetime.utcnow()


@api_view(["GET", "POST"])
@permission_classes([IsStaff])
def articles(request):
    if request.method == "POST":
        payload = request.data or {}
        title = payload.get("title") or {}
        seed = payload.get("slug") or title.get("en") or title.get("de") or title.get("fa")
        article = Article(slug=_unique_key(Article, "slug", seed or "article"))
        _apply_article(article, payload)
        article.save()
        return Response(article_row(article), status=201)

    rows = Article.objects().order_by("order", "-published_at")
    return Response(
        {"results": [article_row(a) for a in rows], "block_types": list(BLOCK_TYPES)}
    )


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsStaff])
def article_detail(request, pk):
    article = Article.objects(id=pk).first()
    if not article:
        raise ApiError("Article not found.", status_code=404)

    if request.method == "DELETE":
        article.delete()
        return Response(status=204)

    if request.method == "PATCH":
        _apply_article(article, request.data or {})
        article.save()

    return Response(article_row(article, with_body=True))
