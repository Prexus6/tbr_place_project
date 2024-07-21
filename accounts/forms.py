from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    secret_question = forms.CharField(max_length=255, required=True, initial="What is your favorite book?")
    secret_answer = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'secret_question', 'secret_answer', 'password1', 'password2')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class SecurityQuestionForm(forms.Form):
    username = forms.CharField(max_length=255)
    secret_answer = forms.CharField(max_length=255, widget=forms.PasswordInput, required=False)

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)
    new_secret_question = forms.CharField(label='New secret question', max_length=255, required=False)
    new_secret_answer = forms.CharField(label='New secret answer', max_length=255, required=False, widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
