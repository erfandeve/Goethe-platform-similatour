from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.courses.urls")),
    path("api/", include("apps.exams.urls")),
    path("api/", include("apps.podcasts.urls")),
    path("api/", include("apps.learning.urls")),
    path("api/", include("apps.adminpanel.urls")),
    path("api/", include("apps.billing.urls")),
    path("api/", include("apps.cms.urls")),
    path("api/", include("apps.core.urls")),
]

# Uploaded media is served by the API in every environment: the host's disk is
# the source of truth, and the frontend only ships a copy of what existed at
# build time. `SERVE_MEDIA=false` turns this off behind a CDN or bucket.
if config("SERVE_MEDIA", default=True, cast=bool):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
