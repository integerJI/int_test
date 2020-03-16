from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick', 'birth_date',]

class UserCreationMultiForm(MultiModelForm):
    form_class = {
        'user' : UserCreationForm,
        'birth_date' : ProfileForm,
    }