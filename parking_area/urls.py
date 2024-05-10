from django.urls import include, path

from parking_area import views

urlpatterns = [
    path("add/", views.AddParkingAreaView.as_view()),
    path("detail/<int:pk>", views.DetailParkingAreaView.as_view()),
    path("delete/<int:pk>", views.DeleteParkingAreaView.as_view()),
]
