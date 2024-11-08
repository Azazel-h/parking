from django.contrib.auth import get_user_model
from django.forms import ModelForm, TextInput
from parking_area.models import ParkingArea


class ParkingAreaCreateForm(ModelForm):
    """
    Форма для создания парковки.
    """

    class Meta:
        model = ParkingArea
        fields = ("address", "all_slots", "price", "manager")
        labels = {
            "address": "Адрес",
            "all_slots": "Количество мест",
            "price": "Цена за минуту парковки",
            "manager": "Менеджер",
        }
        widgets = {
            "address": TextInput(
                attrs={
                    "placeholder": "Адрес",
                    "id": "suggest",
                    "class": "form-control",
                    "autocomplete": "on",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["manager"].queryset = (
            get_user_model()
            .objects.filter(is_staff=True, is_superuser=False)
            .exclude(parkingarea__isnull=False)
        )


class ParkingAreaUpdateForm(ModelForm):
    """
    Форма для обновления информации об парковки.
    """

    class Meta:
        model = ParkingArea
        fields = (
            "all_slots",
            "price",
            "manager",
            "address",
            "latitude",
            "longitude",
        )
        labels = {
            "address": "Адрес",
            "all_slots": "Количество мест",
            "price": "Цена за минуту парковки",
            "manager": "Менеджер",
            "latitude": "Широта",
            "longitude": "Долгота",
        }
        widgets = {
            "address": TextInput(
                attrs={
                    "placeholder": "Адрес",
                    "id": "suggest",
                    "class": "form-control",
                    "autocomplete": "on",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_manager = self.instance.manager
        self.fields["manager"].queryset = get_user_model().objects.filter(
            is_staff=True, is_superuser=False
        ).exclude(parkingarea__isnull=False) | get_user_model().objects.filter(
            pk=current_manager.pk
        )
