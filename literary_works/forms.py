from django import forms
from .models import LiteraryWork, Rating


class LiteraryWorkForm(forms.ModelForm):
    class Meta:
        model = LiteraryWork
        fields = ['title', 'description', 'content', 'image', 'category', 'tags', 'published']
        widgets = {
            'category': forms.Select(),
            'tags': forms.CheckboxSelectMultiple(),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }