from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.db.models import Q
from django.core.mail import send_mail
from .forms import EventForm
# Create your views here.

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    events = Event.objects.filter()
    return render(request, 'events/events.html', {'template_data': template_data, 'events': events,})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            return redirect('events.about')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})