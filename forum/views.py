from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory, Thread, Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test view is working.")

def forum_home_view(request):
    categories = Category.objects.all()
    return render(request, 'forum/forum_home.html', {'categories': categories})

def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    subcategories = category.subcategory_set.all()
    return render(request, 'forum/category_detail.html', {'category': category, 'subcategories': subcategories})

def subcategory_detail_view(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    threads = subcategory.thread_set.all()
    return render(request, 'forum/subcategory_detail.html', {'subcategory': subcategory, 'threads': threads})

def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.post_set.all()
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_thread_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        subcategory_id = request.POST['subcategory_id']
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        thread = Thread.objects.create(title=title, subcategory=subcategory, author=request.user)
        return redirect('thread_detail', pk=thread.pk)
    subcategories = Subcategory.objects.all()
    return render(request, 'forum/create_thread.html', {'subcategories': subcategories})

@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.content = request.POST['content']
        post.save()
        return redirect('thread_detail', pk=post.thread.pk)
    return render(request, 'forum/edit_post.html', {'post': post})

@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    thread_pk = post.thread.pk
    post.delete()
    return redirect('thread_detail', pk=thread_pk)

@login_required
def vote_post_view(request, pk, vote_type):
    post = get_object_or_404(Post, pk=pk)
    # Přidejte logiku pro hlasování
    return redirect('thread_detail', pk=post.thread.pk)

@login_required
def report_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Přidejte logiku pro reportování
    return redirect('thread_detail', pk=post.thread.pk)


def title__icontains(query):
    pass


def search_results_view(request):
    query = request.GET.get('q')
    threads = Thread.objects.filter(title__icontains(query))
    return render(request, 'forum/search_results.html', {'threads': threads})
