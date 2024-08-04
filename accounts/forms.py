from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    secret_question = forms.CharField(
        max_length=255,
        required=True,
        initial="What is your favorite book?"
    )
    secret_answer = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'secret_question', 'secret_answer')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UsernameForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)

class SecurityQuestionForm(forms.Form):
    secret_answer = forms.CharField(max_length=255, required=True)

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=True)
    new_secret_question = forms.CharField(max_length=255, required=False)
    new_secret_answer = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
