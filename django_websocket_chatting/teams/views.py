import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response

from .serializers import TeamSerializer
from .models import Team

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
            team = serializer.save(owner=request.user)
            request.user.teams.add(team)
            return redirect('teams:teams_list')
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@login_required
@require_http_methods(["DELETE"])
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return JsonResponse({'status': 'fail', 'error': '팀의 생성자만 팀을 삭제할 수 있습니다.'}, status=403)
    try:
        team.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'error': str(e)}, status=400)


