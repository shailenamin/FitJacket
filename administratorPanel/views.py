from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.

def emailUsers(request):
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