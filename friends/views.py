from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import FriendRequest, Friendship
from django.db.models import Q
from django.core.mail import send_mail

@login_required
def users(request):
    users = User.objects.exclude(id=request.user.id)
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friend_ids = set()
    for friendship in friendships:
        if friendship.user1 == request.user:
            friend_ids.add(friendship.user2.id)
        else:
            friend_ids.add(friendship.user1.id)
    return render(request, 'friends/userList.html', {'users': users,'sent_requests': sent_requests,'received_requests': received_requests,'friends': friend_ids,})

@login_required
def sendRequest(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    send_mail(
        f"You Have A New Friend Request From {request.user.username}!",
        f"Hi {to_user.username},\n\n{request.user.username} has sent you a friend request on FitJacket. Please login to accept or deline!",
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