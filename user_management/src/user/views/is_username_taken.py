import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class IsUsernameTakenView(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        try:
            username = json_request.get('username')
            if username is None:
                return JsonResponse(data={'is_taken': True}, status=400)
            users = User.objects.filter(username=username)
            if users.exists():
                return JsonResponse(data={'is_taken': True}, status=200)
            return JsonResponse(data={'is_taken': False}, status=200)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
