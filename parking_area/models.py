from django.db import models

from core import settings


class ParkingArea(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
    )
    all_slots = models.PositiveIntegerField(default=0)
    free_slots = models.PositiveIntegerField(default=0)
    taken_slots = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=512)
    latitude = models.FloatField()
    longitude = models.FloatField()