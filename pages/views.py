from django.shortcuts import render, get_object_or_404
from .models import ReservedTable
import datetime

def index(request):
    return render(request, 'pages/index.html')
