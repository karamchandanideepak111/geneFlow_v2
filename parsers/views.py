from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def parse_file(request):
    print("Parsing file")
    print(request.body)
    return JsonResponse({'success': True})