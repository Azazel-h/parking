import decimal
import os

from .models import Booking
import requests
import logging
from urllib.parse import quote

logger = logging.getLogger("booking.views")
TOKEN = os.environ.get("BOT_TOKEN")


def notify_user(booking_id: int) -> None:
    try:
        booking: Booking = Booking.objects.get(pk=booking_id)
        user = booking.user
        if user.telegram_id:
            logger.debug("Sending notification")
            chat_id = user.telegram_id
            text = (
                f"<b>Напоминание о завершении бронирования</b>\n"
                f"Уважаемый {user.last_name} {user.first_name}, ваше бронирование заканчивается через 5 минут.\n"
                f"Вы можете перейти по ссылке и продлить его!\n\n"
                f'<a href="http://127.0.0.1:{os.environ.get("DJANGO_PORT")}/booking/history/">Ссылка</a>'
            )
            encoded_text = quote(text)
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={encoded_text}"
            logger.debug(url)
            logger.debug(requests.get(url).json())
    except Exception as ex:
        logger.warning(ex)


def end_booking(booking_id: int) -> None:
    try:
        logger.debug("Ending booking")
        booking: Booking = Booking.objects.get(pk=booking_id)

        duration = booking.booking_end_time - booking.booking_start_time
        duration_in_hours = duration.total_seconds() / 3600
        total_cost = decimal.Decimal(duration_in_hours) * booking.parking.price

        booking.user.balance -= total_cost
        if booking.user.balance < 0:
            booking.user.balance = 0
        booking.user.save()
        logger.debug(
            f"Booking [{booking.pk} - {booking.user.username}] ended for {total_cost} RUB."
        )
    except Exception as ex:
        logger.warning(ex)


def send_custom_message(user, msg) -> None:
    try:
        if user.telegram_id:
            logger.debug("Sending message")
            chat_id = user.telegram_id
            text = msg
            encoded_text = quote(text)
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={encoded_text}"
            logger.debug(url)
            logger.debug(requests.get(url).json())
    except Exception as ex:
        logger.warning(ex)
