from django.contrib import admin
from chat.models import Room, RoomMember

# 방 관리자 기능 구현 할 것
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    pass
