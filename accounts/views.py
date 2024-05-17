from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, View
from accounts.forms import CustomUserCreateForm, BalanceUpdateForm


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserUpdateView(LoginRequiredMixin, View):
    form_class = BalanceUpdateForm
    success_url = reverse_lazy("index")
    template_name = "pages/users/update.html"

    def post(self, request, *args, **kwargs):
        form = BalanceUpdateForm(request.POST)
        if form.is_valid():
            request.user.update(**form.cleaned_data)
            request.user.save()
        return redirect("index")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"form": self.form_class})
