from django.db import models
from django_q.models import Schedule
from core import settings
from parking_area.models import ParkingArea


class Booking(models.Model):
    """
    Модель бронирования.

    Attributes:
        user (ForeignKey):
            Пользователь, который сделал бронирование.
        parking (ForeignKey):
            Парковка, которая была забронирована.
        end_schedule (ForeignKey):
            Расписание для окончания бронирования.
        notify_schedule (ForeignKey):
            Расписание для уведомлений о бронировании.
        creation_time (DateTimeField):
            Время создания бронирования.
        start_time (DateTimeField):
            Время начала бронирования.
        end_time (DateTimeField):
            Время окончания бронирования.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parking = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    end_schedule = models.ForeignKey(
        Schedule,
        on_delete=models.SET_NULL,
        related_name="end_bookings",
        null=True,
        blank=True,
    )
    notify_schedule = models.ForeignKey(
        Schedule,
        on_delete=models.SET_NULL,
        related_name="notify_bookings",
        null=True,
        blank=True,
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
