from django import forms
from .models import ImageModel
from .models import Blog, BlogComment
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Blog
        fields = ["title", "spot_name", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "spot_name": forms.TextInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "image": forms.ClearableFileInput(attrs={"class": "border border-gray-300 rounded-lg p-2 w-full"}),
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name='blog'
            )
        }

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['title', 'spot_name', 'content', 'image']


def image_verify(file):
    if not file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise NoImageException("The uploaded file is not an image.")

