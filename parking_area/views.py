from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from parking_area.forms import ParkingAreaCreateForm
from parking_area.models import ParkingArea


class AddParkingAreaView(LoginRequiredMixin, CreateView):
    template_name = "pages/parking/add.html"
    model = ParkingArea
    form_class = ParkingAreaCreateForm



class DeleteParkingAreaView(LoginRequiredMixin, View):

    def post(self, request):
        pass


class DetailParkingAreaView(View):
    def get(self, request):
        pass
