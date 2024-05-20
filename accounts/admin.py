from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreateForm, CustomUserAdminEditForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateForm
    form = CustomUserAdminEditForm
    model = CustomUser
    list_display = ("username", "is_staff", "is_superuser", "first_name", "last_name")


admin.site.register(CustomUser, CustomUserAdmin)
