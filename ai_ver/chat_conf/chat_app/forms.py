from django import forms
from .models import Comment

class CommentForm(forms.Form):
    u1_text = forms.CharField(max_length=255, widget=forms.Textarea)