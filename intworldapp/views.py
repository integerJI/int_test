from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment

def index(request):
    posts = Post.objects.order_by('-id')
    app_url = request.path
    return render(request, 'index.html', {'posts':posts, 'app_url':app_url})

def post(request):
    if request.method == 'POST':
        post = Post()
        post.main_text = request.POST['main_text']
        post.create_user = User.objects.get(username = request.user.get_username())
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
        post.save()
        return redirect(reverse('index'))
    return render(request, 'update.html')

def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect(reverse('index'))


@login_required
def c_post(request, post_id):
    if request.method =='POST':
        comment = get_object_or_404(Post, id=post_id)
        comment_text = request.POST.get('comment_text')
        comment_user = User.objects.get(username = request.user.get_username())
        Comment.objects.create(comment=comment, comment_text=comment_text, comment_user=comment_user)

        if request.POST.get('app_url') == '/intworldapp/index/':
            return redirect(reverse('index'), post_id)
        else :
            return redirect('detail', post_id)