"""Public and back-office shapes for the editable content.

Public reads resolve to one language; the back office gets the raw `{fa,en,de}`
objects so a save cannot silently flatten the other two translations.
"""

from apps.adminpanel.serializers import translated
from apps.core.i18n import t


def _paragraphs(field, locale):
    """A textarea becomes paragraphs: blank lines separate, single ones join."""
    raw = t(field, locale)
    return [block.strip() for block in raw.split("\n\n") if block.strip()]


# ----------------------------------------------------------------- public ---


def section_public(section, locale):
    return {
        "key": section.key,
        "kind": section.kind,
        "eyebrow": t(section.eyebrow, locale),
        "title": t(section.title, locale),
        "subtitle": t(section.subtitle, locale),
        "paragraphs": _paragraphs(section.body, locale),
        "items": [
            {
                "title": t(item.title, locale),
                "body": t(item.body, locale),
                "icon": item.icon,
            }
            for item in section.items
        ],
        "image": section.image,
        "image_alt": t(section.image_alt, locale) or t(section.title, locale),
        "image_side": section.image_side,
        "cta_label": t(section.cta_label, locale),
        "cta_href": section.cta_href,
        "accent": section.accent,
    }


def _block_public(block, locale):
    row = {"type": block.type}
    text = t(block.text, locale)

    if block.type in ("p", "h2", "h3", "quote"):
        row["text"] = text
        if block.type == "h2":
            row["id"] = block.anchor
    elif block.type in ("ul", "ol"):
        row["items"] = [t(item, locale) for item in block.items]
    elif block.type == "callout":
        row["title"] = t(block.title, locale)
        row["text"] = text
    elif block.type == "cta":
        row["title"] = t(block.title, locale)
        row["text"] = text
        row["label"] = t(block.label, locale)
        row["href"] = block.href
    elif block.type == "table":
        row["head"] = [t(cell, locale) for cell in block.head]
        row["rows"] = [[t(cell, locale) for cell in r.cells] for r in block.rows]
        caption = t(block.caption, locale)
        if caption:
            row["caption"] = caption

    return row


def article_card(article, locale):
    return {
        "slug": article.slug,
        "title": t(article.title, locale),
        "excerpt": t(article.excerpt, locale),
        "focus_keyword": t(article.focus_keyword, locale),
        "cover": article.cover,
        "reading_minutes": article.reading_minutes,
        "words": article.word_count(locale),
        "published_at": article.published_at.isoformat() if article.published_at else None,
        "updated_at": article.updated_at.isoformat() if article.updated_at else None,
    }


def article_detail(article, locale):
    return {
        **article_card(article, locale),
        "meta_title": t(article.meta_title, locale) or t(article.title, locale),
        "meta_description": t(article.meta_description, locale) or t(article.excerpt, locale),
        "keywords": [
            word.strip() for word in t(article.keywords, locale).split(",") if word.strip()
        ],
        "body": [_block_public(block, locale) for block in article.body],
        "faq": [
            {"q": t(item.question, locale), "a": t(item.answer, locale)} for item in article.faq
        ],
    }


# ------------------------------------------------------------ back office ---


def section_row(section):
    return {
        "id": str(section.id),
        "key": section.key,
        "kind": section.kind,
        "eyebrow": translated(section.eyebrow),
        "title": translated(section.title),
        "subtitle": translated(section.subtitle),
        "body": translated(section.body),
        "items": [
            {"title": translated(item.title), "body": translated(item.body), "icon": item.icon}
            for item in section.items
        ],
        "image": section.image,
        "image_alt": translated(section.image_alt),
        "image_side": section.image_side,
        "cta_label": translated(section.cta_label),
        "cta_href": section.cta_href,
        "accent": section.accent,
        "order": section.order,
        "is_published": section.is_published,
    }


def _block_row(block):
    return {
        "type": block.type,
        "text": translated(block.text),
        "anchor": block.anchor,
        "items": [translated(item) for item in block.items],
        "head": [translated(cell) for cell in block.head],
        "rows": [[translated(cell) for cell in row.cells] for row in block.rows],
        "caption": translated(block.caption),
        "title": translated(block.title),
        "label": translated(block.label),
        "href": block.href,
    }


def article_row(article, *, with_body=False):
    row = {
        "id": str(article.id),
        "slug": article.slug,
        "title": translated(article.title),
        "meta_title": translated(article.meta_title),
        "meta_description": translated(article.meta_description),
        "excerpt": translated(article.excerpt),
        "focus_keyword": translated(article.focus_keyword),
        "keywords": translated(article.keywords),
        "cover": article.cover,
        "related": article.related,
        "reading_minutes": article.reading_minutes,
        "is_published": article.is_published,
        "order": article.order,
        "blocks": len(article.body),
        "words": {code: article.word_count(code) for code in ("fa", "en", "de")},
    }
    if with_body:
        row["body"] = [_block_row(block) for block in article.body]
        row["faq"] = [
            {"question": translated(item.question), "answer": translated(item.answer)}
            for item in article.faq
        ]
    return row
