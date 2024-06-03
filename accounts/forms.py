from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser
from accounts.validators import validate_russian_alphabet, validate_non_negative_balance


class CustomUserCreateForm(UserCreationForm):
    """
    Форма для создания пользователей.

    Attributes:
        first_name (CharField):
            Поле для ввода имени пользователя.
        last_name (CharField):
            Поле для ввода фамилии пользователя.
    """

    first_name = forms.CharField(
        max_length=50, label="Имя", validators=[validate_russian_alphabet]
    )
    last_name = forms.CharField(
        max_length=50, label="Фамилия", validators=[validate_russian_alphabet]
    )

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")


class CustomUserAdminEditForm(UserChangeForm):
    """
    Форма для изменения пользователей в админке.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")


class UserUpdateForm(ModelForm):
    """
    Форма для обновления информации о пользователе.
    """

    first_name = forms.CharField(
        max_length=30, validators=[validate_russian_alphabet], label="Имя", required=False
    )

    last_name = forms.CharField(
        max_length=30, validators=[validate_russian_alphabet], label="Фамилия", required=False
    )

    balance = forms.FloatField(
        validators=[validate_non_negative_balance], label="Баланс", required=False
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "telegram_tag", "balance")
        labels = {
            "balance": "Баланс",
            "email": "Адрес электронной почты",
            "telegram_tag": "Ваш тег в TG или ID",
        }
