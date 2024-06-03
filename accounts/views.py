import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from dotenv import load_dotenv

from accounts.forms import CustomUserCreateForm, UserUpdateForm
import logging

logger = logging.getLogger("parking_area.views")


class SignUpView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Атрибуты:
    ----------
    form_class : CustomUserCreateForm
        Форма для создания нового пользователя.
    success_url : str
        URL для перенаправления после успешной регистрации.
    template_name : str
        Шаблон для отображения страницы регистрации.
    """

    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserUpdateView(LoginRequiredMixin, View):
    """
    Представление для обновления информации о пользователе.

    Атрибуты:
        form_class (Form):
            Класс формы, используемой для обновления информации о пользователе.
        success_url (str):
            URL для перенаправления после успешной отправки формы.
        template_name (str):
            Имя шаблона для отображения формы обновления.
    """

    form_class = UserUpdateForm
    success_url = reverse_lazy("index")
    template_name = "pages/users/update.html"

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        """
        Обработка POST-запросов для обновления информации о пользователе.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponseRedirect:
                Перенаправляет на URL успеха, если форма валидна, в противном случае повторно отображает форму.
        """
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            request.user.update(**form.cleaned_data)
            request.user.save()
            return redirect(self.success_url)
        else:
            context = {"form": form, "bot_tag": os.getenv("BOT_TAG")}
            return render(request, self.template_name, context)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка GET-запросов для отображения формы обновления пользователя.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse:
                HTTP-ответ с отображённым шаблоном.
        """
        form = self.form_class(instance=request.user)
        context = {"form": form, "bot_tag": os.getenv("BOT_TAG")}
        return render(request, self.template_name, context)
