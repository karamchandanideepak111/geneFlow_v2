from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json
import conn_details
import uuid

dbdetails = conn_details.get_details()

@require_POST
@csrf_exempt
def update_connector(request):
    data = json.loads(request.body)
    connector_key = data.get('connector_key')
    
    try:
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )

        cursor = connection.cursor()

        # Update the connector in the database
        update_query = """
        UPDATE geneflow.connDB 
        SET connector_name = %s, status = %s
        WHERE ckey = %s
        """
        cursor.execute(update_query, (
            data.get('connector_name'),
            data.get('status'),
            connector_key
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return JsonResponse({'success': True})
    except mysql.connector.Error as err:
        return JsonResponse({'success': False, 'error': str(err)}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def fetch_conn_data():
    connection = mysql.connector.connect(
        host=dbdetails['host'],
        user=dbdetails['user'],
        password=dbdetails['password'],
        database=dbdetails['database'],
        port=dbdetails['port']
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM geneflow.connDB as c JOIN geneflow.instrumentDB AS i ON c.instrument_id = i.instrument_id;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps(rows, indent=4, default=str)

def index(request):
    json_data = fetch_conn_data()
    connectors = json.loads(json_data)
    # print(connectors)
    context = {
        'current_page': 'connectors',
        'connectors': connectors
    }
    return render(request, 'connectors/index.html', context)

def register_connector(request):
    # print("Request POST:", request.body)  # Check the data being posted
    data = json.loads(request.body)
    connection = mysql.connector.connect(
        host=dbdetails['host'],
        user=dbdetails['user'],
        password=dbdetails['password'],
        database=dbdetails['database'],
        port=dbdetails['port']
    )

    cursor = connection.cursor()

    # Insert the connector into the database
    insert_query = """
    CALL insert_conn(%s, %s, %s)
    """
    connector_key = str(uuid.uuid4())
    cursor.execute(insert_query, (
        data['connector_name'],
        connector_key,
        data['instrument_id']
    ))

    connection.commit()
    cursor.close()
    connection.close()

    json_data = fetch_conn_data()
    connectors = json.loads(json_data)
    context = {
        'current_page': 'connectors',
        'connectors': connectors
    }
    return render(request, 'connectors/index.html', context)

def delete_connector(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Create a connection to the MySQL database
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )

        cursor = connection.cursor()
        try:
            # Execute the stored procedure for deletion
            delete_query = "delete FROM geneflow.connDB where connector_id = %s;"  # Adjust the stored procedure name as necessary
            cursor.execute(delete_query, (data['connector_id'],))

            # Commit the changes
            connection.commit()
        except mysql.connector.Error as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        json_data = fetch_conn_data()
        connectors = json.loads(json_data)
        context = {
            'current_page': 'connectors',
            'connectors': connectors
        }
        cursor.close()
        connection.close()
        return render(request, 'connectors/index.html', context)