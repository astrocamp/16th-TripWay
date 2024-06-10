from django import forms
from .models import Blog, BlogComment
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='extends'))

    class Meta:
        model = Blog
        fields = ["title", "spot_name", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "spot_name": forms.TextInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "image": forms.ClearableFileInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
        }

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content', 'rating']
