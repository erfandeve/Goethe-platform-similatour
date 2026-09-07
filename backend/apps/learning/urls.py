from django.urls import path

from . import views

urlpatterns = [
    # Classroom data
    path("learning/<slug:slug>/", views.classroom),
    path("courses/<str:course_id>/parts/", views.course_parts_view),
    path("parts/<str:part_id>/videos/", views.part_videos),
    path("progress/", views.progress_overview),
    path("progress/video/", views.save_video_progress),
    path("speaking-attempts/", views.list_attempts),
    path("speaking-attempts/<str:video_id>/", views.video_attempts),
    # AI
    path("ai/transcribe/", views.transcribe_view),
    path("ai/analyze/", views.analyze_view),
]
