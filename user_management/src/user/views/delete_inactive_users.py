from django.utils import timezone
from django.views import View

from user.models import User
from user.views.delete_account import delete_account
from user_management import settings
from user_management.JWTManager import UserAccessJWTManager


class DeleteInactiveUsersView(View):

    def remove_inactive_users(self):
        try:
            users = User.objects.all()
            inactive_users = [user for user in users if (timezone.now() - user.last_activity > timezone.timedelta(
                days=settings.MAX_INACTIVITY_DAYS_BEFORE_DELETION))]

            for user in inactive_users:
                success, access_token, errors = UserAccessJWTManager.generate_jwt(user.id)
                response = delete_account(user.id, access_token)
                if not response.ok:
                    return f'Error deleting user {user.id} : {response}'
        except Exception as e:
            return f'Error fetching users : {e}'

    def remove_old_pending_accounts(self):

        try:
            pending_accounts = User.objects.filter(
                emailVerified=False,
                date_joined__lt=timezone.now() - timezone.timedelta(
                    days=settings.MAX_DAYS_BEFORE_PENDING_ACCOUNTS_DELETION)
            )
            for user in pending_accounts:
                user.delete()
        except Exception as e:
            return f'Error deleting pending accounts : {e}'
