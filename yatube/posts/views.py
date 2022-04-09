from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm
from .models import Group, Post, User

PAGE_NUM = 10


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGE_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, PAGE_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author)
    posts_number = post_list.count()
    paginator = Paginator(post_list, PAGE_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts_number': posts_number,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, id=post_id)
    author = posts.author
    posts_numbers = author.posts.count()
    context = {
        'author': author,
        'posts': posts,
        'posts_numbers': posts_numbers,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    is_edit = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', {
            'form': form, 'is_edit': is_edit
        }
        )
    form = PostForm()
    return render(request, 'posts/create_post.html', {
        'form': form, 'is_edit': is_edit
    }
    )


@login_required
def post_edit(request, post_id):
    user = request.user
    posts = get_object_or_404(Post, pk=post_id)
    form = PostForm()
    is_edit = True
    context = {
        'posts': posts,
        'form': form,
        'is_edit': is_edit
    }
    if user != posts.author:
        return redirect('posts:post_detail', posts.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=posts)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.author = request.user
            posts.save()
            return redirect('posts:post_detail', posts.pk)
    return render(request, 'posts/create_post.html', context)
