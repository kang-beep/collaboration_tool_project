from django.db import models
from django.contrib.auth.models import AbstractUser
from teams.models import Team
# Create your models here.


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
    
    
class Friendship(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    DECLINED = 'D'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]
    
    from_user = models.ForeignKey(CustomUser, related_name='friendships_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.get_status_display()})"

    
    