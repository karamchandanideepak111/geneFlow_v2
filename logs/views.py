from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import json
import conn_details

dbdetails = conn_details.get_details()

def fetch_logs_data():
    connection = mysql.connector.connect(
        host=dbdetails['host'],
        user=dbdetails['user'],
        password=dbdetails['password'],
        database=dbdetails['database'],
        port=dbdetails['port']
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT log_id,connector_id, instrument_name,version,ip_address,pc_name,timestamp,status,org_filename,updated_filename FROM geneflow.logsDB AS l JOIN geneflow.instrumentDB AS i ON l.instrument_id = i.instrument_id order by log_id desc;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps(rows, indent=4, default=str)

# Create your views here.
def index(request):
    json_data = fetch_logs_data()
    log_data = json.loads(json_data)
    context = {
        'current_page': 'logs',
        'log_data': log_data
    }
    return render(request, 'logs/index.html', context)
