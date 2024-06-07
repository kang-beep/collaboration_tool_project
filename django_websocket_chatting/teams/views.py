from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from rest_framework.decorators import api_view
from rest_framework import serializers,status
from rest_framework.response import Response

from .serializers import TeamSerializer
from .models import Team
# Create your views here.

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
            return redirect('teams:teams_list')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
