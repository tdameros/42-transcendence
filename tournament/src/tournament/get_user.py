import base64
import json

import requests
from django.http import HttpRequest

from tournament import settings


def get_jwt(request: HttpRequest) -> str:
    return request.headers.get('Authorization')


def get_username_by_id(user_id: int, jwt: str) -> str:
    headers = {'Authorization': jwt}
    response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}/', headers=headers)
    return response.json()['username']


def get_user_id(request: HttpRequest) -> int:
    jwt = request.headers.get('Authorization')
    split_jwt = jwt.split('.')
    payload = base64.b64decode(split_jwt[1] + '===')

    payload_dict = json.loads(payload)
    return int(payload_dict['user_id'])


def get_username(request: HttpRequest) -> str:
    user_id = get_user_id(request)

    headers = {'Authorization': request.headers.get('Authorization')}
    response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}/', headers=headers)
    return response.json()['username']
