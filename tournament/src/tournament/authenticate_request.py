import base64
import json

import jwt
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


def authenticate_request(request):
    encoded_jwt = request.headers.get('Authorization')
    errors = []
    if encoded_jwt is None:
        return None, 'Missing Authorization header'
    payload = decode_jwt(encoded_jwt, errors)
    if payload is None:
        return None, errors
    user_id = payload.get('user_id')
    if user_id is None:
        return None, errors
    user = get_user(user_id, encoded_jwt, errors)
    if user is None:
        return None, errors
    user['id'] = user_id
    return user, None


def decode_jwt(encoded_jwt, errors):
    try:
        decoded_payload = jwt.decode(encoded_jwt, settings.ACCESS_PUBLIC_KEY,
                                     algorithms=[settings.DECODE_ALGORITHM])
        return decoded_payload
    except Exception as e:
        errors.append(str(e))
        return None


def get_user(user_id, encoded_jwt, errors):
    headers = {'Authorization': encoded_jwt}
    try:
        response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}/', headers=headers)

        if response.status_code == 200:
            return response.json()

        body = response.json()

        errors.extend(body['errors'])
        return None
    except Exception as e:
        errors.append(str(e))
        return None
