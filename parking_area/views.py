import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from parking_area.forms import ParkingAreaCreateForm
from parking_area.models import ParkingArea
from crispy_forms.utils import render_crispy_form
import logging


logger = logging.getLogger("parking_area.views")


class AddParkingAreaView(LoginRequiredMixin, View):
    template_name = "pages/parking/add.html"
    model = ParkingArea
    form_class = ParkingAreaCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
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
            # ctx = request.POST.dict()
            # ctx.update(csrf(request))
            # form_html = render_crispy_form(form, context=ctx)
            # logger.debug(form_html)
            is_success = False

        return JsonResponse({"success": is_success})


class DeleteParkingAreaView(LoginRequiredMixin, DeleteView):
    template_name = "pages/parking/delete.html"
    model = ParkingArea
    success_url = reverse_lazy("index")


class DetailParkingAreaView(DetailView):
    template_name = "pages/parking/detail.html"
    model = ParkingArea
