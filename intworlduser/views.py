from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationMultiForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['user-password1'] == request.POST['user-password2']:
            form = UserCreationMultiForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form['user'].save()
                profile = form['profile'].save(commit=False)
                profile.user = user
                profile.nick = user
                profile.save()
                return redirect('login')
            else:
                user = request.POST['user-username']
                user = User.objects.get(username=user)
                # messages.info(request, '아이디가 중복됩니다.')
                return render(request, 'signup.html')
        else:
            # messages.info(request, '비밀번호가 다릅니다.')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
    else:
        return render(request, 'signin.html')

def signout(request):
    return render(request, 'signin.html')