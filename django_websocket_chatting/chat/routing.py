from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    path("ws/chat/rooms/<str:room_pk>/", consumers.ChatConsumer.as_asgi()),
]
# http://localhost:8123/chat/rooms/3/
