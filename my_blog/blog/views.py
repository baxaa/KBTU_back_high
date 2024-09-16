from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


# Create your views here.
def blog(request):
    return "Hello World!"


# List view for all blog posts
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Get all posts, ordered by newest first
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Retrieve post by ID or return 404 if not found
    return render(request, 'post_detail.html', {'post': post})


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new post to the database
            return redirect('post_list')  # Redirect to the list of posts after submission
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})