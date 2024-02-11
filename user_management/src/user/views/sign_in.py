import json

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
    return JsonResponse(data={'refresh_token': refresh_token}, status=200)


def handle_2fa_code(user, json_request):
    twofa_code = json_request.get('2fa_code')
    if twofa_code is None:
        return JsonResponse(data={'errors': ['2fa_code is required']}, status=401)
    if user.verify_2fa(twofa_code):
        return return_refresh_token(user)
    return JsonResponse(data={'errors': ['Invalid 2fa code']}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        try:
            validation_errors = SignInView.signin_infos_validation(json_request)
            if validation_errors:
                return JsonResponse(data={'errors': validation_errors}, status=401)
            user = User.objects.filter(username=json_request['username']).first()
            if user.has_2fa:
                return handle_2fa_code(user, json_request)
            return return_refresh_token(user)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)

    @staticmethod
    def signin_infos_validation(json_request):
        validation_errors = []

        username = json_request.get('username')
        password = json_request.get('password')
        if username is None:
            validation_errors.append('Username empty')
        if password is None:
            validation_errors.append('Password empty')
        if username is None or password is None:
            return validation_errors
        user = User.objects.filter(username=username).first()
        if user is None:
            validation_errors.append('Username not found')
        elif user is not None and password != user.password:
            validation_errors.append('Invalid password')

        return validation_errors
