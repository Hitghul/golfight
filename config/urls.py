from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("game.urls")),
    path("<path:path>", serve, {"document_root": "web"}),
]