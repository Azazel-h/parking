import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from dotenv import load_dotenv

import notifications.notify_bot
from accounts.forms import CustomUserCreateForm, BalanceUpdateForm


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserUpdateView(LoginRequiredMixin, View):
    form_class = BalanceUpdateForm
    success_url = reverse_lazy("index")
    template_name = "pages/users/update.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        form = BalanceUpdateForm(request.POST)
        if form.is_valid():
            request.user.update(**form.cleaned_data)
            request.user.save()
        return redirect("index")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {"form": self.form_class}
        load_dotenv()
        context["bot_tag"] = os.getenv("BOT_TAG")
        return render(request, self.template_name, context={"form": self.form_class})