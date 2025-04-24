from django.urls import path
from . import views

app_name = 'ai_coach'

urlpatterns = [
    path('', views.coach_home, name='home'),
    path('history/', views.coaching_history, name='history'),
    path('favorite/<int:session_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('helpful/<int:session_id>/', views.toggle_helpful, name='toggle_helpful'),
]
