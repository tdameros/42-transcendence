from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User
from user_management.JWTManager import get_user_id


@method_decorator(user_authentication(['GET']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MeView(View):
    @staticmethod
    def get(request):
        user_id = get_user_id(request)
        user = User.objects.get(id=user_id)
        return JsonResponse(data={'id': user.id,
                                  'username': user.username,
                                  'email': user.email,
                                  '2fa': user.has_2fa,
                                  'OAuth': user.oauth,
                                  }, status=200)
