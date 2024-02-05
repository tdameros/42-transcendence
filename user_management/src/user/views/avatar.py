import json

from django.http import JsonResponse
from django.http import FileResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from user.models import User
from user_management.settings import MEDIA_ROOT, STATIC_ROOT


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
        json_request = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username=username).first()
        image_file = json_request.get('image')
        if image_file:
            try:
                with Image.open(image_file) as img:
                    # Vous pouvez ajouter d'autres vérifications ici si nécessaire, par exemple, vérifier les dimensions, etc.
                    pass
            except Exception as e:
                return JsonResponse({'message': 'Fichier non valide. Assurez-vous d\'envoyer une image valide.'}, status=400)
            # Créez une instance du modèle et enregistrez l'image
            user.avatar = image_file
            user.save()
        return JsonResponse(data={'message': 'Avatar updated'}, status=200)