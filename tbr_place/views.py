from django.shortcuts import render
from . models import Prompt
# Create your views here.
import random
from django.contrib import messages


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

    return render(request, 'accounts/index.html', context)