from typing import Any

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from booking.models import Booking
from parking_area.forms import ParkingAreaCreateForm, ParkingAreaUpdateForm
from parking_area.models import ParkingArea
import logging


logger = logging.getLogger("parking_area.views")


class AddParkingAreaView(LoginRequiredMixin, View):
    """
    Представление для добавления парковки.

    Атрибуты:
        template_name (str):
            Имя шаблона для отображения страницы добавления парковки.
        model (Model):
            Модель парковки.
        form_class (Form):
            Класс формы для создания парковки.
    """

    template_name = "pages/parking/add.html"
    model = ParkingArea
    form_class = ParkingAreaCreateForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка GET-запросов для отображения страницы добавления парковки.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse:
                HTTP-ответ с отображённым шаблоном добавления парковки.
        """
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Обработка POST-запросов для добавления парковки.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            JsonResponse:
                JSON-ответ с информацией о успешности добавления.
        """
        form = ParkingAreaCreateForm(request.POST)
        is_success = True
        if form.is_valid():
            logger.debug("Adding new parking area")
            new_parking_data = form.cleaned_data
            new_parking_data["latitude"] = form.data.get("latitude")
            new_parking_data["longitude"] = form.data.get("longitude")
            ParkingArea(**new_parking_data).save()
        else:
            logger.debug(form.errors)
            is_success = False

        return JsonResponse({"success": is_success})


class DeleteParkingAreaView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления парковки.

    Атрибуты:
        template_name (str):
            Имя шаблона для отображения страницы удаления парковки.
        model (Model):
            Модель парковки.
        success_url (str):
            URL для перенаправления после успешного удаления парковки.
    """

    template_name = "pages/parking/delete.html"
    model = ParkingArea
    success_url = reverse_lazy("index")


class DetailParkingAreaView(DetailView):
    """
    Представление для отображения детальной информации об парковки.

    Атрибуты:
        template_name (str):
            Имя шаблона для отображения страницы с детальной информацией.
        model (Model):
            Модель парковки.
    """

    template_name = "pages/parking/detail.html"
    model = ParkingArea


class UpdateParkingAreaView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления информации об парковки.

    Атрибуты:
        template_name (str):
            Имя шаблона для отображения страницы обновления информации.
        model (Model):
            Модель парковки.
        form_class (Form):
            Класс формы для обновления информации об парковки.
    """

    template_name = "pages/parking/update.html"
    model = ParkingArea
    form_class = ParkingAreaUpdateForm


class ManagementParkingAreaView(LoginRequiredMixin, View):
    """
    Представление для управления парковки.

    Атрибуты:
        template_name (str):
            Имя шаблона для отображения страницы управления парковкой.
        model (Model):
            Модель парковки.
    """

    template_name = "pages/parking/management.html"
    model = ParkingArea

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка GET-запросов для отображения страницы управления парковкой.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse:
                HTTP-ответ с отображённым шаблоном управления парковкой.
        """
        context = {"parking": None, "now": timezone.now(), "booking_list": None}
        try:
            parking: ParkingArea = ParkingArea.objects.get(manager=request.user)
            context["parking"] = parking
            context["booking_list"] = Booking.objects.filter(
                parking=parking, conformation_time__isnull=False
            ).order_by("-booking_start_time")
        except ParkingArea.DoesNotExist:
            logger.error("No managed parking")

        return render(request, self.template_name, context=context)
