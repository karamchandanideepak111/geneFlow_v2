from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import json

def fetch_logs_data():
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host='connectordb.ckdztmjxvi1u.us-east-2.rds.amazonaws.com',
        user='admin',
        password='passconn09',
        database='geneflow'
    )

    cursor = connection.cursor(dictionary=True)

    # Execute the query to fetch data from the instrumentDB table
    cursor.execute("SELECT * FROM logs")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the rows to JSON format
    return json.dumps(rows, indent=4, default=str)

# Create your views here.
def index(request):
    json_data = fetch_logs_data()
    log_data = json.loads(json_data)
    context = {
        'current_page': 'logs',
        'log_data': log_data
    }
    print(log_data)
    return render(request, 'logs/index.html', context)
