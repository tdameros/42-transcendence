from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import service_authentication
from user.models import User
from user.views.delete_account import delete_account
from user_management import settings
from user_management.JWTManager import UserAccessJWTManager


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['DELETE']), name='dispatch')
class DeleteInactiveUsersView(View):
    @staticmethod
    def delete(request: HttpRequest) -> JsonResponse:
        response = remove_inactive_users()
        if response:
            return JsonResponse({'errors': [response]}, status=500)
        response = remove_old_pending_accounts()
        if response:
            return JsonResponse({'errors': [response]}, status=500)
        return JsonResponse({'message': 'Inactive users deleted'}, status=200)


def remove_inactive_users():
    try:
        users = User.objects.all()
        inactive_users = [user for user in users if (timezone.now() - user.last_activity > timezone.timedelta(
            days=settings.MAX_INACTIVITY_DAYS_BEFORE_DELETION))]

        for user in inactive_users:
            success, access_token, errors = UserAccessJWTManager.generate_jwt(user.id)
            response = delete_account(user.id, access_token)
            if response.get('errors'):
                return f'Error deleting user {user.id} : {response}'
        return f'Inactive users deleted : {inactive_users}'
    except Exception as e:
        return f'Error fetching users : {e}'


def remove_old_pending_accounts():
    try:
        pending_accounts = User.objects.filter(
            emailVerified=False,
            date_joined__lt=timezone.now() - timezone.timedelta(
                days=settings.MAX_DAYS_BEFORE_PENDING_ACCOUNTS_DELETION)
        )
        deleted_accounts = ""
        timezone_infos = f'timezone.now() : {timezone.now()} \n'
        for user in pending_accounts:
            date_joined__lt_calculus = timezone.now() - timezone.timedelta(
                days=settings.MAX_DAYS_BEFORE_PENDING_ACCOUNTS_DELETION)
            deleted_accounts += (f'id : {user.id}, '
                                 f'username : {user.username}, '
                                 f'email : {user.email}, '
                                 f'emailVerified : {user.emailVerified},'
                                 f'last_activity : {user.last_activity},'
                                 f'date_joined : {user.date_joined},'
                                 f'date_joined__lt calculus : {date_joined__lt_calculus} \n')
            user.delete()
        return f'Pending accounts deleted : {deleted_accounts} \n @{timezone_infos}'
    except Exception as e:
        return f'Error deleting pending accounts : {e}'
