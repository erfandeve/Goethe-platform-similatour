from django.urls import path

from . import views

urlpatterns = [
    path("plans/", views.plans),
    path("my/subscriptions/", views.my_subscriptions),
]
