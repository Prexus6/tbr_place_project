from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm, CustomUserLoginForm, UsernameForm, SecurityQuestionForm, SetNewPasswordForm

CustomUser = get_user_model()

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You have successfully logged in as {username}.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_protect
def forgot_password_view(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = CustomUser.objects.get(username=username)
                request.session['reset_user_id'] = user.id
                request.session['failed_attempts'] = 0  # Reset failed attempts
                return redirect('security_question')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist.')
    else:
        form = UsernameForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

@csrf_protect
def security_question_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password')

    user = get_object_or_404(CustomUser, id=user_id)
    failed_attempts = request.session.get('failed_attempts', 0)

    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            if user.secret_answer == form.cleaned_data['secret_answer']:
                request.session['failed_attempts'] = 0  # Reset failed attempts on success
                return redirect('reset_password')
            else:
                failed_attempts += 1
                request.session['failed_attempts'] = failed_attempts
                if failed_attempts >= 3:
                    messages.error(request, 'You have exceeded the maximum number of attempts. Please contact the administrator.')
                else:
                    messages.error(request, 'Incorrect answer to the secret question. If you do not know the answer, please contact the administrator.')
    else:
        form = SecurityQuestionForm()

    return render(request, 'accounts/security_question.html', {'form': form, 'secret_question': user.secret_question})

@csrf_protect
def reset_password_view(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            if not user_id:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('forgot_password')

            user = get_object_or_404(CustomUser, id=user_id)
            user.set_password(form.cleaned_data['new_password1'])
            new_secret_question = form.cleaned_data.get('new_secret_question')
            new_secret_answer = form.cleaned_data.get('new_secret_answer')

            if new_secret_question:
                user.secret_question = new_secret_question
            if new_secret_answer:
                user.secret_answer = new_secret_answer
            user.save()
            messages.success(request, 'Password and secret question/answer reset successfully. You can now log in.')
            return redirect('login')
    else:
        user_id = request.session.get('reset_user_id')
        if not user_id:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        user = get_object_or_404(CustomUser, id=user_id)
        form = SetNewPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form, 'username': user.username})

def index_view(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'index.html', {'username': username})
