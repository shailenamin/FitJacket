from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('add/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('respond/<int:request_id>/', views.respond_request, name='respond_request'),
]
