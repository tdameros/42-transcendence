import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user_management.JWTManager import (UserAccessJWTManager,
                                        UserRefreshJWTManager)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshJWT(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            refresh_token = json_request.get('refresh_token')
            if refresh_token is None:
                return JsonResponse(data={'errors': ['Refresh token not found']}, status=400)
            success, user_id, errors = UserRefreshJWTManager.authenticate(refresh_token)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            success, access_token, errors = UserAccessJWTManager.generate_jwt(user_id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'access_token': access_token}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
