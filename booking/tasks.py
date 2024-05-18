import decimal
from .models import Booking
import requests
import logging
from urllib.parse import quote

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
                f"<b>Напоминание о завершении бронирования</b>\n"
                f"Уважаемый {user.last_name} {user.first_name}, ваше бронирование заканчивается через 5 минут.\n"
                f'<a href="http://localhost:8000/parking/management/">Вы можете перейти по ссылке и продлить его</a>'
            )
            encoded_text = quote(text)
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={encoded_text}"
            logger.debug(url)
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
