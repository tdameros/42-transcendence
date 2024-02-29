import logging

from common.src import settings
from common.src.internal_requests import InternalAuthRequests


response = InternalAuthRequests.delete(
    f'{settings.TOURNAMENT_ENDPOINT}delete-inactive/'
)

if not response.ok:
    logging.error(f'Error deleting inactive tournaments: {response.text}')