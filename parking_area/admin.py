from django.contrib import admin

from parking_area.models import ParkingArea


class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        "latitude",
        "longitude",
        "all_slots",
        "free_slots",
        "taken_slots",
        "address",
        "manager",
        "price",
    )
    list_filter = ("address", "manager")


admin.site.register(ParkingArea, ParkingAdmin)
