from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .utils import super_paginator_xxx
from .forms import PostForm
from .models import User, Group, Post


def index(request):
    posts = super_paginator_xxx(Post.objects.all(), request)
    return render(request, 'posts/index.html', posts)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
    }
    context.update(super_paginator_xxx(posts, request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all().count()
    context = {
        'author': author,
        'post_list': post_list,
    }
    context.update(super_paginator_xxx(author.posts.all(), request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'posts': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    is_edit = False
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/create_post.html', {
        'form': form, 'is_edit': is_edit
    }
    )


def post_edit(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    is_edit = True
    context = {
        'post': post,
        'form': form,
        'is_edit': is_edit
    }
    if user != post.author:
        return redirect('post:post_detail', post.pk)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post.pk)
    return render(request, 'posts/create_post.html', context)
