import json

import pyotp
import qrcode
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User
from user_management.JWTManager import get_user_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class Enable2fa(View):
    def post(self, request):
        user_id = get_user_id(request)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(data={'errors': ['user not found']}, status=400)
        if user.has_2fa:
            return JsonResponse(data={'errors': ['2fa already enabled']}, status=400)
        user.totp_secret = pyotp.random_base32()
        user.totp_config_url = f'otpauth://totp/{user.username}?secret={user.totp_secret}&issuer=Pong'
        user.save()
        qr = qrcode.make(user.totp_config_url)
        response = HttpResponse(content_type="image/png")
        qr.save(response, "PNG")
        return response


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class Disable2fa(View):
    def post(self, request):
        user_id = get_user_id(request)
        user = User.objects.get(id=user_id)
        if not user.has_2fa:
            return JsonResponse(data={'errors': ['2fa not enabled']}, status=400)
        user.has_2fa = False
        user.save()

        return JsonResponse(data={'message': '2fa disabled'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class Verify2fa(View):
    @csrf_exempt
    def post(self, request):
        user_id = get_user_id(request)
        user = User.objects.get(id=user_id)

        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        code = json_request.get('code')
        if not code:
            return JsonResponse(data={'errors': ['code not provided']}, status=400)
        if not user.verify_2fa(code):
            return JsonResponse(data={'errors': ['invalid code or 2fa not enabled']}, status=400)
        if not user.has_2fa:
            user.has_2fa = True
            user.save()
        return JsonResponse(data={'message': '2fa verified'}, status=200)
