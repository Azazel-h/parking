from django.urls import include, path

from booking import views

urlpatterns = [
    path("add/", views.AddBookingView.as_view()),
]
