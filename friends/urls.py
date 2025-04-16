from django.urls import path
from . import views

app_name = "friends"
urlpatterns = [
    path('', views.users, name='userList'),
    path('add/<int:user_id>/', views.sendRequest, name='sendRequest'),
    path('respond/<int:request_id>/', views.respondRequest, name='respondRequest'),
    path('remove/<int:user_id>/', views.removeFriend, name="removeFriend"),
    path('groups/create/', views.create_group, name='createGroup'),
    path('groups/<int:group_id>/invite/<int:user_id>/', views.invite_to_group, name='inviteToGroup'),
    path('groups/respond_invite/<int:invite_id>/', views.respond_group_invite, name='respondGroupInvite'),
    path('groups/<int:group_id>/leave', views.leave_group, name='leaveGroup'),
]