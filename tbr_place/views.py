from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import MyPromptForm, MyPromptTypeForm
from .models import Prompt, MyPrompt, FavoriteBook, Book, MyPromptType, Reader, PromptType, Quote, ReadingGoal, \
    ReadingProgress
import random
from django.contrib import messages
from .utils import  is_valid_isbn
# save_book_from_open_library
import  requests
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
    context = {}

    if request.method == 'POST':
        selected_types = request.POST.getlist('selectedTypes[]')

        if not selected_types:
            messages.warning(request, 'No prompt types have been selected.')
            return context  # vráti prázdny kontext

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
        return redirect('home')  # Redirect to home to avoid resubmission
    elif request.method == 'POST':
        messages.error(request, 'Form is invalid. Please correct the errors.')

    return {'prompt_type_form': form}




@login_required
def add_my_prompt(request):
    if request.method == 'POST':
        form = MyPromptForm(request.POST, user=request.user)  # Posielame aktuálneho používateľa
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
@csrf_exempt
def add_to_my_books(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            isbn = data.get('isbn')
            print(f'Received ISBN: {isbn}')  # Debugovanie
            if not isbn:
                return JsonResponse({'success': False, 'message': 'ISBN is missing.'})

            book = Book.objects.get(isbn=isbn)
            print(f'Found book: {book}')  # Debugovanie
            user = request.user

            if FavoriteBook.objects.filter(user=user, book=book).exists():
                return JsonResponse({'success': False, 'message': 'Book already in your collection.'})

            FavoriteBook.objects.create(user=user, book=book)
            return JsonResponse({'success': True})
        except Book.DoesNotExist:
            print('Book not found exception')
            return JsonResponse({'success': False, 'message': 'Book not found.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




@login_required
def get_my_books(request):
    user = request.user
    favorite_books = FavoriteBook.objects.filter(user=user)
    book_list = []

    for favorite in favorite_books:
        book = favorite.book
        book_list.append({
            'title': book.book_title,
            'author': book.book_author.author_name,
            'isbn': book.isbn,
            'cover_url': book.book_cover.url if book.book_cover else '',
            'rating': book.book_rating,
        })

    return JsonResponse({'books': book_list}, safe=False)



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


def goal_list(request):
    goals = ReadingGoal.objects.filter(user=request.user)
    return render(request, 'index.html', {'goals': goals})


@login_required
def update_goal(request, id):
    if request.method == "POST":
        try:
            goal = get_object_or_404(ReadingGoal, id=id, user=request.user)
            new_amount = int(request.POST.get('current_amount', 0))


            ReadingProgress.objects.create(
                goal=goal,
                date=date.today(),
                amount=new_amount
            )

            total_progress = ReadingProgress.objects.filter(goal=goal).aggregate(Sum('amount'))['amount__sum'] or 0

            return JsonResponse({
                'success': True,
                'new_amount': total_progress,
                'percentage': goal.progress_percentage()
            })
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=400)


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
        # else:
            # result = search_books_and_handle_favorites(request)
            # if isinstance(result, dict):
            #     context.update(result)

    favorites = FavoriteBook.objects.filter(user=request.user)
    context['favorites'] = favorites
    context['all_prompt_types'] = PromptType.objects.all()
    context['prompt_form'] = MyPromptForm(user=request.user)

    # Získajte prompt typy iba pre aktuálneho používateľa
    context['prompt_types'] = MyPromptType.objects.filter(user=request.user)
    context['prompt_type_form'] = MyPromptTypeForm()
    favorites = FavoriteBook.objects.filter(user=request.user)
    context['favorites'] = favorites

    goals = ReadingGoal.objects.filter(user=request.user)
    context['goals'] = goals
    user_prompts = MyPrompt.objects.filter(user=request.user)
    if filter_prompt_type:
        user_prompts = user_prompts.filter(prompt_type_id=filter_prompt_type)
    context['user_prompts'] = user_prompts
    context['filter_prompt_type'] = filter_prompt_type

    return render(request, 'index.html', context)




