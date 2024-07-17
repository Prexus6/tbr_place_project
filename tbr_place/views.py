from django.shortcuts import render
from .models import Prompt, MyPrompt
import random
from django.contrib import messages
from .utils import save_book_from_open_library, search_books_by_title


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


def search_books_view(request):
    """
    Zobrazuje formulár pre vyhľadávanie kníh a spracúva POST požiadavky.

    Ak je požiadavka typu POST, získa názov knihy z formulára, vyhľadá knihy
    podľa tohto názvu pomocou externého API (Open Library), a uloží nájdené
    knihy do databázy. Zobrazí správu o úspešnom uložení kníh. Inak zobrazí
    formulár pre vyhľadávanie kníh.

    """
    if request.method == 'POST':
        title = request.POST.get('title')
        results = search_books_by_title(title)
        books = results.get('docs', [])

        for book_data in books:
            book_info = {
                "title": book_data.get('title'),
                "author_name": book_data.get('author_name', [''])[0],
                "genres": book_data.get('subject', []),
                "isbn": book_data.get('isbn', [''])[0],
                "rating": 0.0,
                "cover_url": book_data.get('cover_url', "")
            }
            save_book_from_open_library(book_info)

        messages.success(request, 'Books successfully fetched and saved!')

    return render(request, 'search_books.html')


def home_view(request):
    """ Hlavná stránka (testovacia verzia šablony)"""
    context = {}

    if request.method == 'POST':
        context.update(generate_random_prompt(request))

    context['book_message'] = "test message"

    return render(request, 'index.html', context)

# TODO nové testy postman
