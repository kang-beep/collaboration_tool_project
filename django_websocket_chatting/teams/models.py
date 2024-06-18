from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='팀 이름')

    description = models.TextField(null=True, blank=True, verbose_name='팀 설명')

    team_image = models.ImageField(upload_to='team_image/', null=True, blank=True, verbose_name='팀 사진')

    def __str__(self):
        return self.name