from django.http import JsonResponse


def index(request):
    return JsonResponse({'message': 'Hello, world!'}, status=200)
