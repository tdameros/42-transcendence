import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User


@method_decorator(user_authentication(['GET']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserIdView(View):
    @staticmethod
    def get(request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            if user is None:
                return JsonResponse(data={'errors': ['User not found']}, status=404)
            return JsonResponse(data={'id': user.id, 'username': user.username}, status=200)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)


@method_decorator(user_authentication(['POST']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserIdListView(View):
    @staticmethod
    def post(request):
        try:
            id_list = json.loads(request.body).get('id_list')
        except Exception:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        if not all(isinstance(user_id, int) and user_id >= 0 for user_id in id_list):
            return JsonResponse(data={'errors': ['id_list should contain positive integers']}, status=400)
        try:
            if not isinstance(id_list, list):
                return JsonResponse(data={'errors': ['id_list should be a list']}, status=400)

            users = User.objects.filter(id__in=id_list)
            response = {user.id: user.username for user in users}
            return JsonResponse(data=response, status=200, safe=False)

        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
