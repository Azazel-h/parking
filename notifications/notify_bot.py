import os
import django
from asgiref.sync import sync_to_async

# Укажите путь к файлу настроек вашего проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Инициализация Django
django.setup()

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from accounts.models import CustomUser

TOKEN = "6952995842:AAEyiJb8WF0oSwpQPPxMAQbRXElDwfGiin0"

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! Теперь тут будут приходить уведомления."
    )

    user_query = await sync_to_async(CustomUser.objects.filter)(
        telegram_tag=message.from_user.username
    )

    if await sync_to_async(user_query.exists)():
        user = await sync_to_async(user_query.first)()
        user.telegram_id = message.chat.id
        await sync_to_async(user.save)()
        await message.answer(text=f"Ваш telegram_id обновлен: {user.telegram_id}")
    else:
        await message.answer(text="Пользователь не найден в базе данных. Укажите свой тег на сайте проекта.")


async def main() -> None:
    await dp.start_polling(bot)
