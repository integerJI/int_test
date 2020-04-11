from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.conf import settings
from .forms import UserCreationMultiForm, ProfileForm, ProfileUpdateForm
from .models import Profile

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
                return redirect('signin')
            else:
                user = request.POST['user-username']
                user = User.objects.get(username=user)
                messages.info(request, '아이디가 중복됩니다.')
                return render(request, 'signup.html')
        else:
            messages.info(request, '비밀번호가 다릅니다.')
            return render(request, 'signup.html')
    return render(request, 'signup.html')

class Loginviews(LoginView):
    template_name = 'signin.html'
signin = Loginviews.as_view()


class LogoutViews(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
signout = LogoutViews.as_view()