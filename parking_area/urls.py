from django.urls import include, path

from parking_area import views

urlpatterns = [
    path("add/", views.AddParkingAreaView.as_view(), name="add-parking-area"),
    path(
        "management/",
        views.ManagementParkingAreaView.as_view(),
        name="parking-management",
    ),
    path(
        "<int:pk>/detail/",
        views.DetailParkingAreaView.as_view(),
        name="detail-parking-area",
    ),
    path(
        "<int:pk>/delete/",
        views.DeleteParkingAreaView.as_view(),
        name="delete-parking-area",
    ),
    path(
        "<int:pk>/update/",
        views.UpdateParkingAreaView.as_view(),
        name="update-parking-area",
    ),
]
