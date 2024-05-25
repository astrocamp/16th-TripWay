from django import forms
from .models import Comment, Rating

class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, label="推薦指數")

    class Meta:
        model = Comment
        fields = ['content']
