from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.http import HttpResponse

from workoutlogs.models import WorkoutLog
from dashboard.models import Profile



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

def warnUsersAboutStreaks(request):
    today = now().date()
    receivers = []

    for user in User.objects.all():
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            continue

        if profile.current_streak == 0:
            continue

        has_logged_today = WorkoutLog.objects.filter(
            user=user,
            created_at__date=today
        ).exists()

        if not has_logged_today:
            receivers.append(user.email)

    if receivers:
        send_mail(
            subject="Don't lose your streak!",
            message="You haven’t logged a workout today. Log one now to keep your streak alive.",
            from_email="fitjacket.ian2@gmail.com",
            recipient_list=receivers,
            fail_silently=False,
        )

    return HttpResponse("Streak email check complete.")
