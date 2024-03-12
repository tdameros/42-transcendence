import base64
import json
import os
import sys

from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User
from user_management import settings
from user_management.JWTManager import get_user_id
from user_management.settings import MEDIA_ROOT, STATIC_ROOT
from user_management.utils import (get_image_format_from_base64,
                                   save_image_from_base64)


@method_decorator(user_authentication(['POST', 'DELETE']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AvatarView(View):

    @staticmethod
    def create_file_response(path):
        return FileResponse(open(path, 'rb'), content_type='image/png')

    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse(data={'errors': [f'Invalid JSON : {e}']}, status=400)
        try:
            user_id = get_user_id(request)
            user = User.objects.filter(id=user_id).first()
        except Exception as e:
            return JsonResponse(data={'errors': [f'Error getting user : {e}']}, status=500)

        base64_string = json_request.get('avatar')
        if not base64_string:
            return JsonResponse(data={'errors': ['Image not found']}, status=400)
        if not user:
            return JsonResponse(data={'errors': ['User not found']}, status=404)
        if not base64_string:
            return JsonResponse(data={'errors': ['Image not found']}, status=400)
        image_format = get_image_format_from_base64(base64_string)
        if not image_format:
            return JsonResponse(data={'errors': ['Invalid image format']}, status=400)
        if image_format not in ['png', 'jpg', 'jpeg']:
            return JsonResponse(data={'errors': ['Invalid image format']}, status=400)
        try:
            base64_data = base64_string.split(';base64')[1]
            image_data = base64.b64decode(base64_data)
        except Exception:
            return JsonResponse(data={'errors': ['Invalid image format']}, status=400)
        if sys.getsizeof(image_data) > settings.MAX_IMAGE_SIZE:
            return JsonResponse(data={
                'errors': [
                    f'Image too big (max {settings.MAX_IMAGE_SIZE / 1000000} Mb, '
                    f'your image is {sys.getsizeof(image_data) / 1000000} Mb)']},
                status=400)
        success, error = save_image_from_base64(base64_data, user)
        if not success:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'Avatar updated'}, status=200)

    @staticmethod
    def delete(request):
        try:
            user_id = get_user_id(request)
            user = User.objects.filter(id=user_id).first()
        except Exception as e:
            return JsonResponse(data={'errors': [f'Error getting user : {e}']}, status=500)
        if not user:
            return JsonResponse(data={'errors': ['User not found']}, status=404)
        if not user.avatar:
            return JsonResponse(data={'message': 'User already has no avatar'}, status=200)
        file_to_delete = f'{MEDIA_ROOT}/{str(user.avatar)}'
        user.avatar = None
        user.save()
        try:
            os.remove(file_to_delete)
        except Exception as e:
            return JsonResponse(data={'errors': [f'Error deleting file : {e}']}, status=500)

        return JsonResponse(data={'message': 'Avatar deleted'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class GetAvatarView(View):

    @staticmethod
    def get(request, username):
        try:
            user = User.objects.filter(username=username).first()
        except Exception as e:
            return JsonResponse(data={'errors': [f'Error getting user : {e}']}, status=500)
        if not user:
            return JsonResponse(data={'errors': ['User not found']}, status=404)
        if not user.avatar:
            return AvatarView.create_file_response(f'{STATIC_ROOT}/default_avatar.png')
        path = f'{MEDIA_ROOT}/{str(user.avatar)}'
        return AvatarView.create_file_response(path)
