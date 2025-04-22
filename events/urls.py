from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.about, name='events.about'),
    path('events/create/', views.create_group, name='events.create'),

]