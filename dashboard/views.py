from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal, Profile, Progress, WorkoutPlan, WorkoutDay, Exercise
from django.contrib import messages
from django.utils import timezone
from openai import OpenAI
from dotenv import load_dotenv
import os
from .forms import WorkoutPlanGeneratorForm
import json
from django.conf import settings

load_dotenv()


@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if (Goal.expired_goals(request.user) > 0):
        profile.current_streak = 0
        profile.save()
        return redirect('Dashboard')

    if request.method == 'POST':
        if 'submit_goal' in request.POST:
            text = request.POST.get('user_input_field')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if end_date <= start_date:
                messages.error(request, "End date cannot be before or on the start date.")

            elif text and len(text) <= 100:
                exercise_type, duration_minutes, calories_per_minute = text_formatting(text)

                if duration_minutes < 0.01:
                    messages.error(request, "Exercise duration has to be greater than 1 second.")
                    return redirect('Dashboard')

                goal_text = f"{exercise_type} - {duration_minutes} minutes"
                start_date = timezone.make_aware(timezone.datetime.strptime(start_date, "%Y-%m-%d"))
                end_date = timezone.make_aware(timezone.datetime.strptime(end_date, "%Y-%m-%d"))

                create_goal(request.user, goal_text, start_date, end_date, duration_minutes, calories_per_minute)
            else:
                messages.error(request, "Goal must be 100 characters or less")

        elif 'abandon_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            goal.abandoned = True
            goal.completed = False
            goal.save()
            messages.success(request, "Goal abandoned!")
            profile.current_streak = 0
            profile.save()
            return redirect('Dashboard')
        elif 'favorite_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            goal.favorite = True
            goal.save()
            messages.success(request, "Goal favorited!")
            return redirect('favorite/')

    current_goals = Goal.objects.filter(user=request.user, completed=False, abandoned=False)
    completed_goals_count = Goal.objects.filter(user=request.user, completed=True).count()
    abandoned_goals_count = Goal.objects.filter(user=request.user, abandoned=True).count()
    remaining_goals_count = Goal.objects.filter(user=request.user, completed=False, abandoned=False).count()
    return render(request, 'dashboard/goals.html', {
        'user_inputs': current_goals,
        'completed_goals_count': completed_goals_count,
        'abandoned_goals_count': abandoned_goals_count,
        'remaining_goals_count': remaining_goals_count,
        'streak': profile.current_streak
    })


@login_required
def goal_history(request):
    completed_goals = Goal.objects.filter(user=request.user, completed=True)
    abandoned_goals = Goal.objects.filter(user=request.user, abandoned=True)

    return render(request, 'dashboard/goal-history.html', {
        'completed_goals': completed_goals,
        'abandoned_goals': abandoned_goals,
    })


@login_required
def mark_favorite(request):
    if request.method == 'POST':

        if 'unfavorite_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            goal.favorite = False
            goal.save()
            messages.success(request, "Goal Unfavorited!")
            return redirect('FavoriteHistory')

        elif 'add_goal' in request.POST:
            goal_id = request.POST.get('goal_id')
            goal = Goal.objects.get(id=goal_id)
            time_diff = goal.end_date - goal.start_date
            duration = extract_number(goal.text)

            create_goal(request.user, goal.text, timezone.now(), timezone.now() + time_diff,
                        duration, goal.calories_burnt_per_second * 60)

            messages.success(request, "Goal added to Dashbord!")
            return redirect('Dashboard')

    favorite_goals = Goal.objects.filter(user=request.user, favorite=True)
    return render(request, 'dashboard/favorite.html', {
        'favorite_goals': favorite_goals
    })


@login_required
def progress_view(request):
    user_progress = Progress.objects.filter(user=request.user)
    completed = Goal.objects.filter(user=request.user, completed=True).count()
    remaining = Goal.objects.filter(user=request.user, completed=False, abandoned=False)
    remaining_count = remaining.count()
    abandoned = Goal.objects.filter(user=request.user, abandoned=True).count()

    total_progression = 100
    if (remaining_count != 0):
        total_progression = 0
        for goal in remaining:
            total_progression += goal.progress
        total_progression /= remaining_count
        total_progression = round(total_progression, 2)

    return render(request, 'dashboard/progress.html', {
        'remaining_goals': remaining,
        'progress_data': user_progress,
        'completed_goals_count': completed,
        'remaining_goals_count': remaining_count,
        'abandoned_goals_count': abandoned,
        'total_progression_percentage': total_progression
    })


@login_required
def start_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)

    return render(request, 'dashboard/start_goal.html', {
        'goal': goal,
    })


