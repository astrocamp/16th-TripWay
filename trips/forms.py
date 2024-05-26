from django import forms
from .models import Trip

# class UploadModelForm(forms.ModelForm):
#     class Meta:
#         model = Trip
#         fields = ("image",)
#         widgets = {
#             "image": forms.FileInput(attrs={"class": "form-control-file"})
#         }