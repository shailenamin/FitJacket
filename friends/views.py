from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import FriendRequest

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    received_requests = FriendRequest.objects.filter(to_user=request.user)

    return render(request, 'friends/userList.html', {
        'users': users,
        'sent_requests': sent_requests,
        'received_requests': received_requests
    })

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('friends:user_list')


@login_required
def respond_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            friend_request.delete()
        elif action == 'reject':
            friend_request.delete()
    return redirect('friends:user_list')
