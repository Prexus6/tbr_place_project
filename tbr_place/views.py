from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from literary_works.models import LiteraryWork
from .forms import MyPromptForm, MyPromptTypeForm
from .models import Prompt, MyPrompt, FavoriteBook, Book, MyPromptType, Reader, PromptType, Quote
import random
from django.contrib import messages
from literary_works.models import LiteraryWork
import json
from datetime import date

def generate_random_prompt(request):
    """
    Generovanie náhodného promptu.
    """
    context = {}
    try:
        prompts = Prompt.objects.all()
        if not prompts:
            raise ValueError('No prompts available.')

        random_prompt = random.choice(prompts)
        context = {
            'prompt_name': random_prompt.prompt_name,
            'prompt_type': random_prompt.prompt_type.prompt_type_name
        }
        messages.success(request, 'Prompt successfully generated!')

    except ValueError as e:
        context = {
            'prompt_name': 'No prompts available',
            'prompt_type': 'N/A'
        }
        messages.warning(request, str(e))

    return context


def generate_filtered_prompt(request):
    """
    Generovanie náhodného promptu na základe vybraných typov promptov.
    """
    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')
        print("Selected Types:", selected_types)  # Debugovanie

        if not selected_types:
            messages.warning(request, 'No prompt types have been selected.')
            return JsonResponse({'generated_prompt': 'No prompt available for selected types.'})

        prompts = Prompt.objects.filter(
            prompt_type__prompt_type_name__in=selected_types
        )

        if prompts.exists():
            random_prompt = random.choice(prompts)
            generated_prompt = f"Here is your custom prompt: {random_prompt.prompt_name}"
            messages.success(request, 'Custom prompt successfully generated!')
        else:
            generated_prompt = "No prompt available for selected types."
            messages.warning(request, 'No prompts available for selected types.')

        return JsonResponse({'generated_prompt': generated_prompt})
    return JsonResponse({'generated_prompt': 'Invalid request method.'})



@login_required
def generate_custom_prompt(request):
    """
    Generovanie vlastného náhodného promptu.
    """
    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')

        if not selected_types:
            return JsonResponse({'generated_prompt': 'No prompt types have been selected.'}, status=400)

        prompts = MyPrompt.objects.filter(
            prompt_type__myprompt_type_name__in=selected_types,
            user=request.user
        )

        if prompts.exists():
            random_prompt = random.choice(prompts)
            generated_prompt = f"Here is your custom prompt: {random_prompt.prompt_name}"
            return JsonResponse({'generated_prompt': generated_prompt})
        else:
            return JsonResponse({'generated_prompt': 'No prompt available for selected types.'}, status=404)

    return JsonResponse({'generated_prompt': 'Invalid request.'}, status=400)


@login_required
def add_my_prompt_type(request):
    form = MyPromptTypeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        prompt_type = form.save(commit=False)
        prompt_type.user = request.user
        prompt_type.save()
        messages.success(request, 'Prompt type successfully added!')
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'Form is invalid. Please correct the errors.')

    return {'prompt_type_form': form}




@login_required
def add_my_prompt(request):
    if request.method == 'POST':
        form = MyPromptForm(request.POST, user=request.user)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.user = request.user
            prompt.save()
            messages.success(request, 'Prompt successfully added!')
            return redirect('home')  # Redirect to home to avoid resubmission
        else:
            messages.error(request, 'Form is invalid. Please correct the errors.')
    else:
        form = MyPromptForm(user=request.user)  # Posielame aktuálneho používateľa

    prompt_types = MyPromptType.objects.filter(user=request.user)
    return render(request, 'index.html', {'prompt_form': form, 'prompt_types': prompt_types})

@login_required
def edit_prompt(request, prompt_id):
    """
    Editovanie existujúceho promptu.
    """
    prompt = get_object_or_404(MyPrompt, id=prompt_id, user=request.user)
    if request.method == 'POST':
        form = MyPromptForm(request.POST, instance=prompt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prompt successfully updated!')
            return redirect('home')
    else:
        form = MyPromptForm(instance=prompt)
    return render(request, 'edit_prompt.html', {'form': form})

@login_required
def remove_prompt(request, prompt_id):
    try:
        prompt = MyPrompt.objects.get(id=prompt_id, user=request.user)
        prompt.delete()
        messages.success(request, 'Prompt successfully removed!')
    except MyPrompt.DoesNotExist:
        messages.error(request, 'Prompt not found or you do not have permission to delete it.')

    return redirect('home')


def random_quote(request):
    if request.method == "GET":
        quotes = list(Quote.objects.all())
        if not quotes:
            return JsonResponse({"error": "No quotes found"}, status=404)
        quote = random.choice(quotes)
        return JsonResponse({"text": quote.text, "author": quote.author})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)




@login_required
def home_view(request):
    """ Hlavná stránka """
    context = {}

    filter_prompt_type = request.GET.get('filter_prompt_type')

    if request.method == 'POST':
        if 'generate_prompt' in request.POST:
            result = generate_random_prompt(request)
            if isinstance(result, dict):
                context.update(result)
        elif 'generate_filtered_prompt' in request.POST:
            result = generate_filtered_prompt(request)
            if isinstance(result, dict):
                context.update(result)
        elif 'selectedTypes[]' in request.POST:
            result = generate_custom_prompt(request)
            if isinstance(result, dict):
                context.update(result)
        elif 'add_prompt' in request.POST:
            result = add_my_prompt(request)
            if isinstance(result, dict):
                context.update(result)
        elif 'add_prompt_type' in request.POST:
            result = add_my_prompt_type(request)
            if isinstance(result, dict):
                context.update(result)

    works = LiteraryWork.objects.all()
    for work in works:
        work.average_rating = work.ratings.aggregate(average=Avg('rating')).get('average')

    context['works'] = works
    favorites = FavoriteBook.objects.filter(user=request.user)
    context['favorites'] = favorites
    context['all_prompt_types'] = PromptType.objects.all()
    context['prompt_form'] = MyPromptForm(user=request.user)

    context['prompt_types'] = MyPromptType.objects.filter(user=request.user)
    context['prompt_type_form'] = MyPromptTypeForm()
    favorites = FavoriteBook.objects.filter(user=request.user)
    context['favorites'] = favorites
    user_prompts = MyPrompt.objects.filter(user=request.user)
    if filter_prompt_type:
        user_prompts = user_prompts.filter(prompt_type_id=filter_prompt_type)
    context['user_prompts'] = user_prompts
    context['filter_prompt_type'] = filter_prompt_type

    return render(request, 'index.html', context)




