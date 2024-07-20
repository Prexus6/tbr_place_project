from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        security_answer = request.POST['security_answer'].lower()
        try:
            user = User.objects.get(username=username, security_answer=security_answer)
            login(request, user)
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or security answer')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
