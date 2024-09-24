from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
import mysql.connector
import json
import conn_details

dbdetails = conn_details.get_details()

def fetch_conn_data():
    connection = mysql.connector.connect(
        host=dbdetails['host'],
        user=dbdetails['user'],
        password=dbdetails['password'],
        database=dbdetails['database'],
        port=dbdetails['port']
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT connector_id,connector_name,ckey,instrument_name,version,status FROM geneflow.connDB as c JOIN geneflow.instrumentDB AS i ON c.instrument_id = i.instrument_id;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps(rows, indent=4, default=str)

# Create your views here.
def index(request):
    json_data = fetch_conn_data()
    connectors = json.loads(json_data)
    print(connectors)
    context = {
        'current_page': 'connectors',
        'connectors': connectors
    }
    return render(request, 'connectors/index.html', context)