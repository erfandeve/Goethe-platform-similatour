import re
import unicodedata


def slugify(value, fallback="item"):
    value = unicodedata.normalize("NFKD", str(value))
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value or fallback


def get_locale(request):
    locale = (
        request.query_params.get("locale")
        or request.headers.get("X-Locale")
        or "en"
    ).lower()
    return locale if locale in ("fa", "en", "de") else "en"


def rial(amount):
    """Prices are stored as integer Rial to avoid float drift."""
    return int(amount or 0)
