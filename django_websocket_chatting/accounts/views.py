from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from .serializers import CustomUserSerializer
from .models import CustomUser


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


logout = LogoutView.as_view(
    next_page="home:front",
)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
