from django import forms
from .models import Spot


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ["name", "city", "latitude", "longitude", "description"]
        labels = {
            "name": "名稱",
            "city": "城市",
            "description": "描述",
        }
