import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class IsEmailTakenView(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            user_email = json_request.get('email')
            if user_email is None:
                return JsonResponse(data={'errors': ['Empty email']}, status=400)
            users = User.objects.filter(email=user_email)
            if users.exists():
                return JsonResponse(data={'is_taken': True}, status=200)
            return JsonResponse(data={'is_taken': False}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
