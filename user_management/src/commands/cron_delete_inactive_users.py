from django.conf import settings
from django.core.management.base import BaseCommand

from user.views.delete_inactive_users import DeleteInactiveUsersView


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # post request to delete inactive users
        view = DeleteInactiveUsersView()
        request = type('Request', (object,), {'headers': {'Authorization': settings.USER_MANAGEMENT_SECRET_KEY}})
        view.post(request)
