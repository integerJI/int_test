# myApp/views.py

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, Tag_2
from .forms import PostForm
from intworlduser.models import Profile
from django.contrib import messages

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

def index(request):
    posts = Post.objects.all().order_by('-id')
    app_url = request.path

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    if not conn_profile.profile_image:
        pic_url = ""
    else:
        pic_url = conn_profile.profile_image.url
            
    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'profile_pic' : pic_url,
        'intro' : conn_profile.intro,
        'posts' : posts,
        'app_url' : app_url,
    }
    return render(request, 'index.html', context=context)

def dev(request):
    return render(request, 'devpage.html')

def post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            post = form.save(commit = False)
            post.create_user = User.objects.get(username = request.user.get_username())
            post.save()
            post.tag_save()
            post.tag_save_2()
        return redirect(reverse('index'))
    else:
        form = PostForm() 
        return render(request, 'post.html', {'form' : form})

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'detail.html', {'post': post})

def update(request, post_id):
    post = Post.objects.get(id = post_id)
    conn_profile = User.objects.get(username = request.user.get_username())
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            if conn_profile == post.create_user:
                post = form.save(commit=False)
                post.save()
                post.tag_save()
                post.tag_save_2()

                context = {'post': post, 'form': form}
                content = request.POST.get('content')
                        
                messages.info(request, '수정 완료')
                return render(request, 'detail.html', context=context)
                
            else:
                messages.info(request, '수정할 수 없습니다.')
                return render(request, 'detail.html', {'post': post})
    else:
        if conn_profile == post.create_user:
            form = PostForm(instance = post)
            return render(request, 'update.html', {'post': post, 'form': form})
        else:
            messages.info(request, '수정할 수 없습니다.')
            return redirect(reverse('index'), post_id)

def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    conn_profile = User.objects.get(username = request.user.get_username())

    if conn_profile == post.create_user:
        post.delete()
        return redirect(reverse('index'))
    else:
        messages.info(request, '삭제할 수 없습니다.')
        return render(request, 'detail.html', {'post': post})


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

@login_required
def c_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)   

    conn_profile = User.objects.get(username = request.user.get_username())

    if conn_profile == comment.comment_user:
        comment.delete()
        return redirect(reverse('index'), post_id)
    else:
        messages.info(request, '삭제할 수 없습니다.')
        return redirect(reverse('index'), post_id)

@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user 
        create_user = request.POST.get('pk', None)
        post = get_object_or_404(Post, id=create_user)

        if post.likes.filter(id = user.id).exists():
            post.likes.remove(user) 
            message = '좋아요 취소'
        else:
            post.likes.add(user)
            message = '좋아요!'

    context = {'likes_count' : post.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')

def search(request, tag=None, tag_2=None):
    posts = Post.objects.all().order_by('-id')
    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    if not conn_profile.profile_image:
        pic_url = ""
    else:
        pic_url = conn_profile.profile_image.url

    q = request.POST.get('q', False)
    y = request.POST.get('y', False) 

    if tag:
        posts = Post.objects.filter(tag_set__tag_name__iexact=tag).prefetch_related('tag_set').select_related('create_user').order_by('-id')
        if y:
            posts = Post.objects.filter(tag_set_2__tag_name_2__iexact=y).prefetch_related('tag_set_2').select_related('create_user').order_by('-id')

    elif tag_2:
        posts = Post.objects.filter(tag_set_2__tag_name_2__iexact=tag_2).prefetch_related('tag_set_2').select_related('create_user').order_by('-id')
        if y:
            posts = Post.objects.filter(tag_set__tag_name__iexact=y).prefetch_related('tag_set').select_related('create_user').order_by('-id')
    elif q:
        posts = posts.filter(main_text__icontains=q).order_by('-id')
    
    else:
        messages.info(request, '입력된 값이 없습니다.')
        return redirect('index')

    return render(request, 'search.html', {'posts' : posts, 'pic_url' : pic_url, 'q' : q, 'tag': tag})
    
