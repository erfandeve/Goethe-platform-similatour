"""Multilingual text stored inline on every document.

Every user-facing string on the platform exists in three languages, so instead of
duplicating documents per locale we embed a small translation object and resolve
it at serialization time with a fallback chain.
"""

from mongoengine import EmbeddedDocument, StringField

LOCALES = ("fa", "en", "de")
DEFAULT_LOCALE = "en"
FALLBACK_CHAIN = {"fa": ("fa", "en", "de"), "en": ("en", "de", "fa"), "de": ("de", "en", "fa")}


class TranslatedText(EmbeddedDocument):
    fa = StringField(default="")
    en = StringField(default="")
    de = StringField(default="")

    def resolve(self, locale=DEFAULT_LOCALE):
        for candidate in FALLBACK_CHAIN.get(locale, FALLBACK_CHAIN[DEFAULT_LOCALE]):
            value = getattr(self, candidate, "")
            if value:
                return value
        return ""

    def as_dict(self):
        return {"fa": self.fa, "en": self.en, "de": self.de}


def tt(fa="", en="", de=""):
    """Shorthand builder used by fixtures and admin imports."""
    return TranslatedText(fa=fa, en=en, de=de)


def t(field, locale):
    """Resolve a possibly-missing TranslatedText field."""
    if field is None:
        return ""
    return field.resolve(locale)
