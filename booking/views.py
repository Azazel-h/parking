from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from booking.models import Booking
import logging

from parking_area.models import ParkingArea
from http import HTTPStatus

logger = logging.getLogger("parking_area.views")


class AddBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        parking = ParkingArea.objects.get(pk=kwargs["pk"])
        if parking.free_slots >= 1:
            new_booking_data = {
                "user": request.user,
                "parking": parking,
                "creation_time": timezone.now(),
                "start_time": None,
                "end_time": None,
            }
            Booking(**new_booking_data).save()
            parking.free_slots -= 1
            parking.save()
            logger.debug("Adding new booking")

        return redirect("index")


class ManagementView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "pages/booking/management.html"
    context_object_name = "booking_list"

    def get_queryset(self, *args, **kwargs):
        parkings = ParkingArea.objects.filter(manager=self.request.user)
        booking_records = []
        for parking in parkings:
            for i in Booking.objects.filter(parking=parking):
                booking_records.append(i)
        logger.debug(booking_records)
        return booking_records
