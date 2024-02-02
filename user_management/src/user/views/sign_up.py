import json

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import UserRefreshJWTManager


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
            success, refresh_token, errors = UserRefreshJWTManager.generate_jwt(user.id)
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
        if not username.isalnum():
            return False, 'Username must be alphanumeric'
        users = User.objects.filter(username=username)
        if users.exists():
            return False, f'Username {username} already taken'
        return True, None

    @staticmethod
    def is_valid_email(email):
        if email is None or email == '':
            return False, 'Email empty'
        users = User.objects.filter(email=email)
        if users.exists():
            return False, f'Email {email} already taken'
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
