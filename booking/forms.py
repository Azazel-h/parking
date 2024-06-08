import logging
from datetime import datetime

from django import forms
from django.forms import ModelForm, DateTimeInput, TimeInput
from django.utils import timezone

from .models import Booking


logger = logging.getLogger("parking_area.views")


class TimeOnlyField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = TimeInput(attrs={"type": "time"})
        super().__init__(*args, **kwargs)

    def clean(self, value):
        # Parse the time input
        try:
            time_obj = datetime.strptime(value, "%H:%M").time()
        except ValueError:
            raise forms.ValidationError("Введите правильное время.")

        # Combine with today's date
        local_now = timezone.localtime()
        today = local_now.date()
        logger.debug(today)
        return datetime.combine(today, time_obj)


class BookingAddForm(ModelForm):
    booking_start_time = TimeOnlyField(label="Начальное время бронирования")
    booking_end_time = TimeOnlyField(label="Конечное время бронирования")

    class Meta:
        model = Booking
        fields = ("booking_start_time", "booking_end_time")

    def clean(self):
        cleaned_data = super().clean()
        booking_start_time = cleaned_data.get("booking_start_time")
        booking_end_time = cleaned_data.get("booking_end_time")

        # if booking_start_time and booking_end_time:
        # if booking_start_time >= timezone.now():
        #     raise forms.ValidationError(
        #         "Время бронирования должно быть позже текущего."
        #     )
        # if booking_start_time >= booking_end_time:
        #     raise forms.ValidationError(
        #         "Конечное время бронирования должно быть позже начального времени бронирования."
        #     )
        # if booking_end_time - booking_start_time < timezone.timedelta(hours=2):
        #     raise forms.ValidationError(
        #         "Минимальная продолжительность бронирования должна быть не менее двух часов."
        #     )

        return cleaned_data


class ConfirmBookingForm(forms.ModelForm):
    slot_number = forms.IntegerField(min_value=1, initial=1, label="", required=True)

    class Meta:
        model = Booking
        fields = ("slot_number",)

    def __init__(self, max_slot, *args, **kwargs):
        super(ConfirmBookingForm, self).__init__(*args, **kwargs)
        self.fields["slot_number"].widget.attrs["max"] = max_slot
