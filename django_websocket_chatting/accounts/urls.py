from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    # user
    path('signup/', views.signup, name='signup'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    
    # group
    path('teams_list/', views.teams_list, name='teams_list'),
    path('teams_create/', views.teams_create, name='teams_create'),
]
