from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intro = models.TextField(blank=True, max_length=200, )
    profile_image = models.ImageField(blank=True, upload_to='usr')

    def __str__(self):
        return self.user