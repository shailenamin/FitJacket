from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='events.about'),
    path('create/', views.create_group, name='events.create'),
]