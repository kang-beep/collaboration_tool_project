from django.urls import path
from accounts import views


app_name = "accounts"

urlpatterns = [
    # user
    path('signup/', views.signup, name='signup'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    
    # friend url
    path('friend-request/send/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:pk>/', views.AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/<int:pk>/', views.RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/', views.ListFriendsView.as_view(), name='list_friends'),
    path('friend-management/', views.friend_management, name='friend_management'),
    path('friend_profile/', views.friend_profile, name='friend_profile'),   # Friend profile
]
