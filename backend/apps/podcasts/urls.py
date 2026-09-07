from django.urls import path

from . import views

urlpatterns = [
    path("podcasts/", views.podcast_list),
    path("podcasts/episodes/", views.episode_list),
    path("podcasts/episodes/<slug:slug>/", views.episode_detail_view),
    path("podcasts/episodes/<slug:slug>/play/", views.episode_play),
    path("podcasts/episodes/<slug:slug>/progress/", views.save_progress),
    path("podcasts/episodes/<slug:slug>/bookmark/", views.toggle_bookmark),
    path("podcasts/library/", views.my_library),
    path("podcasts/<slug:slug>/", views.podcast_detail_view),
]
