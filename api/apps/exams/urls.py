from django.urls import path

from . import views

urlpatterns = [
    path("exams/", views.exam_list),
    path("exams/<slug:slug>/", views.exam_detail_view),
    path("exams/<slug:slug>/start/", views.start_attempt),
    path("attempts/<str:pk>/answers/", views.save_answers),
    path("attempts/<str:pk>/submit/", views.submit_attempt),
    path("attempts/<str:pk>/", views.attempt_detail),
    path("my/attempts/", views.my_attempts),
]
