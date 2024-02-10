import json

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from user.models import User


@method_decorator(user_authentication(['POST']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class SearchUsernameView(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            search_query = json_request.get('username')
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        if search_query is None or search_query == '':
            return JsonResponse(data={'errors': ['Username not found']}, status=400)
        matching_users = User.objects.filter(username__icontains=search_query)[:settings.MAX_USERNAME_SEARCH_RESULTS]
        if matching_users.exists():
            return JsonResponse(data={'users': [user.username for user in matching_users]}, status=200)
        return JsonResponse(data={'users': []}, status=200)
