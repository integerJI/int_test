from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import re

class Post(models.Model):
    main_text = models.CharField(max_length=200)
    create_user = models.ForeignKey(User, on_delete = models.CASCADE)
    create_date = models.DateTimeField('date published', default=timezone.now)
    update_date = models.DateTimeField('date published', null = True, default=timezone.now)
    create_img = models.ImageField(blank=True, upload_to="post/%Y/%m/%d", null=True)
    likes = models.ManyToManyField(User, related_name='likes')
    tag_set = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.main_text

    @property
    def total_likes(self):
        return self.likes.count()

    # NOTE: content에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.main_text)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag)  # NOTE: ManyToManyField 에 인스턴스 추가

        
class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_text = models.CharField(max_length=200)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    comment_date = models.DateTimeField('date published', default=timezone.now)
    
    class Meta:
        ordering = ['-id']
            
    def __str__(self):
        return '%s - %s' % (self.comment_user, self.comment_text) 

class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name
