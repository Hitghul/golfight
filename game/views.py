from django.contrib.auth.decorators import login_required
from django.views.static import serve


@login_required
def home(request):
    return serve(request, "index.html", document_root="web")