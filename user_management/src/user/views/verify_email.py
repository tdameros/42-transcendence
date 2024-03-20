from datetime import datetime, timezone

from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import UserRefreshJWTManager
from user_management.utils import post_user_stats


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

        if user.emailVerified:
            return JsonResponse(data={'errors': ['user already verified']}, status=400)
        if not default_token_generator.check_token(user, token):
            return JsonResponse(data={'errors': ['invalid verification token']}, status=401)
        if user.emailVerificationTokenExpiration < datetime.now(timezone.utc):
            try:
                user.emailVerificationToken = None
                user.emailVerificationTokenExpiration = None
                user.save()
            except Exception:
                return JsonResponse(
                    data={'errors': ['an error occurred while removing the expired token']}, status=500)
            return JsonResponse(data={'errors': ['verification token expired']}, status=401)
        valid, errors = post_user_stats(user.id)
        if not valid:
            return JsonResponse(data={'errors': errors}, status=500)
        try:
            user.emailVerified = True
            user.save()
        except Exception:
            return JsonResponse(data={'errors': ['an error occurred while verifying the user']}, status=500)
        try:
            success, refresh_token, errors = UserRefreshJWTManager.generate_jwt(user.id)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            try:
                user.update_latest_login()
                user.emailVerificationToken = None
                user.emailVerificationTokenExpiration = None
                user.save()
            except Exception as e:
                return JsonResponse(
                    data={'errors': [f'An error occurred : {e}']}, status=500)
            return JsonResponse(data={'message': 'user verified', 'refresh_token': refresh_token}, status=200)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred: {e}']}, status=500)
