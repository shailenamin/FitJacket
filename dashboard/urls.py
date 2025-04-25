from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('goal-history/', views.goal_history, name='GoalHistory'),
    path('favorite/', views.mark_favorite, name='FavoriteHistory'),
    path('progress/', views.progress_view, name='progress'),
    path('start_goal/<int:goal_id>/', views.start_goal, name='start_goal'),
    path('complete_goal/', views.complete_goal, name='complete_goal'),
    path('workout-plans/', views.workout_plans, name='workout_plans'),
    path('workout-plans/generate/', views.generate_workout_plan, name='generate_workout_plan'),
    path('workout-plans/<int:plan_id>/', views.workout_plan_detail, name='workout_plan_detail'),
    path('workout-plans/<int:plan_id>/delete/', views.delete_workout_plan, name='delete_workout_plan'),
]
