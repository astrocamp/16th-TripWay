from django import forms
from .models import Spot


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ["name", "address", "latitude", "longitude", "phone", "url", "rating"]
        labels = {
            "name": "名稱",
            "address": "地址",
            "city": "城市",
            "latitude": "經度",
            "longitude": "緯度",
            "phone": "電話",
            "url": "網址",
            "rating": "評分",
        }
