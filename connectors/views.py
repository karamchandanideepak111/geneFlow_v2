from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json
import conn_details
import uuid
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import base64
import boto3
import os

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

s3_client = boto3.client('s3')
bucket_name = 'geneflow001'

@require_POST
@csrf_exempt
def upload_file(request):
    try:
        decoded_body = base64.b64decode(request.body).decode('utf-8')
        form_data = json.loads(decoded_body)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    try:
        conn_id = form_data['body']['connector_id']
        key = form_data['body']['key']
        instru_id = form_data['body']['instrument_id']
        ip = form_data['body']['ip']
        timestamp = form_data['body']['timestamp']
        hostname = form_data['body']['pc_name']

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
            WHERE c.connector_id = %s AND c.key = %s
        """
        cursor.execute(conn_query, (conn_id, key))
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        if not result:
            return JsonResponse({'error': 'Invalid connector ID or key'}, status=400)

        matched_row = pd.DataFrame(result)
        location = matched_row['folder_location'].values[0]
        instru_name = matched_row['instrument_name'].values[0]
        instru_ver = matched_row['version'].values[0]
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    try:
        file_content = base64.b64decode(form_data['body']['file'])
        org_filename = form_data['body']['filename']
        temp_file_path = f"/tmp/{org_filename}"

        with open(temp_file_path, 'wb') as f:
            f.write(file_content)
        f.close()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    try:
        new_file_name = f"{conn_id}_{timestamp.replace(':', '-').replace(' ', '-')}_{instru_name}-{instru_ver}.{org_filename.split('.')[-1]}"
        with open(temp_file_path, 'rb') as f:
            s3_client.put_object(Bucket=bucket_name, Key=f"{location}/input/{new_file_name}", Body=f)
        os.remove(temp_file_path)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    try:
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )

        cursor = connection.cursor()

        # Insert log into the database
        insert_log_query = """
        INSERT INTO geneflow.logs (connector_id, instrument_name, instrument_version, ip_address, timestamp, org_filename, updated_filename, pc_name, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_log_query, (
            conn_id,
            instru_name,
            instru_ver,
            ip,
            timestamp,
            org_filename,
            new_file_name,
            hostname,
            "Uploaded"
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return JsonResponse({'message': 'File successfully uploaded to S3!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)