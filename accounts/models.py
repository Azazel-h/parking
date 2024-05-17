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
    telegram_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
