from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    """
    Форма для создания пользователей.

    Attributes:
        first_name (CharField):
            Поле для ввода имени пользователя.
        last_name (CharField):
            Поле для ввода фамилии пользователя.
    """

    first_name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50, label="Фамилия")

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

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "telegram_tag", "balance")
        labels = {
            "balance": "Баланс",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Адрес электронной почты",
            "telegram_tag": "Ваш тег в TG или ID",
        }
