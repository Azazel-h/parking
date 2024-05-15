from django.urls import include, path

from booking import views

urlpatterns = [
    path("add/<int:pk>", views.AddBookingView.as_view(), name="add-booking"),
    path("management/", views.ManagementView.as_view(), name="management"),
    path("<int:pk>/start/", views.AddBookingView.as_view()),
    path("<int:pk>/end/", views.AddBookingView.as_view()),
    path("<int:pk>/delete/", views.AddBookingView.as_view(), name="delete-booking"),
    path("<int:pk>/prolong/", views.AddBookingView.as_view()),
]
