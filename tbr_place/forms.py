from django import forms
from .models import MyPrompt, MyPromptType

class MyPromptForm(forms.ModelForm):
    class Meta:
        model = MyPrompt
        fields = ['prompt_name', 'prompt_type']

class MyPromptTypeForm(forms.ModelForm):
    class Meta:
        model = MyPromptType
        fields = ['myprompt_type_name']