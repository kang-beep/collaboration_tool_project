from django.urls import path
from teams import views

app_name = "teams"

urlpatterns = [
    # group
    path('teams_list/', views.teams_list, name='teams_list'),
    path('teams_create/', views.teams_create, name='teams_create'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
    
    # invate
    path('invite_user/<int:team_id>/', views.invite_user, name='invite_user'),
    path('accept_invitation/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
    path('reject_invitation/<int:invitation_id>/', views.reject_invitation, name='reject_invitation'),
    path('leave_team/<int:team_id>/', views.leave_team, name='leave_team'),
    path('get_invitations/', views.get_invitations, name='get_invitations'),
]
