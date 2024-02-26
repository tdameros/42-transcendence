import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management import settings
from user_management.utils import (is_valid_email, is_valid_password,
                                   is_valid_username, post_user_stats)


def generate_verif_link(user):
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(str(user.id).encode())
    verification_url = reverse('verify_email', kwargs={'user_id': user_id, 'token': token})

    return f'{settings.BASE_URL}{verification_url}'

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        try:
            validation_errors = self.signup_infos_validation(json_request)
            if validation_errors:
                return JsonResponse(data={'errors': validation_errors}, status=400)
            user = User.objects.create(username=json_request['username'],
                                       email=json_request['email'],
                                       password=make_password(json_request['password']))
            valid, errors = post_user_stats(user.id)
            if not valid:
                user.delete()
                return JsonResponse(data={'errors': errors}, status=500)
            # verif_link = generate_verif_link(user)


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
