from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DeleteView

from booking.models import Booking
from booking.tasks import end_booking

from parking_area.models import ParkingArea
from http import HTTPStatus
from django_q.tasks import async_task, schedule
from django_q.models import Schedule

import logging

logger = logging.getLogger("parking_area.views")


class AddBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        parking = ParkingArea.objects.get(pk=kwargs["pk"])
        if (
            parking.free_slots >= 1
            and not Booking.objects.filter(
                user=request.user, end_time__gt=timezone.now()
            ).first()
        ):
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
            for i in Booking.objects.filter(
                parking=parking, start_time__isnull=True
            ).order_by("start_time"):
                booking_records.append(i)
        logger.debug(booking_records)
        return booking_records


class UserBookingView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "pages/booking/user-bookings.html"
    context_object_name = "booking_list"

    def get_queryset(self, *args, **kwargs):
        booking_records = Booking.objects.filter(user=self.request.user).order_by(
            "creation_time"
        )
        return booking_records

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class StartBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.start_time = timezone.now()
        booking.end_time = timezone.now() + timezone.timedelta(minutes=6)
        booking.save()
        logger.debug(booking)

        booking.notify_schedule = schedule(
            "booking.tasks.notify_user",
            booking.id,
            schedule_type="O",
            next_run=booking.end_time - timezone.timedelta(minutes=5),
        )

        booking.end_schedule = schedule(
            "booking.tasks.end_booking",
            booking.id,
            schedule_type="O",
            next_run=booking.end_time,
        )
        booking.save()
        return redirect("booking-management")


class EndBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        end_booking(self.kwargs["pk"])
        Booking.objects.get(pk=self.kwargs["pk"]).notify_schedule.delete()
        Booking.objects.get(pk=self.kwargs["pk"]).end_schedule.delete()

        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")


class DeleteBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        booking = Booking.objects.get(pk=self.kwargs["pk"])
        parking = booking.parking
        parking.free_slots += 1

        parking.save()
        booking.delete()
        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")
