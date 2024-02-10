import json

from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.settings import MEDIA_ROOT, STATIC_ROOT
from user_management.utils import save_image_from_base64


@method_decorator(csrf_exempt, name='dispatch')
class AvatarView(View):
    @staticmethod
    def get(request, username):
        user = User.objects.filter(username=username).first()
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
        user = User.objects.filter(username=username).first()
        base64_string = json_request.get('image')
        if not base64_string:
            return JsonResponse(data={'error': 'Image not found'}, status=400)
        if not user:
            return JsonResponse(data={'error': 'User not found'}, status=404)
        if not base64_string:
            return JsonResponse(data={'error': 'Image not found'}, status=400)
        if not base64_string.startswith('data:image/png;base64,'):
            return JsonResponse(data={'error': 'Invalid image format'}, status=400)
        base64_string = base64_string.replace('data:image/png;base64,', '')
        save_image_from_base64(base64_string, user)

        return JsonResponse(data={'message': 'Avatar updated'}, status=200)
