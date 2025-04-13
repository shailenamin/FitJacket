from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('goal-history/', views.goal_history, name='GoalHistory'),
]