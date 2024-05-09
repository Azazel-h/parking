from django.contrib.auth.models import (
    AbstractUser,
    Group,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from booking.models import Parking


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Car(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=False, null=False
    )
    current_parking = models.ForeignKey(
        Parking, on_delete=models.CASCADE, blank=True, null=True
    )
    car_number = models.CharField(max_length=20)
