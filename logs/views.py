from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Logs

# Create your views here.
def index(request):
    # Fetch logs data through the Logs model
    json_data = Logs.objects.fetch_logs_data()
    log_data = json.loads(json_data)
    
    # Prepare context for the template
    context = {
        'current_page': 'logs',
        'log_data': log_data
    }
    
    # Render the logs/index.html template with the context
    return render(request, 'logs/index.html', context)
