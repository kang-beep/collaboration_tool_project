from django.conf import settings
from django.db import models

#주석
class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='팀 이름')
    
    description = models.TextField(null=True, blank=True, verbose_name='팀 설명')
    
    team_image = models.ImageField(upload_to='team_image/', null=True, blank=True, verbose_name='팀 사진')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams', verbose_name='팀 소유자', null=True, blank=True)
    
    @property
    def members(self):
        return self.users.all()

    def __str__(self):
        return self.name

class TeamInvitation(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_team_invitations', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_team_invitations', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user', 'team')

    def accept(self):
        self.accepted = True
        self.save()
        self.team.users.add(self.to_user)

    def reject(self):
        self.delete()
