import json

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import JWTManager


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
            success, refresh_token, errors = JWTManager('refresh').generate_token(user.id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'refresh_token': refresh_token}, status=201)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)

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
        if username is None or username == '':
            return False, 'Username empty'
        if len(username) < settings.USERNAME_MIN_LENGTH:
            return False, f'Username length {len(username)} < {settings.USERNAME_MIN_LENGTH}'
        if len(username) > settings.USERNAME_MAX_LENGTH:
            return False, f'Username length {len(username)} > {settings.USERNAME_MAX_LENGTH}'
        users = User.objects.filter(username=username)
        if users.exists():
            return False, f'Username {username} already taken'
        return True, None

    @staticmethod
    def is_valid_email(email):
        if email is None or email == '':
            return False, 'Email empty'
        if len(email) > settings.EMAIL_MAX_LENGTH:
            return False, f'Email length {len(email)} > {settings.EMAIL_MAX_LENGTH}'
        if any(char in '!#$%^&*()=' for char in email):
            return False, 'Invalid character in email address'
        if '@' not in email:
            return False, 'Email missing @'
        if '.' not in email:
            return False, 'Email missing "." character'
        if email.count('@') > 1:
            return False, 'Email contains more than one @ character'
        local_part, domain_and_tld = email.rsplit('@', 1)
        if len(local_part) < settings.EMAIL_LOCAL_PART_MIN_LENGTH:
            return False, f'Local part length {len(local_part)} < {settings.EMAIL_LOCAL_PART_MIN_LENGTH}'
        if domain_and_tld.count('.') == 0:
            return False, 'Email missing TLD'
        tld = domain_and_tld.rsplit('.')[-1]
        if len(tld) > settings.TLD_MAX_LENGTH:
            return False, f'TLD length {len(tld)} > {settings.TLD_MAX_LENGTH}'
        return True, None

    @staticmethod
    def is_valid_password(password):
        if password is None or password == '':
            return False, 'Password empty'
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            return False, f'Password length {len(password)} < {settings.PASSWORD_MIN_LENGTH}'
        if len(password) > settings.PASSWORD_MAX_LENGTH:
            return False, f'Password length {len(password)} > {settings.PASSWORD_MAX_LENGTH}'
        if not any(char.isupper() for char in password):
            return False, 'Password missing uppercase character'
        if not any(char.islower() for char in password):
            return False, 'Password missing lowercase character'
        if not any(char.isdigit() for char in password):
            return False, 'Password missing digit'
        if not any(char in '!@#$%^&*()-_+=' for char in password):
            return False, 'Password missing special character'
        return True, None


@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            validation_errors = SignInView.signin_infos_validation(json_request)
            if validation_errors:
                return JsonResponse(data={'errors': validation_errors}, status=400)
            user = User.objects.filter(username=json_request['username']).first()
            success, refresh_token, errors = JWTManager('refresh').generate_token(user.id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'refresh_token': refresh_token}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

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


@method_decorator(csrf_exempt, name='dispatch')
class IsUsernameTakenView(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            username = json_request.get('username')
            if username is None:
                return JsonResponse(data={'is_taken': True}, status=400)
            users = User.objects.filter(username=username)
            if users.exists():
                return JsonResponse(data={'is_taken': True}, status=200)
            return JsonResponse(data={'is_taken': False}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshJWT(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            refresh_token = json_request.get('refresh_token')
            if refresh_token is None:
                return JsonResponse(data={'errors': ['Refresh token not found']}, status=400)
            success, errors, user_id = JWTManager('refresh').is_authentic_and_valid_request(refresh_token)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            success, access_token, errors = JWTManager('access').generate_token(user_id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'access_token': access_token}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
