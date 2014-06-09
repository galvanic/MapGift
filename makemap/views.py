from django.shortcuts import render

import mapgift
from makemap.models import Map, KMLfile

# Create your views here.

def index(request):
    context = {"providers": mapgift.PROVIDERS,}
    return render(request, 'makemap/index.html', context)
