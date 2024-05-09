from django.contrib import admin

from booking.models import Parking, Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "parking", "creation_time", "start_time", "end_time")
    list_filter = ["parking"]



admin.site.register(Booking, BookingAdmin)
