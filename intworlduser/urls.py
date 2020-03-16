# myMember/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]