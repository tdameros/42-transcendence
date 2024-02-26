from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailView(View):
    @csrf_exempt
    def post(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(data={'errors': ['user not found']}, status=404)
        except Exception:
            return JsonResponse(data={'errors': ['invalid user id']}, status=400)

        if user.is_verified:
            return JsonResponse(data={'errors': ['user already verified']}, status=400)
        if not default_token_generator.check_token(user, token):
            return JsonResponse(data={'errors': ['invalid token']}, status=400)

        try:
            user.is_verified = True
            user.save()
        except Exception:
            return JsonResponse(data={'errors': ['an error occurred while verifying the user']}, status=500)
        return JsonResponse(data={'message': 'user verified'}, status=200)
