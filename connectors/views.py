from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json
import conn_details
import uuid
import pandas as pd

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
            # Execute the delete query
            delete_query = "DELETE FROM geneflow.connDB WHERE connector_id = %s;"
            cursor.execute(delete_query, (data['connector_id'],))

            # Commit the changes
            connection.commit()
        except mysql.connector.Error as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            cursor.close()
            connection.close()

        # Return a success response
        return JsonResponse({'message': 'Connector deleted successfully!'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def validate(request):
    print("Request POST:", request.body)
    if request.method == 'POST':
        try:
            event_body = json.loads(request.body)
            key = event_body["key"]

            connection = mysql.connector.connect(
                host=dbdetails['host'],
                user=dbdetails['user'],
                password=dbdetails['password'],
                database=dbdetails['database'],
                port=dbdetails['port']
            )

            cursor = connection.cursor(dictionary=True)

            # Query to fetch data from connDB and instrumentDB
            conn_query = """
                SELECT * FROM geneflow.connDB as c 
                JOIN geneflow.instrumentDB as i 
                ON c.instrument_id = i.instrument_id 
                WHERE c.ckey = %s
            """
            cursor.execute(conn_query, (key,))
            result = cursor.fetchall()

            cursor.close()
            connection.close()

            # Convert the result to a DataFrame
            if result:
                matched_row = pd.DataFrame(result)
                body = matched_row.to_json(orient="records")
            else:
                body = json.dumps({'exists': 'False'})

            return JsonResponse({'statusCode': 200, 'body': body})
        
        except Exception as e:
            print(e)
            return JsonResponse({'statusCode': 500, 'error': str(e)})
    return JsonResponse({'statusCode': 400, 'error': 'Invalid request method.'})

