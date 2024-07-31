from django import forms
from .models import LiteraryWork


class LiteraryWorkForm(forms.ModelForm):
    class Meta:
        model = LiteraryWork
        fields = ['title', 'description', 'content', 'image', 'category', 'tags', 'published']
        widgets = {
            'category': forms.Select(),
            'tags': forms.CheckboxSelectMultiple(),
        }
