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