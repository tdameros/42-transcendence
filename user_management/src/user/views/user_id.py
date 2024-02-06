import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User


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


class UserIdListView(View):
    @staticmethod
    def post(request):
        id_list = json.loads(request.body).get('id_list')
        if not isinstance(id_list, list):
            return JsonResponse(data={'errors': ['id_list should be a list']}, status=400)
        response = []
        for user_id in id_list:
            user = User.objects.filter(id=user_id).first()
            if user is not None:
                response.append({'id': user.id, 'username': user.username})
        return JsonResponse(data=response, status=200, safe=False)
