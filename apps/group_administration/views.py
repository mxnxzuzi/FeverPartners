from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from elastic_transport import Serializer
from apps.alarm.models import Alarm
from apps.goal_management.models import Goal
from apps.group_management.models import Room, User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
import json
from .decorators import room_admin_required
from django.urls import reverse

from django.contrib.auth.decorators import login_required
# 이 부분 나중에 수정되어야 함
@room_admin_required
def show_admin_page(request, room_id):
    room = Room.objects.get(pk=room_id)
    ctx = {
        'room_id':room_id,
        'room': room,
    }
    return render(request, 'group_administration/group_admin_base.html', ctx)

@room_admin_required
def show_member_list(request, room_id):
    master = Room.objects.get(pk=room_id).master
    members = Room.objects.get(pk=room_id).members.exclude(pk=master.pk)
    room = Room.objects.get(pk=room_id)
    cnt = {
        'members':members,
        'room_id':room_id,
        'room': room,
    }
    return render(request, 'group_administration/group_member_list.html', cnt)

@require_http_methods(["DELETE"])
def expel_member(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        member_id = data.get('memberId')

        room = Room.objects.get(pk=room_id)
        member = room.members.get(pk=member_id)

        # 추방에 따른 로직 => 관련 정보 수정 및 초기화
        target_goal = member.goal.filter(belonging_group_id=room_id).first()
        target_goal.is_in_group = False
        target_goal.belonging_group_id = None
        target_goal.save()

        room.members.remove(member)
        return JsonResponse({'message': '멤버가 성공적으로 삭제되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)

@require_http_methods(["POST"]) 
def transfer_master(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        member_id = data.get('memberId')

        room = Room.objects.get(pk=room_id)
        room.master = room.members.get(pk=member_id)
        room.save()

        return JsonResponse({'message': '권한이 성공적으로 양도되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)

@room_admin_required
def activate_room(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        room.is_active = True
        room.save()
        url = reverse('group_activity:member_list', kwargs={'room_id': room_id})
        return redirect(url)
    except Exception:
        return HttpResponse(status=404)

@require_http_methods(["DELETE"])
def delete_room(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        room = Room.objects.get(pk=room_id)

        # 폐쇄에 따른 로직 => 모든 멤버의 Goal 정보 수정 및 초기화(Master본인 포함)
        members = room.members.all()
        for member in members:
            target_goal = member.goal.filter(belonging_group_id=room_id).first()
            target_goal.is_in_group = False
            target_goal.belonging_group_id = None
            target_goal.save()

        room.delete()

        return JsonResponse({'message': '폐쇄 작업이 성공적으로 완료되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)
    
def invited_member(request, room_id):
    master = Room.objects.get(pk=room_id).master
    members = Room.objects.get(pk=room_id).members.exclude(pk=master.pk)
    room = Room.objects.get(pk=room_id)
    cnt = {
        'members':members,
        'room_id':room_id,
        'room': room,
    }
    return render(request, 'group_administration/group_invited_member.html', cnt)

def search_user(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            results = User.objects.filter(nickname__icontains=query)
            data = [{'id': user.id, 'nickname': user.nickname} for user in results]
            print(data)
            return JsonResponse({'results': data})
        else:
            return JsonResponse({'results': []})
    else:
        return JsonResponse({'error': 'GET 요청이 필요합니다.'}, status=400)
    
def suggest_join(request, user_id):
    if request.method == 'POST':
        room_id = request.POST.get('room_id') 
        user = get_user_model().objects.get(pk=user_id)
        room = get_object_or_404(Room, id=room_id)
        # 새 알람 객체 생성 시 인스턴스로 변환된 사용자를 할당
        Alarm.objects.create(alarm_from=request.user, alarm_to=user, room=room)
        return redirect('/')
    else:
        return redirect('/')  # POST 요청이 아닌 경우 홈페이지로 리다이렉트
