from django.urls import path
from chat import views

app_name = "chat"

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("test/", views.index, name="test"),
#     path("new/", views.room_new, name="room_new"),
#     path("<str:room_pk>/chat/", views.room_chat, name="room_chat"),
#     path("<str:room_pk>/delete/", views.room_delete, name="room_delete"),
#     path("<int:room_pk>/users/", views.room_users, name="room_users"),

    
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('teams/<int:team_id>/', views.team_rooms, name='team_rooms'),
    path('teams/<int:team_id>/rooms/new/', views.room_new, name='room_new'),
    path('rooms/<int:room_pk>/', views.room_chat, name='room_chat'),
    path('rooms/<int:room_pk>/delete/', views.room_delete, name='room_delete'),
    path('rooms/<int:room_pk>/users/', views.room_users, name='room_users'),
]