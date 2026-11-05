import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_asgi_app = get_asgi_application()

from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from game.consumers import GameConsumer, VersusConsumer
from lobby.consumers import LobbyConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack( URLRouter([
        path("ws", GameConsumer.as_asgi()),
        path("ws/versus", VersusConsumer.as_asgi()),
        path("ws/lobby", LobbyConsumer.as_asgi()),
    ])),
})
