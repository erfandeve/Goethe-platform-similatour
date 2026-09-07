from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("refresh/", views.refresh),
    path("me/", views.me),
    path("change-password/", views.change_password),
    path("wallet/", views.wallet),
    path("wallet/topup/", views.wallet_topup),
    path("notifications/", views.notifications),
    path("notifications/read-all/", views.notifications_read_all),
    path("notifications/<str:pk>/read/", views.notification_read),
    path("messages/", views.messages),
    path("messages/send/", views.message_send),
    path("messages/<str:pk>/read/", views.message_read),
    path("dashboard/", views.dashboard),
]
