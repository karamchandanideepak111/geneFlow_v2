from django.shortcuts import render
from django.http import JsonResponse
import mysql.connector
import json
import conn_details
from django.views.decorators.csrf import csrf_exempt
from .models import InstrumentData

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

# New view to return instrument data as JSON
def instruments_data(request):
    instruments = json.loads(fetch_instrument_data())
    print(type(instruments))
    return JsonResponse(instruments, safe=False)

dbdetails = conn_details.get_details()

@csrf_exempt
def create_instrument(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body of the request
            data = json.loads(request.body)

            # Call the model method to insert data into the database
            json_data = InstrumentData.create_instrument(data)
            instruments = json.loads(json_data)

            # Return the newly created instruments and success response
            return JsonResponse({
                'message': 'Instrument created successfully',
                'data': instruments
            }, status=201)

        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({
                'message': 'Failed to create instrument',
                'error': str(e)
            }, status=400)

    # If not a POST request, return a method not allowed response
    return JsonResponse({'message': 'Method not allowed'}, status=405)