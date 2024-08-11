from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Thread, Post, Category
from .forms import ThreadForm, PostForm

# View pro hlavní stránku fóra
def forum_home(request):
    categories = Category.objects.all()
    threads = Thread.objects.all()
    user_threads = Thread.objects.filter(author=request.user) if request.user.is_authenticated else []
    commented_threads = Thread.objects.filter(posts__author=request.user).distinct() if request.user.is_authenticated else []
    return render(request, 'forum/forum_home.html', {
        'categories': categories,
        'threads': threads,
        'user_threads': user_threads,
        'commented_threads': commented_threads
    })

# View pro detail vlákna
def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.all()
    form = PostForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect('thread_detail', pk=thread.pk)
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})

# View pro vytvoření vlákna (přístupné pouze pro přihlášené uživatele)
@login_required
def create_thread_view(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})

# View pro editaci vlákna (přístupné pouze pro přihlášené uživatele)
@login_required
def edit_thread_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if thread.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm(instance=thread)
    return render(request, 'forum/edit_thread.html', {'form': form})

# View pro smazání vlákna (přístupné pouze pro přihlášené uživatele)
@login_required
def delete_thread_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if thread.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        thread.delete()
        return redirect('forum_home')
    return render(request, 'forum/delete_thread.html', {'thread': thread})

# View pro editaci příspěvku (přístupné pouze pro přihlášené uživatele)
@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=post.thread.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/edit_post.html', {'form': form})

# View pro smazání příspěvku (přístupné pouze pro přihlášené uživatele)
@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        post.delete()
        return redirect('thread_detail', pk=post.thread.pk)
    return render(request, 'forum/delete_post.html', {'post': post})

# View pro detail kategorie
def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    threads = Thread.objects.filter(category=category)
    return render(request, 'forum/category_detail.html', {'category': category, 'threads': threads})
