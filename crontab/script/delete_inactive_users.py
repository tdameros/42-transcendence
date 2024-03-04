import logging

from common.src import settings
from common.src.internal_requests import InternalAuthRequests


response = InternalAuthRequests.delete(
    f'{settings.USER_MANAGEMENT_URL}user/delete-inactive-users/'
)

if not response.ok:
    logging.error(f'Error deleting inactive users: {response.text}')
else:
    logging.info('Inactive users deleted')