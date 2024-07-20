from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import random

from .forms import CustomUserCreationForm, CustomUserAuthenticationForm

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def index(request):
    return render(request, 'accounts/index.html')

def generate_random_prompt(request):
    prompts = [
        {'prompt_name': 'Prompt 1', 'prompt_type': 'Type A'},
        {'prompt_name': 'Prompt 2', 'prompt_type': 'Type B'},
        {'prompt_name': 'Prompt 3', 'prompt_type': 'Type C'},
    ]
    selected_prompt = random.choice(prompts)
    context = {
        'prompt_name': selected_prompt['prompt_name'],
        'prompt_type': selected_prompt['prompt_type']
    }
    return render(request, 'accounts/index.html', context)
