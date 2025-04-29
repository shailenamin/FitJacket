from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_logs, name='workout_logs'),
]
