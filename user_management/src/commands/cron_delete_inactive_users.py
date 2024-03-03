from django.core.management.base import BaseCommand

from user.delete_inactive_users import remove_inactive_users, remove_old_pending_accounts


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        remove_inactive_users()
        remove_old_pending_accounts()
