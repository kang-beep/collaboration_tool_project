# 필요한 함수와 클래스를 가져옵니다.
from asgiref.sync import async_to_sync, sync_to_async  # 비동기 함수를 동기식으로 호출하기 위해 사용됩니다.
from channels.generic.websocket import JsonWebsocketConsumer, AsyncWebsocketConsumer  # WebSocket에 대한 기본 컨슈머 클래스입니다.
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from chat.models import Room, PrivateMessage, TeamMessage  # chat.models Room,PrivateMessage 모델을 가져옵니다.
from datetime import datetime  # 타임스탬프를 위해 datetime 모듈을 가져옵니다.
from accounts.models import CustomUser

import json
import base64
from django.core.files.base import ContentFile

# ChatConsumer 정의. JsonWebsocketConsumer의 하위 클래스입니다.
class ChatConsumer(JsonWebsocketConsumer):

    # ChatConsumer의 생성자 함수입니다.
    def __init__(self, *args, **kwargs):
        # 상위 클래스의 생성자를 호출합니다.
        super().__init__(args, kwargs)
        self.group_name = ""  # group_name을 빈 문자열로 초기화합니다.
        self.room = None  # room 객체를 None으로 초기화합니다.

    # WebSocket이 연결 과정 중일 때 호출됩니다.
    def connect(self):
        user = self.scope["user"]  # scope에서 사용자를 가져옵니다.

        # 사용자가 인증되지 않았다면 WebSocket 연결을 종료합니다.
        if not user.is_authenticated:
            self.close()
        else:
            # url 경로에서 방의 기본 키를 가져옵니다.
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]

            try:
                # 기본 키를 통해 Room 객체를 가져옵니다.
                self.room = Room.objects.get(pk=room_pk)
            except Room.DoesNotExist:
                # 방이 존재하지 않으면 WebSocket 연결을 종료합니다.
                self.close()
            else:
                # room 객체에서 그룹 이름을 가져옵니다.
                self.group_name = self.room.chat_group_name

                # 사용자를 방에 추가하고 새로운 참가자인지 확인합니다.
                is_new_join = self.room.user_join(self.channel_name, user)
                if is_new_join:
                    # 새로운 사용자라면 그룹에 참가 알림을 보냅니다.
                    async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            "type": "chat.user.join",
                            "username": user.username,
                        }
                    )

                # 현재 채널을 그룹에 추가합니다.
                async_to_sync(self.channel_layer.group_add)(
                    self.group_name,
                    self.channel_name,
                )

                # WebSocket 연결을 수락합니다.
                self.accept()

    # WebSocket이 닫힐 때 호출됩니다.
    def disconnect(self, code):
        # group_name이 있으면 현재 채널을 그룹에서 제거합니다.
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )

        user = self.scope["user"]

        # room 객체가 있으면 사용자가 마지막으로 나가는지 확인합니다.
        if self.room is not None:
            is_last_leave = self.room.user_leave(self.channel_name, user)
            if is_last_leave:
                # 사용자가 마지막이라면 그룹에 나가기 알림을 보냅니다.
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chat.user.leave",
                        "username": user.username,
                    }
                )

    # 서버가 WebSocket으로부터 메시지를 받을 때 호출됩니다.
    def receive_json(self, content, **kwargs):
        user = self.scope["user"]

        _type = content["type"]

        # 메시지 유형이 채팅 메시지인 경우.
        if _type == "chat.message":
            sender = user.username
            message = content["message"]
            image_data = content.get("image")
            timestamp = content.get("timestamp", datetime.now().strftime("%H:%M:%S"))
            
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name=f'{user.username}_{timestamp}.{ext}')
            else:
                image = None

            team_message = TeamMessage(room=self.room, sender=user, message=message)
            if image:
                team_message.image.save(f"{user.username}_{timestamp}.{ext}", image)
            team_message.save()
            
            # 그룹에 채팅 메시지를 전송합니다.
            message_dict = {
                "type": "chat.message",
                "message": message,
                "sender": sender,
                "timestamp": timestamp,
            }
            if image:
                message_dict["image_url"] = team_message.image.url

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                message_dict
            )
        else:
            print(f"잘못된 메시지 유형 : ${_type}")

    # 사용자가 채팅에 참가할 때의 처리입니다.
    def chat_user_join(self, message_dict):
        self.send_json({
            "type": "chat.user.join",
            "username": message_dict["username"],
        })

    # 사용자가 채팅에서 나갈 때의 처리입니다.
    def chat_user_leave(self, message_dict):
        self.send_json({
            "type": "chat.user.leave",
            "username": message_dict["username"],
        })

    # 전송된 채팅 메시지를 처리하는 함수입니다.
    def chat_message(self, message_dict):
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"],
            "sender": message_dict["sender"],
            "timestamp": message_dict["timestamp"],  # 타임스탬프를 포함합니다.
            "image_url": message_dict["image_url"],  # 이미지 URL을 포함합니다.
        })

    # 채팅방이 삭제될 때의 처리입니다.
    def chat_room_deleted(self, message_dict):
        custom_code = 4000  # 방 삭제에 대한 사용자 정의 코드입니다.
        self.close(code=custom_code)  # 사용자 정의 코드로 WebSocket을 닫습니다.


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        print("consumers.py room_id recived", self.room_id)
        self.room_group_name = f'private_chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']

        user1_id, user2_id = map(int, self.room_id.split('-'))
        receiver_id = user2_id if sender.id == user1_id else user1_id
        receiver = await sync_to_async(CustomUser.objects.get)(id=receiver_id)

        if sender.is_authenticated:
            await sync_to_async(PrivateMessage.objects.create)(
                sender=sender, receiver=receiver, message=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'sender_id': sender.id,
                    'sender_name': sender.name,  # 추가된 부분

                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        sender_id = event['sender_id']
        sender_name = event['sender_name']  # 추가된 부분
        
        print(sender_name,"sender_name")
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sender_id': sender_id,
            'sender_name': sender_name,  # 추가된 부분

        }))

    @database_sync_to_async
    def get_receiver(self, username):
        return CustomUser.objects.get(username=username)

    @database_sync_to_async
    def create_private_message(self, sender, receiver, message):
        return PrivateMessage.objects.create(sender=sender, receiver=receiver, message=message)