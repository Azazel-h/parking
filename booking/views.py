import datetime
from typing import Any, List, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from booking.forms import BookingAddForm, ConfirmBookingForm
from booking.models import Booking
from booking.tasks import end_booking, send_custom_message

from parking_area.models import ParkingArea
from django_q.tasks import schedule

import logging

logger = logging.getLogger("parking_area.views")


class AddBookingView(LoginRequiredMixin, View):
    """
    Представление для добавления бронирования.
    """

    model = Booking
    form_class = BookingAddForm

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        """
        Обработка POST-запросов для добавления бронирования.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            logger.debug("Form data: %s", form_data)
            parking = get_object_or_404(ParkingArea, pk=kwargs["pk"])

            # Check for existing active bookings
            existing_booking = Booking.objects.filter(
                user=request.user, end_time__isnull=True, is_canceled=False
            ).first()

            if not existing_booking:
                new_booking_data = {
                    "user": request.user,
                    "parking": parking,
                    "creation_time": timezone.localtime(),
                    "booking_start_time": form_data.get("booking_start_time"),
                    "booking_end_time": form_data.get("booking_end_time"),
                    "start_time": None,
                    "end_time": None,
                }
                Booking.objects.create(**new_booking_data)
                logger.debug("New booking added for user %s", request.user)
            else:
                logger.error(
                    "Existing active booking found: %s with end time %s",
                    existing_booking.pk,
                    existing_booking.booking_end_time,
                )
        else:
            logger.debug("Form errors: %s", form.errors)
            # Optionally, you can return the form with errors back to the user
            # return render(request, 'your_template.html', {'form': form})

        return redirect("index")


class ManagementView(LoginRequiredMixin, ListView):
    """
    Представление для управления бронированиями.

    Атрибуты:
        model (Model):
            Модель бронирования.
        template_name (str):
            Имя шаблона для отображения страницы управления бронированиями.
        context_object_name (str):
            Имя объекта контекста для передачи в шаблон.
    """

    model = Booking
    template_name = "pages/booking/management.html"
    context_object_name = "booking_list"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Booking]:
        """
        Получение списка бронирований.
        """
        parking = ParkingArea.objects.filter(manager=self.request.user).first()
        if not parking:
            return []

        return Booking.objects.filter(
            parking=parking, conformation_time__isnull=True, is_canceled=False
        ).order_by("-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parking = get_object_or_404(ParkingArea, manager=self.request.user)
        bookings = Booking.objects.filter(
            parking=parking, is_canceled=False, end_time__isnull=True
        ).order_by("start_time")

        slots = {}
        # Заполнение данных для каждого парковочного места
        for hour in range(24):
            time_hour = datetime.time(hour)
            next_hour = datetime.time((hour + 1) % 24)
            slots[time_hour] = {
                slot_num: {
                    "next_hour": next_hour,
                    "booking": self.get_booking_for_slot(bookings, slot_num, time_hour),
                }
                for slot_num in range(1, parking.all_slots + 1)
            }

        context["slots"] = slots
        context["slots_range"] = range(1, parking.all_slots + 1)
        context["parking"] = parking
        context["confirm_form"] = ConfirmBookingForm(max_slot=parking.all_slots)
        return context

    def get_booking_for_slot(self, bookings, slot_num, time_hour):
        for booking in bookings:
            booking_start_time_local = timezone.localtime(
                booking.booking_start_time
            ).time()

            booking_end_time_local = timezone.localtime(booking.booking_end_time).time()

            booking_start_time_local_rounded = datetime.time(
                booking_start_time_local.hour, 0
            )

            if booking_end_time_local.minute > 0:
                booking_end_time_local_rounded = datetime.time(
                    (booking_end_time_local.hour + 1) % 24, 0
                )
            else:
                booking_end_time_local_rounded = booking_end_time_local

            logger.debug(
                f"{booking_start_time_local} - {time_hour} - {booking_end_time_local} - {booking.id}"
            )
            if booking.slot_number == slot_num:
                # Handle cases where booking spans across the next day (e.g., 22:57 - 23:58)
                if booking_start_time_local_rounded < booking_end_time_local_rounded:
                    if (
                        booking_start_time_local_rounded
                        <= time_hour
                        < booking_end_time_local_rounded
                    ):
                        logger.debug(
                            f"{booking_start_time_local} - {time_hour} - {booking_end_time_local} - {booking.id}"
                        )
                        return booking
                else:  # Overlapping case (e.g., 23:00 to 00:00)
                    if (
                        time_hour >= booking_start_time_local_rounded
                        or time_hour < booking_end_time_local_rounded
                    ):
                        logger.debug(
                            f"{booking_start_time_local} - {time_hour} - {booking_end_time_local} - {booking.id}"
                        )
                        return booking
        return None


class UserBookingView(LoginRequiredMixin, ListView):
    """
    Представление для отображения бронирований пользователя.

    Атрибуты:
        model (Model):
            Модель бронирования.
        template_name (str):
            Имя шаблона для отображения страницы с бронированиями пользователя.
        context_object_name (str):
            Имя объекта контекста для передачи в шаблон.
    """

    model = Booking
    template_name = "pages/booking/user-bookings.html"
    context_object_name = "booking_list"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Booking]:
        """
        Получение списка бронирований пользователя.

        Аргументы:
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            List[Booking]:
                Список объектов бронирований пользователя.
        """
        booking_records: QuerySet = Booking.objects.filter(
            user=self.request.user
        ).order_by("-creation_time")
        return booking_records

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Получение дополнительных данных контекста.

        Аргументы:
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            Dict[str, Any]:
                Словарь с дополнительными данными контекста.
        """
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class ConfirmBookingView(LoginRequiredMixin, View):
    model = Booking

    def post(self, request, *args, **kwargs):
        booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.conformation_time = timezone.now()
        booking.slot_number = request.POST.get("slot_number")
        booking.save()

        # Установка расписания для уведомления пользователя
        booking.notify_schedule = schedule(
            "booking.tasks.notify_user",
            booking.id,
            schedule_type="O",
            next_run=booking.booking_end_time - timezone.timedelta(minutes=5),
        )

        # Установка расписания для окончания бронирования
        booking.end_schedule = schedule(
            "booking.tasks.end_booking",
            booking.id,
            schedule_type="O",
            next_run=booking.booking_end_time,
        )
        booking.save()

        try:
            send_custom_message(
                user=booking.user,
                msg="Ваше бронирование было успешно подтверждено!",
            )
        except:
            pass

        return redirect("booking-management")


