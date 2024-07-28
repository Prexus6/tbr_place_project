from django import forms
from .models import MyPrompt, MyPromptType

class MyPromptForm(forms.ModelForm):
    class Meta:
        model = MyPrompt
        fields = ['prompt_name', 'prompt_type']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:

            self.fields['prompt_type'].queryset = MyPromptType.objects.filter(user=user)

class MyPromptTypeForm(forms.ModelForm):
    class Meta:
        model = MyPromptType
        fields = ['myprompt_type_name']