from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    main_text = models.CharField(max_length=200)
    create_user = models.ForeignKey(User, on_delete = models.CASCADE)
    create_date = models.DateTimeField('date published')
    update_date = models.DateTimeField('date published', null = True)

    def __str__(self):
        return self.main_text
