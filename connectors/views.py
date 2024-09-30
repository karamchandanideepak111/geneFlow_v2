from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json
import conn_details
import uuid
import pandas as pd
import base64
import boto3
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ConnectorData

def index(request):
    # Fetching the data using the static method from the model
    json_data = ConnectorData.fetch_conn_data()
    connectors = json.loads(json_data)
    
    # Context to pass to the template
    context = {
        'current_page': 'connectors',
        'connectors': connectors
    }

    return render(request, 'connectors/index.html', context)

def register_connector(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        json_data = ConnectorData.register_connector(data)
        connectors = json.loads(json_data)
        context = {
            'current_page': 'connectors',
            'connectors': connectors
        }
        return render(request, 'connectors/index.html', context)

@require_POST
@csrf_exempt
def update_connector(request):
    data = json.loads(request.body)
    try:
        ConnectorData.update_connector(data)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def delete_connector(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            ConnectorData.delete_connector(data['connector_id'])
            return JsonResponse({'message': 'Connector deleted successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def validate(request):
    if request.method == 'POST':
        try:
            event_body = json.loads(request.body)
            key = event_body["ckey"]
            result_df = ConnectorData.validate_connector(key)

            if result_df is not None:
                body = result_df.to_json(orient="records")
            else:
                body = json.dumps({'exists': 'False'})

            return JsonResponse({'statusCode': 200, 'body': body})
        except Exception as e:
            return JsonResponse({'statusCode': 500, 'error': str(e)})
    return JsonResponse({'statusCode': 400, 'error': 'Invalid request method.'})

@csrf_exempt
def upload_file(request):
    dbdetails = conn_details.get_details()
    print(len(request.body))
    if len(request.body) != 0:
        data_str = request.body.decode('utf-8')
        data_json = json.loads(data_str)
        try:
            print("Form data received:")
            for key, value in data_json['body'].items():
                print(f"{key}: {value}")
            
            # Extract file content and decode from base64
            file_content_base64 = data_json['body']['file']
            file_content = base64.b64decode(file_content_base64)
            
            # Get the filename
            filename = data_json['body']['filename']
            
            # Define a custom path
            custom_path = os.path.join('custom_uploads', filename)
            
            # Save the file
            file_name = default_storage.save(custom_path, ContentFile(file_content))
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        try:
            print("Form data received:")
            conn_id = data_json['body']['connector_id']
            key = data_json['body']['key']
            instru_id = data_json['body']['instrument_id']
            ip = data_json['body']['ip']
            timestamp = data_json['body']['timestamp']
            hostname = data_json['body']['pc_name']
            print("All data extracted successfully")

            connection = mysql.connector.connect(
                host=dbdetails['host'],
                user=dbdetails['user'],
                password=dbdetails['password'],
                database=dbdetails['database'],
                port=dbdetails['port']
            )
            print("Connection established successfully")
            cursor = connection.cursor(dictionary=True)

            print("Querying the database")

            # Query to fetch data from connDB and instrumentDB
            conn_query = """
                SELECT * FROM geneflow.connDB as c 
                JOIN geneflow.instrumentDB as i 
                ON c.instrument_id = i.instrument_id 
                WHERE c.connector_id = %s AND c.ckey = %s
            """

            print("Executing the query")

            cursor.execute(conn_query, (conn_id, key))
            print("Query executed successfully")
            result = cursor.fetchall()

            

            print(result)

            if not result:
                return JsonResponse({'error': 'Invalid connector ID or key'}, status=400)

            matched_row = pd.DataFrame(result)
            location = matched_row['folder_location'].values[0]
            instru_name = matched_row['instrument_name'].values[0]
            instru_ver = matched_row['version'].values[0]

            insert_query = """
                call insert_logs (connector_id, instrument_id, ip, pc_name, timestamp, status, file_name, location, instrument_name, version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (conn_id, key, instru_id, ip, timestamp, hostname, file_name, location, instru_name, instru_ver))
            connection.commit()

            cursor.close()
            connection.close()
            
            return JsonResponse({'message': 'File uploaded successfully', 'file_name': file_name}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'Empty'}, status=201)


'''



    # views.py
from django.shortcuts import render
from .models import fetch_conn_data

def index(request):
    json_data = fetch_conn_data()
    connectors = json.loads(json_data)
    
    context = {
        'current_page': 'connectors',
        'connectors': connectors
    }
    return render(request, 'connectors/index.html', context)


'''