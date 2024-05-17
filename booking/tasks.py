from django_q.tasks import async_task
from django.utils import timezone
from .models import Booking
import logging

logger = logging.getLogger("booking.views")


def notify_user(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        user = booking.user
        logger.debug(
            "Напоминание о завершении бронирования"
            f"Уважаемый {user.username}, ваше бронирование заканчивается через 5 минут.",
        )
    except Booking.DoesNotExist:
        pass


def end_booking(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        booking.parking.free_slots += 1
        logger.debug(f"Booking [{booking.pk} - {booking.user.username}] ended.")
    except Booking.DoesNotExist:
        pass
