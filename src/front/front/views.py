from django.http import HttpResponse
import requests


def hello(request):
    try:
        request = requests.get("http://user-nginx/api/")
    except:
        return HttpResponse("Failed to ping user microservice")
    if not request.ok:
        return HttpResponse("Failed to ping user microservice")
    return HttpResponse(f"Ping user microservice result: {request.json()}")
