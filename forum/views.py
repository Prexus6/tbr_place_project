from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Thread, Post, Category
from .forms import ThreadForm, PostForm

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

def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.posts.all()  # Použijeme related_name 'posts' místo 'post_set'
    form = PostForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Přesměrování na přihlašovací stránku, pokud uživatel není přihlášen
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect('thread_detail', pk=thread.pk)
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})

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

@login_required
def edit_thread_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm(instance=thread)
    return render(request, 'forum/edit_thread.html', {'form': form})

@login_required
def delete_thread_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        thread.delete()
        return redirect('forum_home')
    return render(request, 'forum/delete_thread.html', {'thread': thread})

@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=post.thread.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/edit_post.html', {'form': form})

@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('thread_detail', pk=post.thread.pk)
    return render(request, 'forum/delete_post.html', {'post': post})
