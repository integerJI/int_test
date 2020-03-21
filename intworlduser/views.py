from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            return redirect('signin')
    return render(request, 'signup.html')

class Loginviews(LoginView):
    template_name = 'signin.html'
signin = Loginviews.as_view()


class LogoutViews(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
signout = LogoutViews.as_view()