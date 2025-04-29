from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import FriendRequest, Friendship, WorkoutGroup, GroupInvite, GroupMember, Challenge, ChallangeParticipation
from django.db.models import Q
from django.core.mail import send_mail
from .forms import WorkoutGroupForm, ChallengeForm
from dashboard.models import Goal

@login_required
def users(request):
    users = User.objects.exclude(id=request.user.id)
    groups = WorkoutGroup.objects.filter(groupmember__user=request.user)
    group_invites = GroupInvite.objects.filter(to_user=request.user)
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friend_ids = set()
    for friendship in friendships:
        if friendship.user1 == request.user:
            friend_ids.add(friendship.user2.id)
        else:
            friend_ids.add(friendship.user1.id)
    return render(request, 'friends/userList.html', {
        'users': users,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'friends': friend_ids,
        'groups': groups,
        'group_invites': group_invites
    })

@login_required
def sendRequest(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    send_mail(
        f"Friend Request From {request.user.username}!",
        f"Hi {to_user.username},\n\n{request.user.username} has sent you a friend request on FitJacket.\n\nPlease login to accept or decline!",
        "fitjacket.ian2@gmail.com",
        [to_user.email],
        fail_silently=False,
    )
    print(to_user.email)
    return redirect('friends:userList')


@login_required
def respondRequest(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            user1, user2 = sorted([friend_request.from_user, friend_request.to_user], key=lambda u: u.id)
            Friendship.objects.get_or_create(user1=user1, user2=user2)
            friend_request.delete()
        elif action == 'reject':
            friend_request.delete()
    return redirect('friends:userList')

@login_required
def removeFriend(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    friendship = Friendship.objects.filter((Q(user1=request.user) & Q(user2=other_user)) | (Q(user1=other_user) & Q(user2=request.user))).first()
    if friendship:
        friendship.delete()
    return redirect('friends:userList')

@login_required
def create_group(request):
    if request.method == 'POST':
        form = WorkoutGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            GroupMember.objects.create(group=group, user=request.user)
            return redirect('friends:userList')
    else:
        form = WorkoutGroupForm()
    return render(request, 'friends/create_group.html', {'form': form})

@login_required
def invite_to_group(request, group_id=None, user_id=None):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
    group = get_object_or_404(WorkoutGroup, id=group_id)
    to_user = get_object_or_404(User, id=user_id)
    if not GroupMember.objects.filter(group=group, user=request.user).exists():
        return redirect('friends:userList')
    if GroupMember.objects.filter(group=group, user=to_user).exists():
        return redirect('friends:userList')
    GroupInvite.objects.get_or_create(group=group, from_user=request.user, to_user=to_user)
    send_mail(
        f"Friend Request From {request.user.username}!",
        f"Hi {to_user.username},\n\n{request.user.username} has invited you to become a member of the following goup: {group.name}\n\nPlease login to accept or decline!",
        "fitjacket.ian2@gmail.com",
        [to_user.email],
        fail_silently=False,
    )
    return redirect('friends:userList')

def respond_group_invite(request, invite_id):
    invite = get_object_or_404(GroupInvite, id=invite_id, to_user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            GroupMember.objects.get_or_create(group=invite.group, user=request.user)
            invite.accepted = True
            invite.save()
        invite.delete()
    return redirect('friends:userList')

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    membership = GroupMember.objects.filter(group=group, user=request.user).first()
    if membership:
        membership.delete()
    return redirect('friends:userList')

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    members = GroupMember.objects.filter(group=group).select_related('user')
    goals_by_user = []
    for member in members:
        user_goals = Goal.objects.filter(user=member.user)
        goals_by_user.append((member.user, user_goals))
    challenges = Challenge.objects.filter(group=group).order_by('challenge_end_date')
    return render(request, 'friends/group.html', {
        'group': group,
        'goals_by_user': goals_by_user,
        'challenges': challenges,
    })

@login_required
def create_challenge(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            print("SUCESS")
            challenge = form.save(commit=False)
            challenge.group = group
            challenge.created_by = request.user
            challenge.save()
            return redirect('friends:groupDetail', group_id=group.id)
    else:
        form = ChallengeForm()
    return render(request, 'friends/create_challenge.html', {'form': form, 'group': group,})
