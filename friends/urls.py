from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.add, name='friends.add'),
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', remove_friend, name='remove_friend'),
]