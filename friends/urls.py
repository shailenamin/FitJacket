from django.urls import path
from . import views

app_name = "friends"
urlpatterns = [
    path('', views.users, name='userList'),
    path('add/<int:user_id>/', views.sendRequest, name='sendRequest'),
    path('respond/<int:request_id>/', views.respondRequest, name='respondRequest'),
    path('remove/<int:user_id>/', views.removeFriend, name="removeFriend"),
]
