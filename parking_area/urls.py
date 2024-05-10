from django.urls import include, path

from parking_area import views

urlpatterns = [
    path("add/", views.AddParkingAreaView.as_view(), name="add-parking-area"),
    path("detail/<int:pk>", views.DetailParkingAreaView.as_view(), name="detail-parking-area"),
    path("delete/<int:pk>", views.DeleteParkingAreaView.as_view(), name="delete-parking-area"),
]
