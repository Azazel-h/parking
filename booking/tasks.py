import decimal

from django_q.tasks import async_task
from django.utils import timezone
from .models import Booking
from notifications.notify_bot import bot as n_bot
from django_q.tasks import async_task
import requests
import logging

logger = logging.getLogger("booking.views")
TOKEN = "6952995842:AAEyiJb8WF0oSwpQPPxMAQbRXElDwfGiin0"


def notify_user(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        user = booking.user
        if user.telegram_id:
            logger.debug("Sending notification")
            chat_id = user.telegram_id
            text = (
                f"Напоминание о завершении бронирования\n"
                f"Уважаемый {user.username}, ваше бронирование заканчивается через 5 минут."
            )

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
            logger.debug(requests.get(url).json())
    except Exception as ex:
        logger.warning(ex)


def end_booking(booking_id):
    try:
        logger.debug("Ending booking")
        booking = Booking.objects.get(pk=booking_id)

        booking.parking.free_slots += 1
        booking.parking.save()

        duration = booking.end_time - booking.start_time
        duration_in_hours = duration.total_seconds() / 3600
        total_cost = decimal.Decimal(duration_in_hours) * booking.parking.price

        booking.user.balance -= total_cost
        booking.user.save()
        logger.debug(
            f"Booking [{booking.pk} - {booking.user.username}] ended for {total_cost} RUB."
        )
    except Exception as ex:
        logger.warning(ex)
