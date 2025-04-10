from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.

def add(request):
    template_data = {}
    template_data['title'] = 'Fit Jacket'
    template_data = {}
    template_data['title'] = 'Fit Jacket'
    if request.method == 'GET':
        return render(request, 'administratorPanel/email.html', {'template_data': template_data})
    elif request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        receivers = []
        for user in User.objects.all():
            receivers.append(user.email)
        send_mail(
            subject,
            message,
            "fitjacket.ian2@gmail.com",
            receivers,
            fail_silently=False,
        )
        return redirect('administratorPanel.index')

from django.shortcuts import get_object_or_404, redirect
from .models import MyUser

def add_friend(request, user_id):
    user = get_object_or_404(MyUser, user_id=request.user.id)
    friend = get_object_or_404(MyUser, user_id=user_id)
    user.friends.add(friend)
    return redirect('profile')

def remove_friend(request, user_id):
    user = get_object_or_404(MyUser, user_id=request.user.id)
    friend = get_object_or_404(MyUser, user_id=user_id)
    user.friends.remove(friend)
    return redirect('profile')