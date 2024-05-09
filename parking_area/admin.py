from django.contrib import admin

from parking_area.models import Parking


class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        "all_slots",
        "free_slots",
        "taken_slots",
        "address",
        "price",
    )
    list_filter = ("address", "manager")


admin.site.register(Parking, ParkingAdmin)
