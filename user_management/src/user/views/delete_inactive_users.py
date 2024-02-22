from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user.views.delete_account import delete_account
from user_management import settings
from user_management.JWTManager import UserAccessJWTManager


@method_decorator(csrf_exempt, name='dispatch')
class DeleteInactiveUsersView(View):

    def post(self, request):
        if request.headers.get('Authorization') != settings.USER_MANAGEMENT_SECRET_KEY:
            return JsonResponse(data={'errors': ['Unauthorized']}, status=401)
        users = User.objects.all()
        inactive_users = []

        for user in users:
            if (timezone.now() - user.last_activity >
                    timezone.timedelta(days=settings.MAX_INACTIVITY_DAYS_BEFORE_DELETION)):
                inactive_users.append(user)

        for user in inactive_users:
            access_token = UserAccessJWTManager.generate_jwt(user.id)[1]
            try:
                response = delete_account(user.id, access_token)
            except Exception as e:
                return JsonResponse(data={'errors': [f'Error deleting user {user.id} : {e}']}, status=500)
            if response.status_code != 200:
                return JsonResponse(data={'errors': [f'Error deleting user {user.id} : {response}']}, status=500)
        return JsonResponse(data={'message': 'Inactive users deleted'}, status=200)
