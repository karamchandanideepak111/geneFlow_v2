from django.shortcuts import render
from django.core.paginator import Paginator
import json
from .models import Logs

def index(request):
    # Get the selected connector_id from the GET request
    connector_id = request.GET.get('connector_id')

    # Fetch all logs data through the Logs model
    json_data = Logs.objects.fetch_logs_data()
    log_data = json.loads(json_data)

    # Get distinct connector IDs from the logs
    distinct_connector_ids = sorted(set(log['connector_id'] for log in log_data))

    # Filter logs based on the selected connector_id if it's provided
    if connector_id:
        log_data = [log for log in log_data if log['connector_id'] == connector_id]

    # Paginate the log data, 10 items per page
    paginator = Paginator(log_data, 10)
    page_number = request.GET.get('page')  # Get the current page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the logs for the current page

    # Prepare context for the template
    context = {
        'current_page': 'logs',
        'page_obj': page_obj,  # Pass paginated data to the template
        'distinct_connector_ids': distinct_connector_ids,  # Pass distinct connector IDs to the template
        'connector_id': connector_id  # Pass the current filter value to the template
    }

    # Render the logs/index.html template with the context
    return render(request, 'logs/index.html', context)
