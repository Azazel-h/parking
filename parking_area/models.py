from django.db import models

from core import settings


class Parking(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    all_slots = models.PositiveIntegerField(default=0)
    free_slots = models.PositiveIntegerField(default=0)
    taken_slots = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=512)
    price = models.PositiveIntegerField(default=0)
