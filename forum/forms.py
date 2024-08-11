from django import forms
from .models import Thread, Post

# Formulář pro vytváření a editaci vlákna
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category']  # Pole, která budou zobrazena ve formuláři

# Formulář pro vytváření a editaci příspěvku
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']  # Pole, která budou zobrazena ve formuláři
