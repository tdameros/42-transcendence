import csv
import os

from django.core.mail import EmailMessage
from django.http import HttpRequest, JsonResponse
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
    def get(request: HttpRequest) -> JsonResponse:
        user_id = get_user_id(request)
        user = User.objects.get(id=user_id)
        access_token = request.headers.get('Authorization')
        subject = "Your user infos"
        message = 'Here is your user infos in a CSV file.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        email = EmailMessage(subject, message, from_email, recipient_list)
        for key, url in {'user_stats_id': settings.USER_STATS_URL + f'statistics/user/{user.id}/',
                         'user_stats_history': settings.USER_STATS_URL + f'statistics/user/{user.id}/history/',
                         'user_stats_progress': settings.USER_STATS_URL + f'statistics/user/{user.id}/progress/',
                         }.items():

            try:
                response = InternalRequests.get(url, headers={'Authorization': access_token})
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                return JsonResponse(data={'error': f'Error while fetching {key} : {e}'}, status=500)
            try:
                file_name = f'{key}.csv'
                column_names = list(data.keys())
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)
                    writer.writerow([data[column] for column in column_names])
                email.attach_file(file_name)
            except Exception as e:
                return JsonResponse(data={'error': f'Error while creating email : {e}'}, status=500)
            os.remove(file_name)
        user_infos = [{'username': user.username,
                       'email': user.email,
                       'avatar': settings.USER_MANAGEMENT_URL + f'user/avatar/{user.username}/',
                       'two_fa': user.has_2fa}]
        try:
            file_name = 'user_infos.csv'
            column_names = list(user_infos[0].keys())
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)
                for user_info in user_infos:
                    writer.writerow([user_info[column] for column in column_names])
            email.attach_file(file_name)
            os.remove(file_name)
        except Exception as e:
            return JsonResponse(data={'error': f'Error while creating email : {e}'}, status=500)
        email.send()
        return JsonResponse(data={'ok': 'Email sent', 'email': anonymize_email(user.email)})
