from django.http import JsonResponse
from user.models import User
from django.views import View
from django.conf import settings
from datetime import datetime, timedelta
from user_management.decode_jwt import authenticate_request
import jwt
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserInvalidFormat(Exception):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    @csrf_exempt
    def post(self, request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            if not self.is_valid_user(json_request):
                raise UserInvalidFormat()
            User.objects.create(
                username=json_request['username']
            )
            return JsonResponse(data={'username': f'{json_request['username']}'}, status=200)
        except (json.JSONDecodeError, UserInvalidFormat):
            return JsonResponse(data={}, status=400)

    @staticmethod
    def is_valid_user(json_request):
        username = json_request.get('username')
        if not SignUpView.is_valid_username(username):
            return False
        return True

    @staticmethod
    def is_valid_username(username):
        if username is None:
            return False
        if len(username) > 20:
            return False
        return True


class UserView(View):
    @staticmethod
    def get(request, user_id):
        if authenticate_request(request) is None:
            return JsonResponse(data={}, status=401)
        users = User.objects.filter(id=user_id)
        if not users.exists():
            return JsonResponse(data={}, status=404)
        user = users.first()
        data = {
            'username': user.username,
            'elo': user.elo,
        }
        return JsonResponse(data, status=200)


class EncodeJwtView(View):
    @staticmethod
    def get(request, user_id):
        users = User.objects.filter(id=user_id)
        if not users.exists():
            return JsonResponse(data={}, status=404)

        payload = {
            'user_id': user_id,
            'exp': datetime.now() + timedelta(days=1),
            'iat': datetime.now()
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({"jwt": f"{jwt_token}"})
