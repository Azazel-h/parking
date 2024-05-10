from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from parking_area.models import ParkingArea


class AddParkingAreaView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DeleteParkingAreaView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class DetailParkingAreaView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
