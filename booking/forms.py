from django import forms
from django.forms import ModelForm, DateTimeInput
from django.utils import timezone

from .models import Booking


class BookingAddForm(ModelForm):
    """
    Форма для создания бронирования.
    """

    class Meta:
        model = Booking
        fields = ("booking_start_time", "booking_end_time")
        labels = {
            "booking_start_time": "Начальное время бронирования",
            "booking_end_time": "Конечное время бронирования",
        }
        widgets = {
            "booking_start_time": DateTimeInput(attrs={"type": "datetime-local"}),
            "booking_end_time": DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_start_time = cleaned_data.get("booking_start_time")
        booking_end_time = cleaned_data.get("booking_end_time")
        if booking_start_time and booking_end_time:
            if booking_start_time >= booking_end_time:
                raise forms.ValidationError(
                    "Конечное время бронирования должно быть позже начального времени бронирования."
                )
            if booking_end_time - booking_start_time < timezone.timedelta(hours=2):
                raise forms.ValidationError(
                    "Минимальная продолжительность бронирования должна быть не менее двух часов."
                )
        return cleaned_data


class ConfirmBookingForm(forms.ModelForm):
    slot_number = forms.IntegerField(min_value=1, initial=1, label="", required=True)

    class Meta:
        model = Booking
        fields = ("slot_number",)

    def __init__(self, max_slot, *args, **kwargs):
        super(ConfirmBookingForm, self).__init__(*args, **kwargs)
        self.fields["slot_number"].widget.attrs["max"] = max_slot
