import csv
import os

from django.core.mail import EmailMessage
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.internal_requests import InternalRequests
from common.src.jwt_managers import user_authentication
from user.models import User, UserOAuth
from user.views.forgot_password import anonymize_email
from user_management import settings
from user_management.JWTManager import get_user_id


@method_decorator(user_authentication(['GET']), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class SendUserInfosView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            user_id = get_user_id(request)
            user = User.objects.get(id=user_id)
            access_token = request.headers.get('Authorization')

            email = self._prepare_email(user.email)
            self._attach_user_data(email, user, access_token)

            email.send()
            return JsonResponse(data={'ok': 'Email sent', 'email': anonymize_email(user.email)})
        except Exception as e:
            return JsonResponse(data={'error': f'Error while sending email: {e}'}, status=500)

    def _prepare_email(self, recipient_email):
        subject = "Your user information"
        message = 'Here are the data related to your account in CSV files.'
        from_email = settings.EMAIL_HOST_USER
        return EmailMessage(subject, message, from_email, [recipient_email])

    def _attach_user_data(self, email, user, access_token):
        try:
            self._attach_user_stats(email, user, access_token)
            user_info = {
                'username': user.username,
                'email': user.email,
                'avatar': f'{settings.USER_MANAGEMENT_IP}user/avatar/{user.username}/',
                'two_fa': user.has_2fa,
                'last_login': user.last_login,
                'last_activity': user.last_activity,
                'date_joined': user.date_joined
            }
            self._attach_csv_file(email, 'user_infos.csv', user_info)
            user_oauth_data = []
            for row in UserOAuth.objects.filter(user_id=user.id):
                user_oauth_data.append([row.service, row.service_id])
            self._attach_csv_file(email, 'user_oauth_infos.csv', user_oauth_data)
        except Exception as e:
            raise e

    def _attach_user_stats(self, email, user, access_token):
        for key, url in {'user_stats_id': f'statistics/user/{user.id}/',
                         'user_stats_history': f'statistics/user/{user.id}/history/',
                         'user_stats_progress': f'statistics/user/{user.id}/progress/',
                         }.items():
            try:
                response = InternalRequests.get(settings.USER_STATS_URL + url, headers={'Authorization': access_token})
                response.raise_for_status()
                data = response.json()
                self._attach_csv_file(email, f'{key}.csv', data)
            except Exception as e:
                raise e

    def _attach_csv_file(self, email, file_name, data):
        try:
            with open(file_name, 'w', newline='') as csvfile:
                if isinstance(data, dict):
                    fieldnames = data.keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(data)
                else:
                    writer = csv.writer(csvfile)
                    for row in data:
                        writer.writerow(row)

            email.attach_file(file_name)
            os.remove(file_name)
        except Exception as e:
            raise e
