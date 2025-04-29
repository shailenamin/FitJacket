from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render
from .models import WorkoutLog


def workout_logs(request):
    logged_workout = None
    notes = None

    if request.method == 'POST':
        selected_workout = request.POST.get('workout_type')
        notes = request.POST.get('notes')
        new_log = WorkoutLog(user=request.user, workout_type=selected_workout, notes=notes)
        new_log.save()
        logged_workout = selected_workout

    # Always fetch logs, even on GET
    all_logs = WorkoutLog.objects.order_by('-created_at')

    return render(request, 'workoutlogs/workout_logs.html', {
        'logged_workout': logged_workout,
        'notes': notes,
        'all_logs': all_logs
    })



