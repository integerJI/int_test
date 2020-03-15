from django import forms
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
        'user' : CreateUserForm,
        'birth_date' : ProfileForm,
    }

class UserSignupView(generic.CreateView):
    form_class = UserCreationMultiForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form['user'].save()
        profile = form['profile'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.success_url)