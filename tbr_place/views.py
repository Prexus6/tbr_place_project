from django.shortcuts import render
from .models import Prompt, MyPrompt
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

    return render(request, 'index.html', context)



def generate_custom_prompt(request):
    """
        Generovanie vlastného náhodného promptu.
    """
    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')

        # Vygenerovanie promptu na základe vybraných typov
        generated_prompt = "Here is your custom prompt: "

        prompts = MyPrompt.objects.filter(prompt_type__myprompt_type_name__in=selected_types)

        if prompts.exists():
            random_prompt = random.choice(prompts)
            generated_prompt += random_prompt.prompt_name
            messages.success(request, 'Custom prompt successfully generated!')
        else:
            generated_prompt += "No prompt available for selected types."
            messages.warning(request, 'No prompts available for selected types.')

        return render(request, 'index.html', {'generated_prompt': generated_prompt})

    return render(request, 'index.html')


def search_book(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        # book_details = get_book_details(isbn)

# todo - get aws acc

    #     return render(request, 'index.html', {'book_details': book_details})
    # return render(request, 'index.html')