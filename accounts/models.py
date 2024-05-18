import uuid

from django.contrib.auth.models import (
    AbstractUser,
    Group,
    PermissionsMixin,
)
from django.db import models

from booking.models import ParkingArea


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=False
    )
    telegram_tag = models.CharField(max_length=256, blank=True, null=True)
    telegram_id = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.username

    def update(self, commit=False, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        if commit:
            self.save()
