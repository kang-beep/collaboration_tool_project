from django.urls import path
from accounts import views


app_name = "accounts"

urlpatterns = [
    # user
    path('signup/', views.signup, name='signup'),
    path("login/", views.user_login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile, name="profile"),
    
    # friend url
    path('friend-request/send/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:pk>/', views.AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/reject/<int:pk>/', views.RejectFriendRequestView.as_view(), name='reject-friend-request'),
    
    path('friends/', views.ListFriendsView.as_view(), name='list_friends'),
    path('friend-management/', views.friend_management, name='friend_management'),
    path('friend-profile/', views.friend_profile, name='friend_profile'),   # Friend profile
    path('get-friends-list/', views.get_friends_list, name='get_friends_list'), # return Friend list
    path('friend-requests/received/', views.get_received_friend_requests, name='get_received_friend_requests'), # get received list
    
    path('friend/remove/<int:friend_id>/', views.remove_friend, name='remove-friend'),
]
