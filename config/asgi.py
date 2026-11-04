import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from game.consumers import GameConsumer, VersusConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws", GameConsumer.as_asgi()),
        path("ws/versus", VersusConsumer.as_asgi()),
    ]),
})
