from django.urls import path
from . consumers import *

ws_urlpatterns = [
    path('ws/ac/', MyWSC.as_asgi())
]