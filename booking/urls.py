from django.urls import path
from booking import views

urlpatterns = [
    path("add/<int:pk>", views.AddBookingView.as_view(), name="add-booking"),
    path("management/", views.ManagementView.as_view(), name="booking-management"),
    path("history/", views.UserBookingView.as_view(), name="booking-user"),
    path("<int:pk>/confirm/", views.ConfirmBookingView.as_view(), name="confirm-booking"),
    path("<int:pk>/start/", views.StartBookingView.as_view(), name="start-booking"),
    path("<int:pk>/end/", views.EndBookingView.as_view(), name="end-booking"),
    path("<int:pk>/delete/", views.DeleteBookingView.as_view(), name="delete-booking"),
    path(
        "<int:pk>/prolong/", views.ProlongBookingView.as_view(), name="prolong-booking"
    ),
]
