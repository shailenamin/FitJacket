from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .models import Event, Participation
from .forms import EventForm

# View to list events
def about(request):
    events = Event.objects.order_by('event_date')# ✅ Sorted upcoming events
    if request.user.is_authenticated:
        for event in events:
            event.is_joined = Participation.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/events.html', {'events': events})

# View to create a new event
@login_required
def create_group(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, '🎉 Event created successfully!')
            return redirect('events.about')
        else:
            messages.error(request, '⚠️ Please correct the errors below.')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Participation.objects.filter(user=request.user, event=event).exists():
        return redirect('events.about')
    Participation.objects.create(user=request.user, event=event)
    send_mail(
        f"See you at {event.name}!",
        f"Hi {request.user.username},\n\nThank you for signing up for the {event.name} on {event.event_date} with FitJacket.\n\n{event.description}\n\nWe look forward to seeing you there!",
        "fitjacket.ian2@gmail.com",
        [request.user.email],
        fail_silently=False,
    )
    return redirect('events.about')