from django.db import models
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django import forms

class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

        user = models.OneToOneField(User, on_delete=models.CASCADE)
        # OneToOneField를 통해 Django에서 제공하는 User과 1:1로 묶는다.
        # ForeginKet와 개념적으로 같지만 둘의 차이점은 역관계에 있다.
        # 역관계란? https://whatisthenext.tistory.com/118
        # OneToOneField가 바라보는 값이 삭제될때 OneToOneField를 포함한 모델 인스턴스(row)도 삭제된다.
        name = models.CharField(max_length=50)
        intro = models.TextField(blank=True, max_length=200)
        # blank=True는 폼에서 입력을 할때 빈값을 입력할수 있게 해준다.
        # 저장될땐 장고는 NULL을 저장하지 않으므로 빈 문자열 ('')이 저장된다.
        profile_image = models.ImageField(blank=True, upload_to='user/%Y/%m/%d/')
    	# 저장경로 : MEDIA_ROOT/user/%Y/%m/%d/*.jpg 경로에 저장
	    # DB필드 : 'MEDIA_URL/user/%Y/%m/%d/*.jpg' 문자열 저장


    def __str__(self):
        return self.name