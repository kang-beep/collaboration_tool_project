from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='팀 이름')

    description = models.TextField(null=True, blank=True, verbose_name='팀 설명')

    team_image = models.ImageField(upload_to='team_image/', null=True, blank=True, verbose_name='팀 사진')

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    # 기존 필드인 username, password, email은 AbstractUser 모델에 이미 존재

    # 이름 필드 추가 
    name = models.CharField(max_length=100, verbose_name='이름')
    
    # '연락처' 필드 추가
    contact = models.CharField(max_length=20, verbose_name='연락처', null=True)

    # 프로필 사진 필드 추가
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='프로필 사진')
    
    # 다대다 관계 설정
    teams = models.ManyToManyField(Team, related_name='users', verbose_name='소속 팀')