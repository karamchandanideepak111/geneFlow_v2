from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from . import beckman

# Create your views here.
@csrf_exempt
def parse_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_name = data.get('file_name')
        s3_location = data.get('s3_location')
        print(f'File name: {file_name}')
        data=file_name.split('.')
        inst_data = data[0].split('_')
        print(f'Instrument: {inst_data[0]}')
        print(f'File Type: {inst_data[1]}')
        print(f'version: {inst_data[2]}')
        print(f'S3 Location: {s3_location}')

        # Parse the file
        parser = beckman.Vicellxr(file_name)

        # Process the data or store it in your database
        return JsonResponse({'status': 'success', 'file_name': file_name, 'location': s3_location})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)      