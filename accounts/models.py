import uuid

from django.contrib.auth.models import (
    AbstractUser,
    Group,
    PermissionsMixin,
)
from django.db import models

from booking.models import ParkingArea


class CustomUser(AbstractUser):
    """
    Модель пользователя.

    Attributes:
        id (UUIDField):
            Уникальный идентификатор пользователя.
        balance (DecimalField):
            Баланс пользователя.
        telegram_tag (CharField):
            Тег пользователя в Telegram.
        telegram_id (CharField):
            Идентификатор пользователя в Telegram.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=False
    )
    telegram_tag = models.CharField(max_length=256, blank=True, null=True)
    telegram_id = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя.

        Returns:
            str: Строковое представление пользователя.
        """
        return self.username

    def update(self, commit=False, **kwargs) -> None:
        """
        Обновляет поля пользователя на основе переданных значений.

        Args:
            commit (bool):
                Флаг, указывающий, нужно ли сохранить изменения в базе данных.
            **kwargs (dict):
                Пары ключ-значение для обновления полей пользователя.

        Returns:
            None
        """
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)
        if commit:
            self.save()
