import json

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import common.src.settings as common
from common.src.internal_requests import InternalRequests
from user.models import User
from user_management import settings
from user_management.JWTManager import UserRefreshJWTManager
from user_management.utils import (is_valid_email, is_valid_password,
                                   is_valid_username)


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            validation_errors = self.signup_infos_validation(json_request)
            if validation_errors:
                return JsonResponse(data={'errors': validation_errors}, status=400)
            user = User.objects.create(username=json_request['username'],
                                       email=json_request['email'],
                                       password=json_request['password'])
            valid, errors = self.post_user_stats(user.id)
            if not valid:
                user.delete()
                return JsonResponse(data={'errors': errors}, status=500)
            success, refresh_token, errors = UserRefreshJWTManager.generate_jwt(user.id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'refresh_token': refresh_token}, status=201)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred: {e}']}, status=500)

    @staticmethod
    def post_user_stats(user_id: int) -> (bool, list):
        try:
            if settings.DEBUG:
                response = InternalRequests.post(f'{common.DEBUG_USER_STATS_USER_ENDPOINT}{user_id}/',
                                                 data=json.dumps({}))
            else:
                response = InternalRequests.post(f'{common.USER_STATS_USER_ENDPOINT}{user_id}/',
                                                 data=json.dumps({}))
        except requests.exceptions.RequestException:
            return False, ['Could not access user-stats']
        if not response.ok:
            print(response.json())
            return False, ['Could not create user in user-stats']
        return True, None

    @staticmethod
    def signup_infos_validation(json_request):
        validation_errors = []

        username = json_request.get('username')
        email = json_request.get('email')
        password = json_request.get('password')

        valid_username, error_message_username = is_valid_username(username)
        valid_email, error_message_email = is_valid_email(email)
        valid_password, error_message_password = is_valid_password(password)

        if not valid_username:
            validation_errors.append(error_message_username)
        if not valid_email:
            validation_errors.append(error_message_email)
        if not valid_password:
            validation_errors.append(error_message_password)
        return validation_errors
