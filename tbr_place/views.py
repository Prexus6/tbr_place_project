from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MyPromptForm, MyPromptTypeForm
from .models import Prompt, MyPrompt, FavoriteBook, Book, MyPromptType, Reader, PromptType
import random
from django.contrib import messages
from .utils import save_book_from_open_library, search_books_by_title


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
    context = {}

    selected_types = request.POST.getlist('selectedTypes')

    if not selected_types:
        messages.warning(request, 'No prompt types have been selected.')
        return context

    prompts = Prompt.objects.filter(
        prompt_type__prompt_type_name__in=selected_types
    )

    if prompts.exists():
        random_prompt = random.choice(prompts)
        context = {
            'filtered_prompt_name': random_prompt.prompt_name,
            'filtered_prompt_type': random_prompt.prompt_type.prompt_type_name
        }
        messages.success(request, 'Filtered prompt successfully generated!')
    else:
        context = {
            'filtered_prompt_name': 'No prompts available for the selected types',
            'filtered_prompt_type': 'N/A'
        }
        messages.warning(request, 'No prompts available for selected types.')

    return context


def generate_custom_prompt(request):
    """
    Generovanie vlastného náhodného promptu.
    """
    context = {}

    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to generate a prompt.')
        return context

    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')

        if not selected_types:
            messages.warning(request, 'No prompt types have been selected.')
            return context

        prompts = MyPrompt.objects.filter(
            prompt_type__myprompt_type_name__in=selected_types,
            user=request.user
        )

        if prompts.exists():
            random_prompt = random.choice(prompts)
            generated_prompt = f"Here is your custom prompt: {random_prompt.prompt_name}"
            context['generated_prompt'] = generated_prompt
            messages.success(request, 'Custom prompt successfully generated!')
        else:
            generated_prompt = "No prompt available for selected types."
            context['generated_prompt'] = generated_prompt
            messages.warning(request, 'No prompts available for selected types.')

    return context

@login_required
def add_my_prompt_type(request):
    form = MyPromptTypeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        prompt_type = form.save(commit=False)
        prompt_type.user = request.user
        prompt_type.save()
        messages.success(request, 'Prompt type successfully added!')
        return redirect('home')  # Redirect to home to avoid resubmission
    elif request.method == 'POST':
        messages.error(request, 'Form is invalid. Please correct the errors.')

    return {'prompt_type_form': form}




@login_required
def add_my_prompt(request):
    form = MyPromptForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        prompt = form.save(commit=False)
        prompt.user = request.user
        prompt.save()
        messages.success(request, 'Prompt successfully added!')
        return redirect('home')  # Redirect to home to avoid resubmission
    elif request.method == 'POST':
        messages.error(request, 'Form is invalid. Please correct the errors.')

    prompt_types = MyPromptType.objects.filter(user=request.user)
    return {'prompt_form': form, 'prompt_types': prompt_types}


def search_books_and_handle_favorites(request):
    context = {}

    if request.method == 'POST':
        if 'title' in request.POST:
            title = request.POST.get('title')
            results = search_books_by_title(title)
            books = results.get('docs', [])

            if not books:
                messages.info(request, 'Žiadne knihy sa nenašli pre zadaný názov.')

            for book_data in books:
                book_info = {
                    "title": book_data.get('title'),
                    "author_name": book_data.get('author_name', [''])[0],
                    "genres": book_data.get('subject', []),
                    "isbn": book_data.get('isbn', [''])[0],
                    "rating": 0.0,
                    "cover_url": f"http://covers.openlibrary.org/b/id/{book_data.get('cover_i')}-L.jpg" if book_data.get(
                        'cover_i') else None
                }
                save_book_from_open_library(book_info)

            context['books'] = books
            messages.success(request, 'Books successfully fetched and saved!')
        elif 'add_to_favorites' in request.POST:
            book_id = request.POST.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            if FavoriteBook.objects.filter(user=request.user, book=book).exists():
                messages.info(request, 'Túto knihu už máte v obľúbených.')
            else:
                FavoriteBook.objects.create(user=request.user, book=book)
                messages.success(request, 'Kniha bola pridaná do obľúbených.')
        elif 'remove_from_favorites' in request.POST:
            book_id = request.POST.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            favorite = FavoriteBook.objects.filter(user=request.user, book=book).first()
            if favorite:
                favorite.delete()
                messages.success(request, 'Kniha bola odstránená z obľúbených.')
            else:
                messages.info(request, 'Kniha nebola nájdená v obľúbených.')

    favorites = FavoriteBook.objects.filter(user=request.user)
    context['favorites'] = favorites

    return context


@login_required
def add_to_favorites(request, book_id):
    """
    Pridanie knihy do obľúbených.
    """
    print(f"Adding book with ID {book_id} to favorites")  # Debug print
    book = get_object_or_404(Book, id=book_id)
    if FavoriteBook.objects.filter(user=request.user, book=book).exists():
        messages.info(request, 'Túto knihu už máte v obľúbených.')
    else:
        FavoriteBook.objects.create(user=request.user, book=book)
        messages.success(request, 'Kniha bola pridaná do obľúbených.')
    return redirect('home')


@login_required
def remove_from_favorites(request, book_id):
    """
    Odstránenie knihy z obľúbených.
    """
    print(f"Removing book with ID {book_id} from favorites")  # Debug print
    book = get_object_or_404(Book, id=book_id)
    favorite = FavoriteBook.objects.filter(user=request.user, book=book).first()
    if favorite:
        favorite.delete()
        messages.success(request, 'Kniha bola odstránená z obľúbených.')
    else:
        messages.info(request, 'Kniha nebola nájdená v obľúbených.')
    return redirect('home')


@login_required
def home_view(request):
    """ Hlavná stránka """
    context = {}

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
        else:
            result = search_books_and_handle_favorites(request)
            if isinstance(result, dict):
                context.update(result)

    favorites = FavoriteBook.objects.filter(user=request.user)
    context['all_prompt_types'] = PromptType.objects.all()
    context['favorites'] = favorites
    context['prompt_types'] = MyPromptType.objects.filter(user=request.user)
    context['prompt_form'] = MyPromptForm()
    context['prompt_type_form'] = MyPromptTypeForm()

    return render(request, 'index.html', context)



