# Configuration minimale de Django pour Golfight
SECRET_KEY = "golfight"
DEBUG = False
ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "server.urls"
ASGI_APPLICATION = "server.asgi.application"
