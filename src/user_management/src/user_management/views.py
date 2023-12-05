from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def hello(request):
    return JsonResponse({'message': 'Hello from user_management!'})

@csrf_exempt
def login(request):

    print("login api requested")

    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            name = json_data.get('name', '')
            return JsonResponse({'message': f'Welcome! {name}'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    if request.method == "GET":
        return JsonResponse({'message': 'Expected POST method, received GET ...'})
