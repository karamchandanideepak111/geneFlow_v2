from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import boto3
import os
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIAXJDVAFSV3NCPPGGV',
    aws_secret_access_key='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',
    region_name='us-east-2'
)

def decide_parser(vendor,instrument,filename):
    if vendor == 'beckman':
        if instrument == 'vicellxr':
            from . import beckman
            return beckman.Vicellxr(filename)
    if vendor == 'thermo':
        if instrument == 'chemstation':
            from . import agilent
            return agilent.Chemstation(filename)
    if vendor == 'appliedbio':
        if instrument == 'quantstudio':
            from . import appliedbio
            return appliedbio.QuantStudio(filename)
    if vendor == 'brucker':
        if instrument == 'iconnmr':
            from . import brucker
            return brucker.Iconnmr(filename)
    

# Create your views here.
@csrf_exempt
def parse_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_name = data.get('file_name')
        s3_location = data.get('s3_location')

        # Extract bucket name and key from s3_location
        bucket_name, key = s3_location.replace("s3://", "").split("/", 1)
        
        # Define the local folder to download the file into
        local_folder = 'Upload_files'
        os.makedirs(local_folder, exist_ok=True)  # Create the folder if it doesn't exist
        
        # Generate a unique temporary file name
        temp_file_name = os.path.join(local_folder, f"{uuid.uuid4()}_{os.path.basename(file_name)}")
        
        # Download the file
        s3_client.download_file(bucket_name, key, temp_file_name)
        
        # Define the final file path
        final_file_path = os.path.join(local_folder, os.path.basename(file_name))
        
        # Rename the file to the original file name
        os.rename(temp_file_name, final_file_path)
        print(f'File name: {file_name}')
        data = file_name.split('/')
        print(data)
        file_info = data[0].split('_')
        print(f'Folder location: {data[2]}')
        vendor = file_info[0].lower()
        print(f'Vendor: {vendor}')
        instrument = file_info[1].replace('-', '').lower()
        print(f'Instrument: {instrument}')
        # print(f'File Type: {inst_data}')
        # print(f'version: {inst_data}')
        # print(f'S3 Location: {s3_location}')
        # print(f'File Content: {file_content}')
        print(f'Vendor: {vendor} : Instrument: {instrument} : File Path: {final_file_path}')
        ob = decide_parser(vendor,instrument,final_file_path)
        print("File Contents : ", ob.get_data())
        # # Read the file content
        # with open(final_file_path, 'r') as file:
        #     file_content = file.read()
        # ob = decide_parser(vendor,instrument,final_file_path)
        # file_content = data.get_combined_data()

        # Delete the file
        os.remove(final_file_path)
        print(f'File {final_file_path} has been deleted.')

        # Process the data or store it in your database
        return JsonResponse({'status': 'success', 'file_name': file_name, 'location': s3_location})#, 'content': file_content})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
