from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("home/", views.home),
    path("sitemap-feed/", views.sitemap_feed),
]
