from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event
from .forms import EventForm

# View to list events
def about(request):
    events = Event.objects.order_by('event_date')  # ✅ Sorted upcoming events
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
