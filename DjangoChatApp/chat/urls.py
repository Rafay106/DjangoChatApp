from django.urls import path

from . views import *

app_name = 'chat'
urlpatterns = [
    path('login/', loginUser, name='loginUser'),
    path('logout/', logoutUser, name='logoutUser'),
    path('register/', registerUser, name='registerUser'),

    path('', homeView, name='homeView'),
    path('room-<int:pk>/', roomView, name='roomView'),

    path('create-room/', createView, name='createView'),
    path('update-room/<int:pk>/', updateView, name='updateView'),
    path('delete-room/<int:pk>/', deleteRoom, name='deleteView'),
    path('delete-message/<int:pk>/', deleteMessage, name='deleteMsg'),

    path('profile-<str:uname>/', userProfileView, name='userProfileView'),
    path('profile/edit', editUserProfile, name='editUserProfile'),
    
    path('topics/', topicsView, name='topicsView'),
    path('recent-activities/', activityView, name='activityView'),
]