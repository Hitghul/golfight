from django.urls import path
from django.views.static import serve

urlpatterns = [
    path("", serve, {"path": "index.html", "document_root": "web"}),
    path("<path:path>", serve, {"document_root": "web"}),
]
