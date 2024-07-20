from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserLoginForm, SetNewPasswordForm, SecurityQuestionForm

CustomUser = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your form.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        secret_answer = request.POST['secret_answer']

        try:
            user = CustomUser.objects.get(username=username)
            if user.secret_answer == secret_answer:
                request.session['reset_user_id'] = user.id
                return redirect('reset_password')
            else:
                messages.error(request, 'Incorrect answer to the secret question.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'accounts/forgot_password.html')

def reset_password_view(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['new_password1']
            password2 = form.cleaned_data['new_password2']

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password')

            user_id = request.session.get('reset_user_id')
            if not user_id:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('forgot_password')

            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successfully. You can now log in.')
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist.')
    else:
        form = SetNewPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')
