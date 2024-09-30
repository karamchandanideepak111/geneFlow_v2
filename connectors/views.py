from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import boto3
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ConnectorData
from datetime import datetime

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

@csrf_exempt
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

# Initialize the S3 client with your credentials and region from settings
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAXJDVAFSV3NCPPGGV',
    aws_secret_access_key='X953zBPgwki97tz+sAMOvGn0W2tmxK/SctlKmYY+',
    region_name='us-east-2'
)

# Name of the S3 bucket
S3_BUCKET_NAME = 'geneflow001'

@csrf_exempt
def upload_file(request):
    if len(request.body) != 0:
        data_str = request.body.decode('utf-8')
        data_json = json.loads(data_str)
        try:
            print("Form data received:")
            for key, value in data_json['body'].items():
                print(f"{key}: {value}")

            # Extract data from the request body
            conn_id = data_json['body']['connector_id']
            key = data_json['body']['key']
            instru_id = data_json['body']['instrument_id']
            ip = data_json['body']['ip']
            timestamp_str = data_json['body']['timestamp']
            hostname = data_json['body']['pc_name']

            # Convert timestamp to MySQL-friendly format
            timestamp_obj = datetime.strptime(timestamp_str, '%d/%m/%y %H:%M:%S')
            mysql_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
            print("All data extracted successfully")

            # Fetch data from the database
            matched_row = ConnectorData.fetch_connector_and_instrument_data(conn_id, key)

            if matched_row.empty:
                return JsonResponse({'error': 'Invalid connector ID or key'}, status=400)

            # Extract necessary details
            location = matched_row['folder_location'].values[0]
            instru_name = matched_row['instrument_name'].values[0]
            instru_ver = matched_row['version'].values[0]

            # Extract file content and decode from base64
            file_content_base64 = data_json['body']['file']
            file_content = base64.b64decode(file_content_base64)
            org_filename = data_json['body']['filename']

            # Generate new file name
            new_file_name = f"{conn_id}_{mysql_timestamp.replace(' ', '-')}_{instru_name}-{instru_ver}.{org_filename.split('.')[-1]}"
            new_file_name = new_file_name.replace(':', '-')
            print(f"New file name: {new_file_name}")

            # Define a custom path for local storage
            custom_path = os.path.join('Upload_files', new_file_name)

            # Save the file locally first
            default_storage.save(custom_path, ContentFile(file_content))

            # Upload the file to the S3 bucket
            try:
                s3_key = f"{location}/input/{new_file_name}"
                
                # Upload the file to S3
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=s3_key,
                    Body=file_content
                )

                # File URL in S3
                s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
                print(f"File uploaded successfully to S3: {s3_url}")

                # Delete the local file after successful upload to S3
                os.remove(custom_path)
                print(f"File {custom_path} deleted successfully from local storage.")

            except Exception as e:
                os.remove(custom_path)
                print(f"File {custom_path} deleted successfully from local storage.")
                print(f"Failed to upload file to S3: {e}")
                return JsonResponse({'error': f"Failed to upload file to S3: {str(e)}"}, status=500)

            print("Inserting log into the database")
            ConnectorData.insert_log(conn_id, instru_id, ip, hostname, mysql_timestamp, 'Uploaded', org_filename, new_file_name)
            print("Log inserted successfully")

            return JsonResponse({'message': 'File uploaded successfully', 'file_url': s3_url}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'Empty'}, status=201)
