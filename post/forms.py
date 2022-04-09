from django.forms import ModelForm
from .models import Post, Rate
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag']

class RateForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Rate
        fields = ['comment']