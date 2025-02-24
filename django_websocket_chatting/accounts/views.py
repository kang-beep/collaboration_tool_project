from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods

from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomUserSerializer, FriendRequestSerializer
from .models import CustomUser, FriendRequest

app_name = 'accounts'

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            password2 = serializer.validated_data.get('password2')
            if password != password2:
                return render(request, 'accounts/signup.html', {
                    'error_message': "비밀번호가 일치하지 않습니다.",
                    'form': request.data,
                })
            
            # 비밀번호 해쉬화
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            serializer.save()

            return redirect('accounts:login')  # 회원가입 성공 시 이동할 페이지
        return render(request, 'accounts/signup.html', {
            'errors': serializer.errors,
            'form': request.data,
        })
    return render(request, 'accounts/signup.html')


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'error_message': '로그인 정보가 올바르지 않습니다.'}, status=400)
    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': 'Logged out successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def profile(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        file_name = default_storage.save(f"profile_pictures/{profile_picture.name}", profile_picture)
        request.user.profile_picture = file_name
        request.user.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user': request.user})


# 친구 요청을 보내는 엔드 포인트 
class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    
    def create(self, request, *args, **kwargs):
        username =request.data.get('to_user')
        try:
            to_user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': '등록된 유저가 조회되지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        to_user = get_object_or_404(CustomUser, username=request.data.get('to_user'))
        
        
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'detail': '이미 친구요청을 보낸 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'detail': '친구요청을 보냈습니다!'}, status=status.HTTP_201_CREATED)

# 친구 요청을 수락하는 API 엔드포인트
class AcceptFriendRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    
    def update(self, request, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, pk=kwargs['pk'])
        if friend_request.to_user != request.user:
            return Response({'detail': 'Not your friend request. '}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.accept()
        return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)

# 친구 요청을 거부하는 API 엔드포인트
class RejectFriendRequestView(generics.DestroyAPIView):
    permission_calsses = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs ):
        friend_request = get_object_or_404(FriendRequest, pk=kwargs['pk'])
        if friend_request.to_user != request.user:
            return Response({'detail': 'Not your friend request.'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.reject()
        return Response({'detail': 'Friend request rejected.'}, status=status.HTTP_204_NO_CONTENT)

# 사용자의 친구 목록을 조회하는 API 엔드포인트=
class ListFriendsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        return self.request.user.friends.all()
    
# 친구 기능 html 템플릿 렌더링 뷰
@login_required
def friend_management(request):
    friends = request.user.friends.all()
    received_requests = request.user.received_requests.filter(accepted=False)
    sent_requests = request.user.sent_requests.filter(accepted=False)
    return render(request, 'friends/friend_management.html', {
        'friends': friends,
        'received_requests':received_requests,
        'sent_requests': sent_requests
    })
    

# 자신의 친구들 반환
@login_required
def get_friends_list(request):
    friends = request.user.friends.all()
    friends_data = [{'id': friend.id, 'username': friend.username, 'name': friend.name, 'is_online': friend.is_online,} for friend in friends]
    return JsonResponse({'friends': friends_data})

# 요청된 친구 요청들을 반환
@login_required
@require_http_methods(["GET"])
def get_received_friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    for req in received_requests :
        print(req, "received")
    
    print(received_requests, "received")
    data = [
        {
            'id': req.id,
            'from_user': req.from_user.username,
            'timestamp': req.timestamp,
        } for req in received_requests
    ]
    return JsonResponse({'requests': data}, status=200)


# 친구 프로필 데이터 반환
@login_required
@require_GET
def friend_profile(request):
    friend_id = request.GET.get('id')
    friend = get_object_or_404(CustomUser, id=friend_id)
    print(friend.is_online)
    data = {
        'username': friend.username,
        'name' : friend.name,
        'email': friend.email,
        'profile_picture': friend.profile_picture.url if friend.profile_picture else '',
        'is_online' : friend.is_online,
        
    }
    return JsonResponse(data)

# 등록된 친구를 삭제하는 기능
@login_required
@require_http_methods(["DELETE"])
def remove_friend(request, friend_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=friend_id)

    if friend not in user.friends.all():
        return JsonResponse({'detail': 'Not your friend.'}, status=400)

    user.friends.remove(friend)
    friend.friends.remove(user)

    return JsonResponse({'detail': 'Friend removed successfully.'}, status=204)
