from django.core.mail import send_mail
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.internal_requests import InternalRequests
from common.src.jwt_managers import user_authentication
from user.models import User
from user.views.forgot_password import anonymize_email
from user_management import settings
from user_management.JWTManager import get_user_id


@method_decorator(user_authentication(['GET']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class SendUserInfosView(View):

    @staticmethod
    def get(request : HttpRequest) -> JsonResponse:
        user_id = get_user_id(request)
        user = User.objects.get(id=user_id)
        infos = {'username': user.username,
                 'email': user.email,
                 'avatar': settings.USER_MANAGEMENT_URL + f'user/avatar/{user.username}/',
                 'two_fa': user.has_2fa,
                 }

        for key, url in {'user_stats_id': settings.USER_STATS_URL + f'statistics/user/{user.id}/',
                         'user_stats_history': settings.USER_STATS_URL + f'statistics/user/{user.id}/history/',
                         'user_stats_progress': settings.USER_STATS_URL + f'statistics/user/{user.id}/progress/',
                        }.items():

            access_token = request.headers.get('Authorization')
            try:
                response = InternalRequests.get(url, headers={'Authorization': access_token})
                response.raise_for_status()
                data = response.json()
                infos[key] = data
            except Exception as e:
                return JsonResponse(data={'error': f'Error while fetching {key} : {e}'}, status=500)

        subject = "Your user infos"
        message = 'Here are your user infos : \n'
        for key, value in infos.items():
            message += f'{key} : {value}\n'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse(data={'ok': 'Email sent', 'email': anonymize_email(user.email)})
