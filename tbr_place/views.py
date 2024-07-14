from django.http import JsonResponse
from django.shortcuts import render
from .models import Prompt, MyPrompt
import random
from django.contrib import messages
from .utils import save_book_details


def generate_random_prompt(request):
    """
    Generovanie náhodného promptu.
    """
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


def generate_custom_prompt(request):
    """
    Generovanie vlastného náhodného promptu.
    """
    context = {}
    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')

        generated_prompt = "Here is your custom prompt: "

        prompts = MyPrompt.objects.filter(prompt_type__myprompt_type_name__in=selected_types)

        if prompts.exists():
            random_prompt = random.choice(prompts)
            generated_prompt += random_prompt.prompt_name
            context['generated_prompt'] = generated_prompt
            messages.success(request, 'Custom prompt successfully generated!')
        else:
            generated_prompt += "No prompt available for selected types."
            context['generated_prompt'] = generated_prompt
            messages.warning(request, 'No prompts available for selected types.')

    return context


def search_book(request):
    pass


def add_book_view(request):
    """ Zkladanie získaných kníh (for API functions settings, check utils.py) """
    isbn = request.GET.get('isbn')
    if isbn:
        save_book_details(isbn)
        return JsonResponse({"message": "Book details fetched and saved."})
    return JsonResponse({"message": "ISBN not provided."})


def home_view(request):
    """ Hlavná stránka """
    context = {}

    context.update(generate_random_prompt(request))
    context.update(generate_custom_prompt(request))
    context['book_message'] = "test message"

    return render(request, 'index.html', context)

# TODO nové testy postman
