from django import forms
from .models import Category, Husband

class AddPostForm(forms.Form):
    title=forms.CharField(max_length=255)
    slug=forms.SlugField(max_length=255)
    content=forms.CharField(widget=forms.Textarea())
    is_published=forms.BooleanField()
    cat=forms.ModelMultipleChoiceField(queryset=Category.objects.all())