from django.urls import path
from . import views

app_name = 'ai_coach'
urlpatterns = [
    path('', views.coach_home, name='home'),
    path('ask/', views.ask_coach, name='ask'),
    path('history/', views.coaching_history, name='history'),
]
