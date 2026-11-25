from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("game.urls")),
    path("lobby/", include("lobby.urls")),
]

if settings.SERVE_STATIC:
    urlpatterns.append(path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}))