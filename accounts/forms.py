from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50, label="Фамилия")

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")


class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")


class BalanceUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "telegram_id", "balance")
        labels = {
            "balance": "Баланс",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Адрес электронной почты",
            "telegram_id": "Ваш тег в TG или ID",
        }
