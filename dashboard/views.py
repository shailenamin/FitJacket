from django.shortcuts import render, redirect
from .models import Goal


def dashboard(request):
    if request.method == 'POST':
        if 'submit_goal' in request.POST:
            text = request.POST.get('user_input_field')
            if text:
                Goal.objects.create(text=text, user=request.user)

        elif 'complete_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            goal.completed = True
            goal.abandoned = False
            goal.save()
            return redirect('Dashboard')

        elif 'abandon_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            goal.abandoned = True
            goal.completed = False
            goal.save()
            return redirect('Dashboard')

    all_goals = Goal.objects.filter(user=request.user).order_by('created_at')
    completed_goals_count = Goal.objects.filter(user=request.user, completed=True).count()
    abandoned_goals_count = Goal.objects.filter(user=request.user, abandoned=True).count()
    remaining_goals_count = Goal.objects.filter(user=request.user, completed=False, abandoned=False).count()

    return render(request, 'dashboard/goals.html', {
        'user_inputs': all_goals,
        'completed_goals_count': completed_goals_count,
        'abandoned_goals_count': abandoned_goals_count,
        'remaining_goals_count': remaining_goals_count,
    })