class StartBookingView(LoginRequiredMixin, View):
    """
    Представление для начала бронирования.

    Атрибуты:
        model (Model):
            Модель бронирования.
    """

    model = Booking
    form_class = ConfirmBookingForm

    def post(self, request, *args, **kwargs):
        booking = Booking.objects.get(pk=self.kwargs["pk"])

        # Создание экземпляра формы
        form = self.form_class(request.POST)

        # Проверка валидности формы
        if form.is_valid():
            # Установка времени начала и окончания бронирования
            form_data = form.cleaned_data
            booking.conformation_time = timezone.now()
            booking.end_time = booking.booking_end_time
            booking.slot_number = form_data.get("slot_number")
            booking.save()

            # Установка расписания для уведомления пользователя
            booking.notify_schedule = schedule(
                "booking.tasks.notify_user",
                booking.id,
                schedule_type="O",
                next_run=booking.end_time - timezone.timedelta(minutes=5),
            )

            # Установка расписания для окончания бронирования
            booking.end_schedule = schedule(
                "booking.tasks.end_booking",
                booking.id,
                schedule_type="O",
                next_run=booking.end_time,
            )
            booking.save()

        return redirect("booking-management")


class EndBookingView(LoginRequiredMixin, View):
    """
    Представление для завершения бронирования.

    Атрибуты:
        model (Model):
            Модель бронирования.
    """

    model = Booking

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        """
                Обработка POST-запросов для завершения бронирования.

                Аргументы:
                    request (HttpRequest):
                        Объект HTTP-запроса.
                        *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponseRedirect:
                Перенаправляет на страницу управления бронированиями.
        """
        booking: Booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.end_time = booking.booking_end_time
        booking.save()

        end_booking(self.kwargs["pk"])

        try:
            Booking.objects.get(pk=self.kwargs["pk"]).end_schedule.delete()
            Booking.objects.get(pk=self.kwargs["pk"]).notify_schedule.delete()
        except Exception as ex:
            logger.error(ex)

        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")


class ProlongBookingView(LoginRequiredMixin, View):
    """
    Представление для продления бронирования.

    Атрибуты:
        model (Model):
            Модель бронирования.
    """

    model = Booking

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка POST-запросов для продления бронирования.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse:
                Перенаправляет на страницу управления бронированиями или страницу бронирований пользователя.
        """
        booking: Booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.save()

        try:
            Booking.objects.get(pk=self.kwargs["pk"]).end_schedule.delete()
            Booking.objects.get(pk=self.kwargs["pk"]).notify_schedule.delete()
        except Exception as ex:
            logger.error(ex)
        new_end_time = booking.booking_end_time + timezone.timedelta(minutes=30)
        booking.booking_end_time = new_end_time

        booking.notify_schedule = schedule(
            "booking.tasks.notify_user",
            booking.id,
            schedule_type="O",
            next_run=new_end_time - timezone.timedelta(minutes=5),
        )

        booking.end_schedule = schedule(
            "booking.tasks.end_booking",
            booking.id,
            schedule_type="O",
            next_run=new_end_time,
        )
        booking.was_prolonged = True
        booking.save()

        try:
            send_custom_message(
                user=booking.user,
                msg="Ваше бронирование успешно продлено на 30 мин.",
            )
        except:
            pass

        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")


class DeleteBookingView(LoginRequiredMixin, View):
    """
    Представление для удаления бронирования.

    Атрибуты:
        model (Model):
            Модель бронирования.
    """

    model = Booking

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обработка POST-запросов для удаления бронирования.

        Аргументы:
            request (HttpRequest):
                Объект HTTP-запроса.
            *args (Any):
                Дополнительные позиционные аргументы.
            **kwargs (Any):
                Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse:
                Перенаправляет на страницу управления бронированиями или страницу бронирований пользователя.
        """
        booking: Booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.delete()
        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")


class CancelBookingView(LoginRequiredMixin, View):
    """
    Представление для удаления бронирования.

    Атрибуты:
        model (Model):
            Модель бронирования.
    """

    model = Booking

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        booking: Booking = Booking.objects.get(pk=self.kwargs["pk"])
        booking.is_canceled = True
        booking.save()

        try:
            send_custom_message(
                user=booking.user,
                msg="Ваше бронирование было отменено, создайте новую заявку на другое время.",
            )
        except:
            pass

        if request.user.is_staff:
            return redirect("parking-management")
        else:
            return redirect("booking-user")
