import logging

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from parking_area.forms import ParkingAreaCreateForm
from parking_area.models import ParkingArea


class AddParkingAreaView(LoginRequiredMixin, View):
    template_name = "pages/parking/add.html"
    model = ParkingArea
    form_class = ParkingAreaCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = ParkingAreaCreateForm(request.POST)
        if form.is_valid():
            logging.debug("Adding new parking area")
            new_parking_data = form.cleaned_data
            new_parking_data["latitude"] = form.data.get("latitude")
            new_parking_data["longitude"] = form.data.get("longitude")
            ParkingArea(**new_parking_data).save()
        else:
            logging.debug(form.errors)
        return render(request, self.template_name, {"form": form})


class DeleteParkingAreaView(LoginRequiredMixin, DeleteView):
    model = ParkingArea


class DetailParkingAreaView(DetailView):
    template_name = "pages/parking/detail.html"
    model = ParkingArea
