from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework import serializers,status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect

from .serializers import CustomUserSerializer, TeamSerializer
from .models import Team


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
            user = authenticate(username=serializer.validated_data.get('username'), password=password)
            if user is not None:
                login(request, user)
            return redirect('chat:index')  # 회원가입 성공 시 이동할 페이지
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
            return redirect('accounts:profile')  # 로그인 성공 시 이동할 페이지
        else:
            return render(request, 'accounts/login.html', {'error_message': '유효하지 않은 사용자 이름 또는 비밀번호입니다.'})
    else:
        return render(request, 'accounts/login.html')
    
logout = LogoutView.as_view(
    next_page="accounts:login",
)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
@api_view(['GET'])
def teams_list(request):
    user = request.user
    teams = user.teams.all()  # 현재 유저가 속한 팀 목록
    return render(request, 'team/teams_list.html', {'teams': teams})


@login_required
@api_view(['GET', 'POST'])
def teams_create(request):
    
    if request.method == 'GET':
        teams = Team.objects.all()
        form = TeamSerializer()
        return render(request, 'team/teams_create.html', {'teams': teams, 'form': form})


    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save()
            request.user.teams.add(team)
            return redirect('accounts:teams_list')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
