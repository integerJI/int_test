from django import forms
from django.db import models
from .models import Profile
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False) 
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'intro',]

class UserCreationMultiForm(MultiModelForm):
    form_classes = {
        'user' : CreateUserForm,
        'profile' : ProfileForm,
    }
        