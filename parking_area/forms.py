from django.forms import ModelForm, TextInput

from parking_area.models import ParkingArea


class ParkingAreaCreateForm(ModelForm):
    class Meta:
        model = ParkingArea
        fields = ("address", "all_slots", "price", "manager")
        labels = {
            "address": "Адрес",
            "all_slots": "Количество мест",
            "price": "Цена за час парковки",
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
