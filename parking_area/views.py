from typing import Any

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from booking.models import Booking
from parking_area.forms import ParkingAreaCreateForm, ParkingAreaUpdateForm
from parking_area.models import ParkingArea
import logging


logger = logging.getLogger("parking_area.views")


class AddParkingAreaView(LoginRequiredMixin, View):
    template_name = "pages/parking/add.html"
    model = ParkingArea
    form_class = ParkingAreaCreateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        form = ParkingAreaCreateForm(request.POST)
        is_success = True
        if form.is_valid():
            logger.debug("Adding new parking area")
            new_parking_data = form.cleaned_data
            new_parking_data["free_slots"] = form.data.get("all_slots")
            new_parking_data["latitude"] = form.data.get("latitude")
            new_parking_data["longitude"] = form.data.get("longitude")
            ParkingArea(**new_parking_data).save()
        else:
            logger.debug(form.errors)
            is_success = False

        return JsonResponse({"success": is_success})


class DeleteParkingAreaView(LoginRequiredMixin, DeleteView):
    template_name = "pages/parking/delete.html"
    model = ParkingArea
    success_url = reverse_lazy("index")


class DetailParkingAreaView(DetailView):
    template_name = "pages/parking/detail.html"
    model = ParkingArea


class UpdateParkingAreaView(LoginRequiredMixin, UpdateView):
    template_name = "pages/parking/update.html"
    model = ParkingArea
    form_class = ParkingAreaUpdateForm


class ManagementParkingAreaView(LoginRequiredMixin, View):
    template_name = "pages/parking/management.html"
    model = ParkingArea

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {"parking": None, "now": timezone.now()}
        try:
            parking: ParkingArea = ParkingArea.objects.get(manager=request.user)
            context["parking"] = parking
            context["booking_list"] = Booking.objects.filter(
                parking=parking, start_time__isnull=False
            ).order_by("-start_time")
        except ParkingArea.DoesNotExist:
            logger.error("No managed parking")

        return render(request, self.template_name, context=context)
