import markdown2
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import LiteraryWork, Category, Rating
from .forms import LiteraryWorkForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate

@login_required
def literary_work_create(request):
    if request.method == 'POST':
        form = LiteraryWorkForm(request.POST, request.FILES)
        if form.is_valid():
            literary_work = form.save(commit=False)
            literary_work.user = request.user
            literary_work.save()
            print("Literary work created successfully!")
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = LiteraryWorkForm()
    return render(request, 'literary_work_form.html', {'form': form})

@login_required
def literary_work_edit(request, pk):
    literary_work = get_object_or_404(LiteraryWork, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LiteraryWorkForm(request.POST, request.FILES, instance=literary_work)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LiteraryWorkForm(instance=literary_work)
    return render(request, 'literary_work_form.html', {'form': form})


@login_required
def literary_work_detail(request, pk):
    literary_work = get_object_or_404(LiteraryWork, pk=pk)
    literary_work.content_html = markdown2.markdown(literary_work.content)
    average_rating = literary_work.ratings.aggregate(average=Avg('rating')).get('average')

    has_rated = Rating.objects.filter(work=literary_work, user=request.user).exists()

    if request.method == 'POST':
        if 'submit_rating' in request.POST:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating_value = form.cleaned_data['rating']
                Rating.objects.update_or_create(
                    work=literary_work,
                    user=request.user,
                    defaults={'rating': rating_value}
                )
                return redirect('literary_work_detail', pk=pk)
        elif 'remove_rating' in request.POST:
            Rating.objects.filter(work=literary_work, user=request.user).delete()
            return redirect('literary_work_detail', pk=pk)
    else:
        form = RatingForm()

    context = {
        'literary_work': literary_work,
        'average_rating': average_rating,
        'form': form,
        'has_rated': has_rated,
    }

    return render(request, 'literary_work_detail.html', context)


def literary_work_list(request):
    category_id = request.GET.get('category')
    if category_id and category_id != 'all':
        works = LiteraryWork.objects.filter(category_id=category_id)
    else:
        works = LiteraryWork.objects.all()

    data = list(works.values('id', 'title', 'description', 'user__username', 'category__name', 'image'))
    for work in data:
        work['image'] = work['image'] if work['image'] else ''
    return JsonResponse(data, safe=False)

def category_list(request):
    categories = Category.objects.all()
    data = list(categories.values('id', 'name'))
    return JsonResponse(data, safe=False)

@login_required
def user_profile(request):
    works = LiteraryWork.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'user': request.user, 'works': works})


@login_required
def literary_work_delete(request, pk):
    literary_work = get_object_or_404(LiteraryWork, pk=pk, user=request.user)

    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            literary_work.delete()
            messages.success(request, "Literary work deleted successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Incorrect password. Please try again.")

    return render(request, 'literary_work_delete.html', {'literary_work': literary_work})


@login_required
def add_or_update_rating(request, pk):
    literary_work = get_object_or_404(LiteraryWork, pk=pk)
    user_rating, created = Rating.objects.get_or_create(work=literary_work, user=request.user)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            form.save()
            return redirect('literary_work_detail', pk=pk)
    else:
        form = RatingForm(instance=user_rating)

    return render(request, 'rating_form.html', {'form': form, 'literary_work': literary_work})


@login_required
def delete_rating(request, pk):
    literary_work = get_object_or_404(LiteraryWork, pk=pk)
    rating = get_object_or_404(Rating, work=literary_work, user=request.user)
    rating.delete()
    return redirect('literary_work_detail', pk=pk)