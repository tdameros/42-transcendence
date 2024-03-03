from django.core.management.base import BaseCommand

from user.views.delete_inactive_users import DeleteInactiveUsersView


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        view = DeleteInactiveUsersView()
        view.remove_inactive_users()
        view.remove_old_pending_accounts()



