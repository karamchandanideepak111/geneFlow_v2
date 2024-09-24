from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import json
import conn_details

dbdetails = conn_details.get_details()

def fetch_instrument_data():
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host=dbdetails['host'],
        user=dbdetails['user'],
        password=dbdetails['password'],
        database=dbdetails['database'],
        port=dbdetails['port']
    )

    cursor = connection.cursor(dictionary=True)

    # Execute the query to fetch data from the instrumentDB table
    cursor.execute("SELECT * FROM instrumentDB")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the rows to JSON format
    return json.dumps(rows, indent=4)

# Create your views here.
def index(request):
    json_data = fetch_instrument_data()
    instruments = json.loads(json_data)
    context = {
        'current_page': 'instruments',
        'instruments': instruments
    }
    return render(request, 'instruments/index.html', context)