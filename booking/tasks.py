from django_q.tasks import async_task
from django.utils import timezone
from .models import Booking
from notifications.notify_bot import bot as n_bot
from django_q.tasks import async_task
import asyncio
import logging

logger = logging.getLogger("booking.views")


def notify_user(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        user = booking.user
        if user.telegram_id:
            logger.debug("Sending notification")
            asyncio.run(
                n_bot.send_message(
                    chat_id=user.telegram_id,
                    text="Напоминание о завершении бронирования"
                    f"Уважаемый {user.username}, ваше бронирование заканчивается через 5 минут.",
                )
            )
    except Booking.DoesNotExist:
        logger.warning("Booking does not exist!")


def end_booking(booking_id):
    try:
        logger.debug("Ending booking")
        booking = Booking.objects.get(pk=booking_id)
        booking.parking.free_slots += 1

        duration = booking.end_time - booking.start_time
        duration_in_hours = duration.total_seconds() / 3600
        total_cost = duration_in_hours * booking.parking.price

        booking.user.balance -= total_cost
        booking.user.save()
        logger.debug(
            f"Booking [{booking.pk} - {booking.user.username}] ended for {total_cost} RUB."
        )
    except Booking.DoesNotExist:
        logger.warning("Booking does not exist!")
