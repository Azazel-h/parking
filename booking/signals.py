from django.db.models.signals import post_delete
from django.dispatch import receiver
from booking.models import Booking


@receiver(post_delete, sender=Booking)
def delete_related_schedules(sender, instance, **kwargs):
    if instance.end_schedule:
        instance.end_schedule.delete()
    if instance.notify_schedule:
        instance.notify_schedule.delete()