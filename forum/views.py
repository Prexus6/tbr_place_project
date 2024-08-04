from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Post, Subcategory
from .forms import ThreadForm, PostForm

@login_required
def forum_home_view(request):
    threads = Thread.objects.all()
    user_threads = Thread.objects.filter(author=request.user)
    subcategories = Subcategory.objects.all()
    return render(request, 'forum/forum_home.html', {'threads': threads, 'user_threads': user_threads, 'subcategories': subcategories})

@login_required
def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = PostForm()
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts, 'form': form})

@login_required
def create_thread_view(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('forum_home')
    else:
        form = ThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})
