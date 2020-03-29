from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post

def index(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'index.html', {'posts':posts})

def post(request):
    if request.method == 'POST':
        post = Post()
        post.main_text = request.POST['main_text']
        post.create_user = User.objects.get(username = request.user.get_username())
        post.create_date = timezone.datetime.now()
        post.save()
        return redirect(reverse('index'))
    return render(request, 'post.html')

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'detail.html', {'post': post})

def update(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        post.main_text = request.POST['main_text']
        post.create_user = User.objects.get(username = request.user.get_username())
        post.update_date = timezone.datetime.now()
        post.save()
        return redirect(reverse('index'))
    return render(request, 'update.html')

def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect(reverse('index'))