import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from server.game import GameConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([path("ws", GameConsumer.as_asgi())]),
})
