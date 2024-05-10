from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from booking.models import ParkingArea


class IndexView(ListView):
    template_name = "pages/index.html"
    model = ParkingArea

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["parking_list"] = ParkingArea.objects.all()
    #     return context
