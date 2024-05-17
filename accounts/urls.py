from django.urls import include, path

from accounts import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("update/", views.UserUpdateView.as_view(), name="user-update"),
]
