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
    
    # 친구 목록 필드 추가 
    friends = models.ManyToManyField('self', blank=True)
    
# 친구 요청 모델
class FriendRequest(models.Model):
    
    # 친구 요청을 보낸 사용자
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    # 친구 요청을 받은 사용자
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    # 친구 요청이 생성된 시간
    timestamp = models.DateTimeField(auto_now_add=True)
    # 친구 요청이 수락되었는지 여부
    accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    # 친구 요청을 수락하고, 요청을 보낸 사용자와 받은 사용자를 서로의 친구 목록에 추가
    def accept(self):
        self.accepted = True
        self.save()
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)
    
    # 친구 요청을 거부하고 요청을 삭제
    def reject(self):
        self.delete()
    
    