from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'current_page': 'instruments'
    }
    return render(request, 'instruments/index.html')