from django.conf import settings
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='팀 이름')
    
    description = models.TextField(null=True, blank=True, verbose_name='팀 설명')
    
    team_image = models.ImageField(upload_to='team_image/', null=True, blank=True, verbose_name='팀 사진')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams', verbose_name='팀 소유자', null=True, blank=True)
    
    def __str__(self):
        return self.name