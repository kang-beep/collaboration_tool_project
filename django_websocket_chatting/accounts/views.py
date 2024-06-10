from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomUserSerializer, FriendRequestSerializer
from .models import CustomUser, FriendRequest

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            password2 = serializer.validated_data.get('password2')
            if password != password2:
                return Response({"password": ["비밀번호가 일치하지 않습니다."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # 비밀번호 해쉬화
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
            user = serializer.save()

            # 자동 로그인
            # user = authenticate(username=serializer.validated_data.get('username'), password=password)
            # if user is not None:
            #     login(request, user)
            return redirect('accounts:login')  # 회원가입 성공 시 이동할 페이지
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print(request , "request 데이터 입니다.")
        return render(request, 'accounts/signup.html')
    
    
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teams:teams_list')  # 로그인 성공 시 이동할 페이지
        else:
            return render(request, 'accounts/login.html', {'error_message': '유효하지 않은 사용자 이름 또는 비밀번호입니다.'})
    else:
        return render(request, 'accounts/login.html')
    
    
logout = LogoutView.as_view(
    next_page="home:front",
)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# 친구 요청을 보내는 엔드 포인트 
class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer
    
    def create(self, request, *args, **kwargs):
        print(request.data.get('to_user'))
        to_user = get_object_or_404(CustomUser, username=request.data.get('to_user'))
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'detail': 'Friend request sent.'}, status=status.HTTP_201_CREATED)

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
    

# 친구 프로필 데이터 반환
@login_required
@require_GET
def friend_profile(request):
    friend_id = request.GET.get('id')
    friend = get_object_or_404(CustomUser, id=friend_id)
    profile_data = {
        'username': friend.username,
        'name': friend.name,
        'email': friend.email,
        'id': friend.id,
    }
    return JsonResponse(profile_data)
