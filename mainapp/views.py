from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    context = {
        'current_page': 'dashboard'
    }
    return render(request, 'index.html')