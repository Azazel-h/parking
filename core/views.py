from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from booking.models import ParkingArea, Booking


class IndexView(ListView):
    template_name = "pages/index.html"
    model = ParkingArea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_booking = None
        if self.request.user.is_authenticated:
            has_booking = Booking.objects.filter(Q(
                user=self.request.user, end_time__gt=timezone.now()) | Q(user=self.request.user, end_time__isnull=True)
            ).first()
        context["has_booking"] = has_booking
        return context
