from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post

def index(request):
    posts = Post.objects
    return render(request, 'index.html', {'posts':posts})

def post(request):
    if request.method == 'POST':
        post = Post()
        post.main_text = request.POST['main_text']
        post.create_user = User.objects.get(username = request.user.get_username())
        post.create_date = timezone.datetime.now()
        post.save()
        return redirect('/index/')
    return render(request, 'post.html')
