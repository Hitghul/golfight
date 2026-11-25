from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def home(request):
    return render(request, "index.html")

def health(request):
    return HttpResponse("ok")