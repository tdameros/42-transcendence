import json
import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.utils import is_valid_password


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordSendCodeView(View):
    @staticmethod
    def post(request):
        try:

            try:
                json_request = json.loads(request.body.decode('utf-8'))
            except Exception:
                return JsonResponse(data={'errors': ['Invalid JSON format in the request body : decode error']},
                                    status=400)

            try:
                user_email = json_request['email']
            except KeyError:
                return JsonResponse(data={'errors': ['No email provided']}, status=400)

            if user_email is None:
                return JsonResponse(data={'errors': ['Email can not be empty']}, status=400)

            user = User.objects.filter(email=user_email).first()
            if user is None:
                return JsonResponse(data={'errors': ['Username not found']}, status=400)

            random_code = ''.join(random.choice(string.digits)
                                  for _ in range(settings.FORGOT_PASSWORD_CODE_MAX_LENGTH))

            user.forgotPasswordCode = random_code
            user.forgotPasswordCodeExpiration = datetime.utcnow() + timedelta(
                minutes=settings.FORGOT_PASSWORD_CODE_EXPIRATION_MINUTES)

            user.save()

            subject = "Did you forgot your password?"
            message = (f'Here is your {settings.FORGOT_PASSWORD_CODE_MAX_LENGTH} '
                       f'characters code : ' + str(random_code) + '\n'
                       '\nCopy-paste this code to renew the '
                       'account access!\n\n')

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse(data={'ok': 'Email sent', 'email': anonymize_email(user_email),
                                      'expires': user.forgotPasswordCodeExpiration}, status=200)

        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)


def anonymize_email(email):
    if "@" in email:
        local_part, domain = email.split("@")
        mask = "*" * (len(local_part) - 2) + local_part[-2:]
        email_mask = f"{mask}@{domain}"
        return email_mask
    else:
        return email


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordCheckCodeView(View):
    @staticmethod
    def post(request):
        try:
            try:
                json_request = json.loads(request.body.decode('utf-8'))
            except Exception:
                return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)

            try:
                user_email = json_request['email']
                code_provided = json_request['code']
            except KeyError as e:
                return JsonResponse(data={'errors': [f'Mandatory value missing : {e}']}, status=400)

            if user_email is None:
                return JsonResponse(data={'errors': ['Email empty']}, status=400)

            if code_provided is None or code_provided == '':
                return JsonResponse(data={'errors': ['Code empty']}, status=400)

            user = User.objects.filter(email=user_email).first()
            if user is None:
                return JsonResponse(data={'errors': ['Username not found']}, status=400)

            user_code = user.forgotPasswordCode
            if code_provided != user_code:
                return JsonResponse(data={'errors': ['Invalid code'],
                                          'errors details': f'Code provided : {code_provided}'}, status=400)
            if timezone.now() > user.forgotPasswordCodeExpiration:
                return JsonResponse(
                    data={'errors': ['Code expired'],
                          'errors details': f'Code valid until : {user.forgotPasswordCodeExpiration}'
                                            f', current time is : {timezone.now()}'},
                    status=400)
            return JsonResponse(data={'ok': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordChangePasswordView(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        try:
            user_email = json_request['email']
            code_provided = json_request['code']
            new_password = json_request['new_password']
        except KeyError as e:
            return JsonResponse(data={'errors': [f'Mandatory value missing : {e}']}, status=400)
        if user_email is None:
            return JsonResponse(data={'errors': ['Email empty']}, status=400)
        if code_provided is None or code_provided == '':
            return JsonResponse(data={'errors': ['Code empty']}, status=400)
        valid_password, password_errors = is_valid_password(new_password)
        if not valid_password:
            return JsonResponse(data={'errors': [password_errors]}, status=400)
        user = User.objects.filter(email=user_email).first()
        if user is None:
            return JsonResponse(data={'errors': ['Username not found']}, status=400)
        user_code = user.forgotPasswordCode
        if code_provided != user_code:
            return JsonResponse(data={'errors': ['Invalid code'],
                                      'errors details': f'Code provided : {code_provided}'}, status=400)
        if timezone.now() > user.forgotPasswordCodeExpiration:
            return JsonResponse(data={'errors': ['Code expired'],
                                      'errors details': f'Code valid until : {user.forgotPasswordCodeExpiration}'
                                                        f', current time is : {timezone.now()}'},
                                status=400)
        user.password = new_password
        user.forgotPasswordCodeExpiration = None
        user.forgotPasswordCode = None
        user.save()
        return JsonResponse(data={'ok': 'ok'}, status=200)
