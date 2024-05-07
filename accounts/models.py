from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=False, blank=True)