from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.emailUsers, name='administratorPanel.emailUsers'),
]