import json
import os

from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User
from user_management.JWTManager import get_user_id
from user_management.settings import MEDIA_ROOT, STATIC_ROOT
from user_management.utils import save_image_from_base64


@method_decorator(user_authentication(['POST', 'GET', 'DELETE']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AvatarView(View):
    @staticmethod
    def get(request, username):
        try:
            user = User.objects.filter(username=username).first()
        except Exception as e:
            return JsonResponse(data={'error': f'Error getting user : {e}'}, status=500)
        if not user:
            return JsonResponse(data={'error': 'User not found'}, status=404)
        if not user.avatar:
            return AvatarView.create_file_response(f'{STATIC_ROOT}/default_avatar.png')
        path = f'{MEDIA_ROOT}/{str(user.avatar)}'
        return AvatarView.create_file_response(path)

    @staticmethod
    def create_file_response(path):
        return FileResponse(open(path, 'rb'), content_type='image/png')

    @staticmethod
    def post(request, username):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse(data={'error': f'Invalid JSON : {e}'}, status=400)
        try:
            user_id = get_user_id(request)
            user = User.objects.filter(id=user_id).first()
        except Exception as e:
            return JsonResponse(data={'error': f'Error getting user : {e}'}, status=500)
        if user.username != username:
            return JsonResponse(data={'error': 'User not found'}, status=404)

        base64_string = json_request.get('avatar')
        if not base64_string:
            return JsonResponse(data={'error': 'Image not found'}, status=400)
        if not user:
            return JsonResponse(data={'error': 'User not found'}, status=404)
        if not base64_string:
            return JsonResponse(data={'error': 'Image not found'}, status=400)
        if not base64_string.startswith('data:image/png;base64,'):
            return JsonResponse(data={'error': 'Invalid image format'}, status=400)
        base64_string = base64_string.replace('data:image/png;base64,', '')
        success, error = save_image_from_base64(base64_string, user)
        if not success:
            return JsonResponse(data={'error': error}, status=400)
        return JsonResponse(data={'message': 'Avatar updated'}, status=200)

    @staticmethod
    def delete(request, username):
        try:
            user_id = get_user_id(request)
            user = User.objects.filter(id=user_id).first()
        except Exception as e:
            return JsonResponse(data={'error': f'Error getting user : {e}'}, status=500)
        if user.username != username:
            return JsonResponse(data={'error': 'User not found'}, status=404)
        if not user:
            return JsonResponse(data={'error': 'User not found'}, status=404)
        file_to_delete = f'{MEDIA_ROOT}/{str(user.avatar)}'
        user.avatar = None
        user.save()
        try:
            os.remove(file_to_delete)
        except Exception as e:
            return JsonResponse(data={'error': f'Error deleting file : {e}'}, status=500)

        return JsonResponse(data={'message': 'Avatar deleted'}, status=200)
