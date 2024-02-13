from django.shortcuts import redirect,render, get_object_or_404
from apps.alarm.models import Alarm
from apps.goal_management.models import Goal
from django.contrib.auth.decorators import login_required

def delete(request, pk):
    if request.method == 'POST':
        Alarm.objects.get(id=pk).delete()
    return redirect('user_management:detail')

def show_alarms(request):
    alarms = Alarm.objects.filter(alarm_to=request.user) #현재 유저일때만
    cnt = {
        'alarms':alarms,
    }
    return render(request, 'alarm/alarms.html', cnt)

def alarm_detail_as_user(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    context = {
        'alarm': alarm,
    }
    return render(request, 'alarm/alarm_detail_from_group.html', context)

def alarm_detail_as_master(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    context = {
        'alarm': alarm,
    }
    return render(request, 'alarm/alarm_detail_from_user.html', context)

def alarm_detail_direct(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    goals = Goal.objects.filter(user=alarm.alarm_to)
    context = {
        'alarm': alarm,
        'goals':goals,
    }
    return render(request, 'alarm/alarm_detail_direct.html', context)

@login_required
def accept_request(request, alarm_id):

    alarm = get_object_or_404(Alarm, id=alarm_id)
    room = alarm.room
    goal = alarm.goal
    if request.user == room.master:
        # 유저의 그룹에 대한 가입 요청 -> 요청을 보낸 유저를 방에 추가
        room.members.add(alarm.alarm_from)
        goal.is_in_group = True
        goal.belonging_group_id = room.pk
        goal.save()
    else:
        # 다른 그룹의 관리자가 유저에게 가입 제안 -> 대상이 되는 유저를 방에 추가
        room.members.add(alarm.alarm_to)
        goal.is_in_group = True
        goal.belonging_group_id = room.pk
        goal.save()

    alarm.delete()
    return redirect('alarm:show_alarms')

def accept_direct_request(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    room = alarm.room
    goal_id = request.POST.get('goal')
    goal = get_object_or_404(Goal, id=goal_id)

    room.members.add(alarm.alarm_to)
    goal.is_in_group = True
    goal.belonging_group_id = room.pk
    goal.save()
    
    alarm.delete()
    return redirect('alarm:show_alarms')

@login_required
def reject_request(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    alarm.delete()
    return redirect('alarm:show_alarms')
