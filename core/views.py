from django.shortcuts import render
from django.views.generic import TemplateView

from booking.models import ParkingArea


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parking_list"] = ParkingArea.objects.all()
        return context
