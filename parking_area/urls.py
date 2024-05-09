from django.urls import include, path

from parking_area import views

urlpatterns = [
    path("add/", views.AddParkingAreaView.as_view()),
]
