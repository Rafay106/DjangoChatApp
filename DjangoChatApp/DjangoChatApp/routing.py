from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django .urls import path
import chat.routing

application = ProtocolTypeRouter({
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(chat.routing.ws_urlpatterns)
        )
    )
})