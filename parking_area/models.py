from django.db import models
from django.urls import reverse

from core import settings


class ParkingArea(models.Model):
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True, "is_superuser": False},
    )
    all_slots = models.PositiveIntegerField(default=1, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=False, blank=False
    )
    free_slots = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=512)
    latitude = models.FloatField(default=0, null=False, blank=False)
    longitude = models.FloatField(default=0, null=False, blank=False)

    def get_absolute_url(self):
        return reverse("detail-parking-area", kwargs={"pk": self.pk})
