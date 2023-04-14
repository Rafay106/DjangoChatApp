from django.urls import path
from . consumers import *

ws_urlpatterns = [
    path('ws/ac/<str:groupName>', MyWSC.as_asgi())
]