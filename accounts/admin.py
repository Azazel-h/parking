from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreateForm, CustomUserEditForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserEditForm
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name")


admin.site.register(CustomUser, CustomUserAdmin)
