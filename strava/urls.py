from django.urls import path
from . import views

urlpatterns = [
    path('', views.strava_import, name='strava.import'),
    path('login/', views.strava_login, name='strava.login'),
    path('callback/', views.strava_callback, name='strava.callback'),
    path('workouts/', views.show_workouts, name='strava.workouts'),
]