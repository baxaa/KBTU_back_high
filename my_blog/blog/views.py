from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, CustomUser, Tag
from .forms import PostForm, CommentForm, TagForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


def blog(request):
    return "Hello World!"


@cache_page(60)  # Cache this view for 60 seconds
def post_list(request):
    posts = Post.objects.select_related('author').prefetch_related('comments').order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = Post.objects.select_related('author').prefetch_related('comments__author').get(id=post_id)

    # Low-level caching for the comment count
    cache_key = f'post_{post_id}_comment_count'
    comment_count = cache.get(cache_key)

    if comment_count is None:
        comment_count = post.comments.count()  # Expensive query
        cache.set(cache_key, comment_count, timeout=60)  # Cache for 60 seconds

    # Handle comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # Invalidate the cached comment count
            cache.delete(cache_key)

            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    comments = post.comments.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'comment_count': comment_count,  # Pass the cached comment count
    })


def post_create(request):
    if request.method == 'POST':
        print(request.user)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            user = CustomUser.objects.get(username=request.user)
            post.author = user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.user.id:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post_detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.user.id:
        messages.error(request, "You are not authorized to delete this post.")
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'post_detail.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('post_list')


# Create a new tag
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('tag_list')  # Redirect to the list view after creation
    else:
        form = TagForm()
    return render(request, 'tag_create.html', {'form': form})


# Read/Display all tags
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})


# Delete a tag (requires login)
@login_required
def tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tag_list')
    return render(request, 'tag_confirm_delete.html', {'tag': tag})
