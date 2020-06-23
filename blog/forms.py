from django import forms
from .models import MAX_POST_LENGTH


class NewPost(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":3}), max_length=MAX_POST_LENGTH)
