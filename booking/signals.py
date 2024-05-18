from typing import Any, Type

from django.db.models.signals import post_delete
from django.dispatch import receiver
from booking.models import Booking


@receiver(post_delete, sender=Booking)
def delete_related_schedules(
    sender: Type[Booking], instance: Booking, **kwargs: Any
) -> None:
    if instance.end_schedule:
        instance.end_schedule.delete()
    if instance.notify_schedule:
        instance.notify_schedule.delete()
