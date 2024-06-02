# 필요한 라이브러리와 모듈을 임포트합니다.
from asgiref.sync import async_to_sync  # 비동기 코드를 동기 코드로 변환해주는 유틸리티.
from channels.layers import get_channel_layer   # Django Channels에서 채널 레이어를 가져오는 함수
from django.conf import settings    # Django 설정 모듈
from django.db import models    # Django ORM에서 사용되는 모델 모듈
from django.db.models.signals import post_delete    # DJango의 모델이 삭제될 때 실행되는 시그널
from config.json_extended import ExtendedJSONEncoder, ExtendedJSONDecoder   # 사용자 정의 JSON 인코더 및 디코더
from accounts.models import Team

# 온라인 상태인 사용자를 관리하는 Mixin 클래스입니다.
class OnlineUserMixin(models.Model):
    # 이 클래스는 DB 테이블로 만들어지지 않는 추상 클래스로 정의합니다.
    class Meta:
        abstract = True

    # 온라인 사용자 목록을 ManyToMany 필드로 관리합니다.
    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,    # 사용자 모델을 참조합니다.
        through="RoomMember",        # 중간 모델로 RoomMember를 사용합니다.
        blank=True,                  # 빈 상태도 허용합니다.
        related_name="joined_room_set",  # 역 참조 설정입니다.
    )

    # 현재 온라인인 사용자들을 반환하는 메소드입니다.
    def get_online_users(self):
        return self.online_user_set.all()

    # 온라인 사용자의 '이름'만 리스트로 반환합니다.
    def get_online_usernames(self):
        qs = self.get_online_users().values_list("username", flat=True)
        return list(qs)

    # 사용자가 온라인 상태인지 확인합니다.
    def is_joined_user(self, user):
        return self.get_online_users().filter(pk=user.pk).exists()

    # 사용자가 채팅방에 입장할 때의 동작을 정의합니다.
    def user_join(self, channel_name, user):
        try:
            # RoomMember 모델에서 현재 채팅방('self')과 사용자를 기준으로 객체를 검색
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            # 해당 객체가 없으면 새 RoomMember 객체를 생성
            room_member = RoomMember(room=self, user=user)

        # room_member.channel_names가 비어있는지 확인 비어있으면 사용자가 처음으로 입장했다는 것을 알림
        is_new_join = len(room_member.channel_names) == 0

        # 사용자의 channel_name을 room_member의 channel_names 필드에 추가합니다. 
        room_member.channel_names.add(channel_name)

        # room_member 객체가 데이터베이스에 아직 저장되지 않았다면('pk가 None')객체를 새로 저장합니다.
        if room_member.pk is None:
            room_member.save()
        else:
            room_member.save(update_fields=["channel_names"])

        return is_new_join

    # 사용자가 채팅방에서 나갈 때의 동작을 정의합니다.
    def user_leave(self, channel_name, user):
        try:
            # RoomMember 모델에서 현재 채팅방('self')과 사용자를 기준으로 객체를 검색합니다.
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            # 사용자가 채팅방에 없으면 예외를 던져 True를 반환하고 함수 종료
            return True

        # 사용자의 channel_name을 room_member의 channel_names필드에서 제거
        room_member.channel_names.remove(channel_name)
        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member.save(update_fields=["channel_names"])
            return False


# Team, Room 중간 테이블 정의
class TeamRoom(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_rooms')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='team_rooms')

# 채팅방을 나타내는 모델입니다.
class Room(OnlineUserMixin, models.Model):
    # 채팅방의 주인을 나타내는 필드입니다.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_room_set",
    )
    # 채팅방의 이름을 나타내는 필드입니다.
    name = models.CharField(max_length=100)
    ##### 여기에 forms.py의 필드에 Description 필드를 추가할 수 있도록 모델에 추가가 필요한데, 이 부분은 논의하기
    # TeamRoom 모델과 다대다 연결
    teams = models.ManyToManyField(Team, through='TeamRoom', related_name='rooms', verbose_name='소속 팀')

    # 채팅방을 최신 생성 순으로 정렬합니다.
    class Meta:
        ordering = ["-pk"]

    # 채팅방의 그룹 이름을 반환하는 프로퍼티입니다.
    @property
    def chat_group_name(self):
        return self.make_chat_group_name(room=self)

    # 채팅방의 그룹 이름을 생성하는 메소드입니다.
    @staticmethod
    def make_chat_group_name(room=None, room_pk=None):
        return "chat-%s" % (room_pk or room.pk)

# 채팅방이 삭제되었을 때 호출되는 함수입니다.
def room__on_post_delete(instance: Room, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.chat_group_name,
        {
            "type": "chat.room.deleted",
        }
    )

# post_delete 시그널에 위에서 정의한 함수를 연결합니다.
post_delete.connect(
    room__on_post_delete,
    sender=Room,
    dispatch_uid="room__on_post_delete",
)

# 채팅방의 멤버와 관련된 정보를 저장하는 모델입니다.
class RoomMember(models.Model):
    # 해당 멤버의 사용자 정보입니다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 해당 멤버가 속한 채팅방입니다.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # 사용자의 채널 이름들을 저장하는 JSON 필드입니다.
    channel_names = models.JSONField(
        default=set,   # 기본값은 빈 set입니다.
        encoder=ExtendedJSONEncoder,  # 사용자 정의 JSON 인코더
        decoder=ExtendedJSONDecoder,  # 사용자 정의 JSON 디코더
    )
