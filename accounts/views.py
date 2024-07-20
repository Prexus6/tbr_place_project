from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Přesměruje na index po přihlášení
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')  # Přesměruje na index po odhlášení

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Přesměruje na index po registraci
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            if user.secret_answer == request.POST.get('secret_answer'):
                # Redirect to a password reset form or handle password reset
                return redirect('reset_password')  # Assume there's a view for resetting password
        except CustomUser.DoesNotExist:
            pass  # Handle user not existing
    return render(request, 'accounts/forgot_password.html')

def index_view(request):
    return render(request, 'index.html')
