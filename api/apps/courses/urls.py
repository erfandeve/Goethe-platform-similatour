from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list),
    path("courses/<slug:slug>/", views.course_detail_view),
    path("courses/<slug:slug>/enroll/", views.enroll_free),
    path("courses/<slug:slug>/progress/", views.update_progress),
    path("courses/<slug:slug>/reviews/", views.add_review),
    path("categories/", views.category_list),
    path("instructors/", views.instructor_list),
    path("cart/", views.cart_view),
    path("cart/add/", views.cart_add),
    path("cart/remove/", views.cart_remove),
    path("cart/coupon/", views.cart_coupon),
    path("checkout/", views.checkout),
    path("orders/", views.order_list),
    path("my/courses/", views.my_courses),
]
