import markdown2
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import LiteraryWork, Category
from .forms import LiteraryWorkForm
from django.contrib.auth.decorators import login_required

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
    try:
        literary_work = get_object_or_404(LiteraryWork, pk=pk)
        literary_work.content_html = markdown2.markdown(literary_work.content)
        return render(request, 'literary_work_detail.html', {'literary_work': literary_work})
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("Something went wrong.")


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