@login_required
def complete_goal(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        goal_id = request.POST.get('goal_id')
        calories_burned = float(request.POST.get('calories_burned'))
        total_seconds_elapsed = int(request.POST.get('time_elapsed', 0))

        goal = Goal.objects.get(id=goal_id)
        goal.progress = (total_seconds_elapsed / goal.total_duration_seconds) * 100

        Progress.objects.create(
            user=request.user,
            goal_name=goal.text,
            progress_value=goal.progress,
        )

        profile.total_calories_burnt += calories_burned
        if (goal.progress >= 100):
            goal.completed = True
            profile.current_streak += 1
        else:
            goal.total_duration_seconds -= total_seconds_elapsed

        profile.save()
        goal.save()

        return redirect('progress')


def text_formatting(text):
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = (
            "You will extract exercise type, duration in minutes, and estimate calories burned per minute. The exercise type should be one that Strava uses. "
            "Return in JSON format like this: "
            "{\"exercise\": \"Jump Rope\", \"duration_minutes\": 20, \"calories_per_minute\": 12}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
        )

        response_text = response.choices[0].message.content.strip()

        parsed = json.loads(response_text)

        exercise_type = parsed.get("exercise", "Unknown Exercise")
        duration_minutes = parsed.get("duration_minutes", 0)
        calories_per_minute = parsed.get("calories_per_minute", 0)

        return exercise_type, duration_minutes, calories_per_minute

    except Exception as e:
        print(f"Error with AI request: {e}")
        return "Break", 0, 0


def create_goal(user, goal_text, start_date, end_date, duration_minutes, calories_per_minute=1):

    goal = Goal.objects.create(
        text=goal_text,
        user=user,
        start_date=start_date,
        end_date=end_date,
        total_duration_seconds=duration_minutes * 60,
        calories_burnt_per_second=calories_per_minute / 60
    )
    return goal


def extract_number(text):
    number = ''
    decimal_found = False

    for char in text:
        if char.isdigit():
            number += char
        elif char == '.' and not decimal_found:
            number += char
            decimal_found = True

    return float(number) if number else None


@login_required
def generate_workout_plan(request):
    if request.method == 'POST':
        form = WorkoutPlanGeneratorForm(request.user, request.POST)
        if form.is_valid():
            goals = form.cleaned_data['fitness_goals']
            experience = form.cleaned_data['experience_level']
            frequency = form.cleaned_data['workout_frequency']
            duration = form.cleaned_data['plan_duration']
            equipment = form.cleaned_data['equipment_access']
            notes = form.cleaned_data['additional_notes']

            goal_descriptions = [goal.text for goal in goals]

            workout_plan_data = generate_ai_workout_plan(
                goal_descriptions,
                experience,
                frequency,
                duration,
                equipment,
                notes
            )

            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                title=workout_plan_data['title'],
                description=workout_plan_data['description'],
                frequency=frequency,
                difficulty=experience,
                duration_weeks=duration
            )

            for day_data in workout_plan_data['workout_days']:
                workout_day = WorkoutDay.objects.create(
                    workout_plan=workout_plan,
                    day_number=day_data['day_number'],
                    focus=day_data['focus'],
                    instructions=day_data['instructions']
                )

                for i, exercise_data in enumerate(day_data['exercises']):
                    Exercise.objects.create(
                        workout_day=workout_day,
                        name=exercise_data['name'],
                        sets=exercise_data['sets'],
                        reps=exercise_data['reps'],
                        notes=exercise_data.get('notes', ''),
                        order=i
                    )

            messages.success(request, "Your personalized workout plan has been created!")
            return redirect('workout_plan_detail', plan_id=workout_plan.id)
    else:
        form = WorkoutPlanGeneratorForm(request.user)

    return render(request, 'dashboard/generate_workout_plan.html', {
        'form': form
    })


def generate_ai_workout_plan(goals, experience, frequency, duration, equipment, notes):
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        system_prompt = """
        You are an expert fitness trainer who creates personalized workout plans.
        Given the user's goals, experience level, and constraints, create a detailed workout plan.

        Your response should be in JSON format with the following structure:
        {
            "title": "Name of the workout plan",
            "description": "Overall description of the plan and its benefits",
            "workout_days": [
                {
                    "day_number": 1,
                    "focus": "Main focus of this workout (e.g., 'Upper Body', 'Legs', 'Cardio', 'Rest Day')",
                    "instructions": "General instructions for this day's workout",
                    "exercises": [
                        {
                            "name": "Exercise name",
                            "sets": number_of_sets,
                            "reps": "repetition range or duration",
                            "notes": "Any special instructions or form cues"
                        }
                    ]
                }
            ]
        }

        Based on the workout frequency, include an appropriate number of workout days in a week.
        Include rest days as appropriate.
        Design the plan to progress over the specified duration.
        For each exercise, provide clear instructions and appropriate sets/reps.
        """

        # Construct the user message with all the parameters
        user_message = f"""
        Create a personalized workout plan with the following parameters:

        Goals: {', '.join(goals)}
        Experience level: {experience}
        Workout frequency: {frequency}
        Duration: {duration} weeks
        Equipment available: {equipment}

        Additional notes: {notes if notes else 'None provided'}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2000,
        )

        workout_plan_json = response.choices[0].message.content.strip()
        # Parse the JSON response
        workout_plan = json.loads(workout_plan_json)

        return workout_plan

    except Exception as e:
        print(f"Error with AI request: {e}")
        return {
            "title": "Basic Fitness Plan",
            "description": "A simple workout plan to help you get started. There was an issue generating your personalized plan.",
            "workout_days": [
                {
                    "day_number": 1,
                    "focus": "Full Body",
                    "instructions": "Perform these exercises with proper form.",
                    "exercises": [
                        {"name": "Push-ups", "sets": 3, "reps": "8-12", "notes": "Keep your core tight"},
                        {"name": "Bodyweight Squats", "sets": 3, "reps": "12-15", "notes": ""},
                        {"name": "Plank", "sets": 3, "reps": "30 seconds", "notes": ""}
                    ]
                }
            ]
        }


@login_required
def workout_plans(request):
    plans = WorkoutPlan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/workout_plans.html', {
        'plans': plans
    })


@login_required
def workout_plan_detail(request, plan_id):
    plan = get_object_or_404(WorkoutPlan, id=plan_id, user=request.user)
    workout_days = plan.workout_days.all().prefetch_related('exercises')

    return render(request, 'dashboard/workout_plan_detail.html', {
        'plan': plan,
        'workout_days': workout_days
    })


@login_required
def delete_workout_plan(request, plan_id):
    plan = get_object_or_404(WorkoutPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Workout plan deleted successfully.")
        return redirect('workout_plans')

    return render(request, 'dashboard/delete_workout_plan.html', {
        'plan': plan
    })
