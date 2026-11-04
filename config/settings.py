# Configuration minimale de Django pour Golfight
SECRET_KEY = "golfight"
DEBUG = False
ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
