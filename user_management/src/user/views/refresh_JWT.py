import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import (UserAccessJWTManager,
                                        UserRefreshJWTManager)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshJWT(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        try:
            refresh_token = json_request.get('refresh_token')
            if refresh_token is None:
                return JsonResponse(data={'errors': ['Refresh token not found']}, status=400)
            success, user_id, errors = UserRefreshJWTManager.authenticate(refresh_token)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            if user_id is None:
                return JsonResponse(data={'errors': ['User not found']}, status=404)
            user = User.objects.get(id=user_id)
            if user.account_deleted:
                return JsonResponse(data={'errors': ['User deleted']}, status=404)
            success, access_token, errors = UserAccessJWTManager.generate_jwt(user_id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            try:
                user.update_latest_activity()
                user.save()
            except Exception as e:
                return JsonResponse(
                    data={'errors': [f'An error occurred while updating the last login date : {e}']}, status=500)
            return JsonResponse(data={'access_token': access_token}, status=200)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
