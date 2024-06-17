# chat/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from chat.forms import RoomForm, TeamMessageForm
from chat.models import Room, Team, TeamRoom, TeamMessage

from accounts.models import CustomUser

@login_required
def team_rooms(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    room_qs = team.rooms.all()
    return render(request, "chat/team_rooms.html", {
        "team": team,
        "room_list": room_qs,
    })


@login_required
def room_new(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
            TeamRoom.objects.create(team_id=team.id, room=created_room)
            return redirect("chat:team_rooms", team_id=team.id)
    else:
        form = RoomForm()

    return render(request, "chat/room_new.html", {
        "form": form,
        "team": team,
    })


@login_required
def room_chat(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    team = TeamRoom.objects.filter(room=room).first().team
    messages = TeamMessage.objects.filter(room=room).order_by('timestamp')  # 기존 메시지 내역 불러오기
    return render(request, "chat/room_chat.html", {
        "room": room,
        "team": team,
        "messages": messages,
    })


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    team = TeamRoom.objects.filter(room=room).first().team
    if room.owner != request.user:
        messages.error(request, "채팅방 소유자가 아닙니다.")
        return redirect("chat:team_rooms", team_id=team.id)
    
    if request.method == "POST":
        room.delete()
        messages.success(request, "채팅방을 삭제했습니다.")
        return redirect("chat:team_rooms", team_id=team.id)

    return render(request, "chat/room_confirm_delete.html", {
        "room": room,
    })


@login_required
@csrf_exempt
def room_users(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if not room.is_joined_user(request.user):
        return HttpResponse("Unauthorized user", status=401)

    username_list = room.get_online_usernames()

    return JsonResponse({
        "username_list": username_list,
    })


def generate_chat_room_id(user1_id, user2_id):
    return f"{min(user1_id, user2_id)}-{max(user1_id, user2_id)}"


@login_required
def private_chat(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    room_id = generate_chat_room_id(request.user.id, friend.id)

    print(room_id)
    
    return render(request, 'chat/private_chat.html', {
        'room_name': room_id,
        'friend_username': friend.name
    })


    
def generate_chat_room_id(user1_id, user2_id):
    return f"{min(user1_id, user2_id)}-{max(user1_id, user2_id)}"


@login_required
def private_chat(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    room_id = generate_chat_room_id(request.user.id, friend.id)
    return redirect(f'/chat/private_chat/{room_id}/')


@login_required
@require_POST
@csrf_exempt
def send_message(request, room_pk):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=room_pk)
        message = request.POST.get('message', '').strip()
        image = request.FILES.get('image')

        if not message and not image:
            return JsonResponse({'error': 'Either message or image must be provided.'}, status=400)

        team_message = TeamMessage(room=room, sender=request.user, message=message, image=image if image and image.size > 0 else None)
        team_message.save()

        response_data = {
            'message': team_message.message,
            'image_url': team_message.image.url if team_message.image else None,
            'timestamp': team_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender': request.user.username,
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)


