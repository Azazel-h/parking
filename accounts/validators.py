import re
from django.core.exceptions import ValidationError


def validate_russian_alphabet(value):
    if not re.match(r"^[А-Яа-яЁё]+$", value):
        raise ValidationError(
            "Это поле может содержать только буквы русского алфавита."
        )


def validate_non_negative_balance(value):
    if value < 0:
        raise ValidationError("Баланс не может быть отрицательным.")
