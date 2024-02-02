from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserIdView(View):
    @staticmethod
    def get(request, user_id):
        if not user_id.isnumeric():
            return JsonResponse(data={'errors': ['User id must be an integer']}, status=400)
        try:
            user = User.objects.filter(id=user_id).first()
            if user is None:
                return JsonResponse(data={'errors': ['User not found']}, status=404)
            return JsonResponse(data={'username': user.username}, status=200)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
