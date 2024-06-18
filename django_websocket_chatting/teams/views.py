import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response

from accounts.models import CustomUser

from .serializers import TeamSerializer
from .models import Team, TeamInvitation


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
        return JsonResponse({'status': 'fail', 'error': '팀의 관리자만 팀을 삭제할 수 있습니다.'}, status=403)
    try:
        team.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'error': str(e)}, status=400)


###  팀 초대 관련 부분 

@login_required
@require_POST
def invite_user(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return JsonResponse({'error': '권한이 없습니다.'}, status=403)

    data = json.loads(request.body)
    user_id = data.get('user_id')
    
    try:
        user = CustomUser.objects.get(username=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    if user in team.users.all():
        return JsonResponse({'error': '사용자는 이미 팀의 멤버입니다.'}, status=400)

    if TeamInvitation.objects.filter(to_user=user, team=team).exists():
        return JsonResponse({'error': '이미 초대 요청이 있습니다.'}, status=400)

    TeamInvitation.objects.create(from_user=request.user, to_user=user, team=team)
    return JsonResponse({'success': '초대 요청이 발송되었습니다.'}, status=200)

# 팀 초대 목록
@login_required
@require_GET
def get_invitations(request):
    invitations = TeamInvitation.objects.filter(to_user=request.user, accepted=False)
    invitation_data = [{'id': inv.id, 'team_name': inv.team.name} for inv in invitations]
    return JsonResponse({'invitations': invitation_data})

@login_required
@require_http_methods(["POST"])
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id, to_user=request.user)
    invitation.accept()
    return JsonResponse({'success': '초대 요청을 수락했습니다.'}, status=200)


@login_required
@require_http_methods(["POST", "DELETE"])
def reject_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id, to_user=request.user)
    invitation.reject()
    return JsonResponse({'success': '초대 요청을 거절했습니다.'}, status=200)


def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.users.all():
        return JsonResponse({'error': '팀의 멤버가 아닙니다.'}, status=400)

    if team.owner == request.user:
        return JsonResponse({'error': '팀 소유자는 팀을 탈퇴할 수 없습니다.'}, status=400)

    team.users.remove(request.user)
    return JsonResponse({'success': '팀에서 탈퇴했습니다.'}, status=200)

