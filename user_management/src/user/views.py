from django.http import JsonResponse
from user.models import User
from django.views import View
from django.conf import settings
from datetime import datetime, timedelta
from user_management.JWTManager import user_exist, JWTManager
import jwt
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            validation_errors = self.signup_infos_validation(json_request)
            if not validation_errors:
                User.objects.create(username=json_request['username'],
                                    email=json_request['email'],
                                    password=json_request['password'])
                user = User.objects.filter(username=json_request['username']).first()
                refresh_token = JWTManager('refresh').generate_token(user.id)
                return JsonResponse(data={'refresh_token': refresh_token}, status=201)
            else:
                return JsonResponse(data={'errors': validation_errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        except Exception as e:
            return JsonResponse(data={'errors': ['An unexpected error occurred']}, status=500)

    def signup_infos_validation(self, json_request):
        validation_errors = []

        username = json_request.get('username')
        email = json_request.get('email')
        password = json_request.get('password')
        valid_username, error_message_username = self.is_valid_username(username)
        valid_email, error_message_email = self.is_valid_email(email)
        valid_password, error_message_password = self.is_valid_password(password)

        if not valid_username:
            validation_errors.append(error_message_username)
        if not valid_email:
            validation_errors.append(error_message_email)
        if not valid_password:
            validation_errors.append(error_message_password)

        return validation_errors

    @staticmethod
    def is_valid_username(username):
        if username is None:
            return False, "Username empty"
        if len(username) > 20:
            return False, f"Username length {len(username)} > 20"
        users = User.objects.filter(username=username)
        if users.exists():
            return False, "Username already taken"
        return True, None

    @staticmethod
    def is_valid_email(email):
        if email is None:
            return False, "Email empty"
        if len(email) > 50:
            return False, f"Email length {len(email)} > 50"
        if '@' not in email:
            return False, "Email missing @"
        if '.' not in email:
            return False, "Email missing \".\" character"
        if email.count('@') > 1:
            return False, "Email contains more than one @ character"
        return True, None

    @staticmethod
    def is_valid_password(password):
        if password is None:
            return False, "Password empty"
        if len(password) < 8:
            return False, f"Password length {len(password)} < 8"
        if not any(char.isupper() for char in password):
            return False, "Password missing uppercase character"
        if not any(char.isdigit() for char in password):
            return False, "Password missing digit"
        if not any(char in "!@#$%^&*()-_+=" for char in password):
            return False, "Password missing special character"
        return True, None

@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            validation_errors = SignInView.signin_infos_validation(json_request)
            if not validation_errors:
                user = User.objects.filter(username=json_request['username']).first()
                refresh_token = JWTManager('refresh').generate_token(user.id)
                return JsonResponse(data={'refresh_token': refresh_token}, status=200)
            else:
                return JsonResponse(data={'errors': validation_errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

        except Exception as e:
            return JsonResponse(data={'errors': ['An unexpected error occurred']}, status=500)

    @staticmethod
    def signin_infos_validation(json_request):
        validation_errors = []

        username = json_request.get('username')
        password = json_request.get('password')
        if username is None:
            validation_errors.append("Username empty")
        if password is None:
            validation_errors.append("Password empty")

        user = User.objects.filter(username=username).first()
        if user is None:
            validation_errors.append("Username not found")
        elif user is not None and password != user.password:
            validation_errors.append("Invalid password")

        return validation_errors


class IsUsernameTakenView(View):
    @staticmethod
    def get(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            username = json_request.get('username')
            if username is None:
                return JsonResponse(data={'is_taken': True}, status=400)
            users = User.objects.filter(username=username)
            if users.exists():
                return JsonResponse(data={'is_taken': True}, status=200)
            else:
                return JsonResponse(data={'is_taken': False}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': ['An unexpected error occurred']}, status=500)
