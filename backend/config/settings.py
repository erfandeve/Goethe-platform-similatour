from pathlib import Path

import mongoengine
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="dev-insecure-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.core",
    "apps.accounts",
    "apps.courses",
    "apps.exams",
    "apps.podcasts",
    "apps.learning",
    "apps.adminpanel",
    "apps.billing",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # Serves the admin's own CSS in production; the app itself is an API.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]

# We use MongoDB through mongoengine; Django's ORM stays unused.
DATABASES = {}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Behind a proxy (Render, Railway, Fly) the TLS terminates upstream.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default="http://localhost:3000", cast=Csv()
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("apps.accounts.auth.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "apps.core.exceptions.api_exception_handler",
}

CORS_ALLOWED_ORIGINS = config(
    "CORS_ORIGINS", default="http://localhost:3000", cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# --- MongoDB -----------------------------------------------------------------
MONGO_HOST = config("MONGO_HOST", default="mongodb://localhost:27017/goteh")
MONGO_DB = config("MONGO_DB", default="goteh")
mongoengine.connect(db=MONGO_DB, host=MONGO_HOST, alias="default")

# --- Auth --------------------------------------------------------------------
JWT_ACCESS_MINUTES = config("JWT_ACCESS_MINUTES", default=60, cast=int)
JWT_REFRESH_DAYS = config("JWT_REFRESH_DAYS", default=14, cast=int)

# --- AI speaking teacher ------------------------------------------------------
# The key stays server-side: nothing here is ever exposed to the browser.
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_TEXT_MODEL = config("OPENAI_TEXT_MODEL", default="gpt-5.4-mini")
OPENAI_TRANSCRIPTION_MODEL = config("OPENAI_TRANSCRIPTION_MODEL", default="gpt-transcribe")
MAX_AUDIO_DURATION = config("MAX_AUDIO_DURATION", default=60, cast=int)
STORE_AUDIO = config("STORE_AUDIO", default=False, cast=bool)
AI_MAX_RETRIES = config("AI_MAX_RETRIES", default=2, cast=int)

# Recorded answers are small; this ceiling keeps a bad client from filling memory.
DATA_UPLOAD_MAX_MEMORY_SIZE = 16 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 16 * 1024 * 1024

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"apps.learning": {"handlers": ["console"], "level": "INFO"}},
}
