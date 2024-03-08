import json

from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import UserRefreshJWTManager


def return_refresh_token(user):
    success, refresh_token, errors = UserRefreshJWTManager.generate_jwt(user.id)
    if success is False:
        return JsonResponse(data={'errors while creating jwt': errors}, status=500)
    with transaction.atomic():
        try:
            user.update_latest_activity()
        except Exception as e:
            return JsonResponse(data={'errors': [f'An error occurred while updating the last login date : {e}']},
                                status=500)
    return JsonResponse(data={'refresh_token': refresh_token}, status=200)


def handle_2fa_code(user, json_request):
    twofa_code = json_request.get('2fa_code')
    if twofa_code is None:
        return JsonResponse(data={'errors': ['2fa_code is required'], '2fa': True}, status=401)
    if user.verify_2fa(twofa_code):
        return return_refresh_token(user)
    return JsonResponse(data={'errors': ['Invalid 2fa code'], '2fa': True}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        try:
            user, validation_errors = SignInView.signin_infos_validation(json_request)
            if validation_errors:
                return JsonResponse(data={'errors': validation_errors}, status=401)
            if user.has_2fa:
                return handle_2fa_code(user, json_request)
            return return_refresh_token(user)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)

    @staticmethod
    def signin_infos_validation(json_request):
        validation_errors = []

        login = json_request.get('login')
        password = json_request.get('password')
        if login is None:
            validation_errors.append('Login empty')
        if password is None:
            validation_errors.append('Password empty')
        if login is None or password is None:
            return None, validation_errors
        user, error = SignInView.get_user_by_login(login)
        if user is None:
            validation_errors.append(error)
            return None, validation_errors
        elif user.password is None or check_password(password, user.password) is False:
            validation_errors.append('Invalid password')
        if user.emailVerified is False:
            validation_errors.append('User not verified')
        return user, validation_errors

    @staticmethod
    def get_user_by_login(login: str) -> (User, str):
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=login)
            except User.DoesNotExist:
                return None, 'User not found'
        except Exception as error:
            return None, error
        return user, None
