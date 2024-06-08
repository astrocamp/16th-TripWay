from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "image": forms.ClearableFileInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
        }
