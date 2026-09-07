"""Small builders so the article modules read as content, not as constructors."""

from apps.cms.models import ArticleBlock, FaqItem, TableRow
from apps.core.i18n import tt


def p(fa, en, de):
    return ArticleBlock(type="p", text=tt(fa, en, de))


def h2(anchor, fa, en, de):
    return ArticleBlock(type="h2", anchor=anchor, text=tt(fa, en, de))


def h3(fa, en, de):
    return ArticleBlock(type="h3", text=tt(fa, en, de))


def quote(fa, en, de):
    return ArticleBlock(type="quote", text=tt(fa, en, de))


def bullets(*triples):
    return ArticleBlock(type="ul", items=[tt(*triple) for triple in triples])


def steps(*triples):
    return ArticleBlock(type="ol", items=[tt(*triple) for triple in triples])


def callout(title, body):
    return ArticleBlock(type="callout", title=tt(*title), text=tt(*body))


def cta(title, body, href, label):
    return ArticleBlock(
        type="cta", title=tt(*title), text=tt(*body), href=href, label=tt(*label)
    )


def table(caption, head, rows):
    return ArticleBlock(
        type="table",
        caption=tt(*caption),
        head=[tt(*cell) for cell in head],
        rows=[TableRow(cells=[tt(*cell) for cell in row]) for row in rows],
    )


def faq(*pairs):
    return [FaqItem(question=tt(*q), answer=tt(*a)) for q, a in pairs]
