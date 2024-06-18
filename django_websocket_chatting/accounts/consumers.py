import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class StatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            await self.update_user_status(self.user, True)
            await self.accept()
            
    async def disconnect(self, close_code):
        if hasattr(self, 'user'):
            await self.update_user_status(self.user, False)
    
    @database_sync_to_async
    def update_user_status(self, user, is_online):
        user.is_online = is_online
        user.save()
        
    async def send_user_status(self):
        await self.channel_layer.group_send(
            "status_updates",
            {
                "type": "user_status",
                "user_id": self.user.id,
                "is_online": self.user.is_online,
            },
        )

    async def user_status(self, event):
        await self.send_json(event)