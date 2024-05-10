from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
