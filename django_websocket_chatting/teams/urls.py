from django.urls import path
from teams import views

app_name = "teams"

urlpatterns = [
    # group
    path('teams_list/', views.teams_list, name='teams_list'),
    path('teams_create/', views.teams_create, name='teams_create'),
]