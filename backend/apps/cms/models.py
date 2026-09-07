"""Editable content: the home page's own sections, and the articles.

Both were hard-coded once. They are the two places the marketing side of the
site needs to change without a deploy, so they live in the database with the
same `{fa, en, de}` embedding the rest of the catalogue uses.
"""

from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    StringField,
)

from apps.core.i18n import TranslatedText

# What a home section looks like on the page. The kind drives the layout only;
# every kind reads from the same fields, so switching one does not lose content.
SECTION_KINDS = (
    "text_image",  # prose beside a picture — the "About Lexora" block
    "rich_text",   # a wide column of prose with optional bullets
    "features",    # a grid of small cards built from `items`
    "stats",       # `items` rendered as value + label
    "faq",         # `items` rendered as question + answer
    "cta",         # a single band with a button
)

BLOCK_TYPES = ("p", "h2", "h3", "ul", "ol", "quote", "callout", "table", "cta")


class SectionItem(EmbeddedDocument):
    """One card, stat, or question inside a section.

    Deliberately generic: `title`/`body` mean value/label for a stats block and
    question/answer for a FAQ, which keeps the editor to one shape.
    """

    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    body = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    icon = StringField(default="")


class HomeSection(Document):
    meta = {"collection": "home_sections", "indexes": ["key", "order"]}

    key = StringField(required=True, unique=True)
    kind = StringField(choices=SECTION_KINDS, default="text_image")

    eyebrow = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    subtitle = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # Paragraphs are separated by blank lines, so the editor stays a textarea.
    body = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    items = EmbeddedDocumentListField(SectionItem, default=list)

    image = StringField(default="")
    image_alt = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # Which side the picture sits on for `text_image`; ignored by other kinds.
    image_side = StringField(choices=("start", "end"), default="end")

    cta_label = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    cta_href = StringField(default="")

    accent = StringField(default="#8b7dff")
    order = IntField(default=0)
    is_published = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.utcnow)


class TableRow(EmbeddedDocument):
    cells = EmbeddedDocumentListField(TranslatedText, default=list)


class ArticleBlock(EmbeddedDocument):
    """One block of an article body.

    Which fields matter depends on `type`; the rest stay empty. Storing the
    structure rather than HTML is what keeps headings, lists and tables
    semantic in every language without trusting editor markup.
    """

    type = StringField(choices=BLOCK_TYPES, default="p")
    text = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # h2 only: the id the table of contents links to.
    anchor = StringField(default="")
    items = EmbeddedDocumentListField(TranslatedText, default=list)
    # table only
    head = EmbeddedDocumentListField(TranslatedText, default=list)
    rows = EmbeddedDocumentListField(TableRow, default=list)
    caption = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # callout and cta
    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    label = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    href = StringField(default="")


class FaqItem(EmbeddedDocument):
    question = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    answer = EmbeddedDocumentField(TranslatedText, default=TranslatedText)


class Article(Document):
    meta = {"collection": "articles", "indexes": ["slug", "-published_at"]}

    slug = StringField(required=True, unique=True)

    title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # Hand-tuned for the search result; falls back to `title` when empty.
    meta_title = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    meta_description = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    excerpt = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    focus_keyword = EmbeddedDocumentField(TranslatedText, default=TranslatedText)
    # Comma-separated per language — one field the editor can actually fill in.
    keywords = EmbeddedDocumentField(TranslatedText, default=TranslatedText)

    cover = StringField(default="")
    body = EmbeddedDocumentListField(ArticleBlock, default=list)
    faq = EmbeddedDocumentListField(FaqItem, default=list)
    related = ListField(StringField(), default=list)

    reading_minutes = IntField(default=10)
    is_published = BooleanField(default=True)
    order = IntField(default=0)

    published_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def word_count(self, locale):
        """Rough count of the body in one language, for the byline."""
        words = 0
        for block in self.body:
            for field in (block.text, block.title, block.caption):
                words += len(field.resolve(locale).split()) if field else 0
            for item in block.items:
                words += len(item.resolve(locale).split())
            for row in block.rows:
                for cell in row.cells:
                    words += len(cell.resolve(locale).split())
        for item in self.faq:
            words += len(item.question.resolve(locale).split())
            words += len(item.answer.resolve(locale).split())
        return words
