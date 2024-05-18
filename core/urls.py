from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls, name="admin"),
    path("booking/", include("booking.urls")),
    path("parking/", include("parking_area.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
