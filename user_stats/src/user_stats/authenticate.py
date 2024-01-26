import json
from typing import Any

import jwt
import requests
from django.http import HttpRequest

from user_stats import settings


def authenticate(request: HttpRequest) -> (Any, list[str]):
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


def decode_jwt(encoded_jwt: Any, errors: list[str]) -> Any:
    try:
        decoded_payload = jwt.decode(encoded_jwt, settings.ACCESS_PUBLIC_KEY,
                                     algorithms=[settings.DECODE_ALGORITHM])
        return decoded_payload
    except Exception as e:
        errors.append(str(e))
        return None


def get_user(user_id: int, encoded_jwt: Any, errors: list[str]):
    headers = {'Authorization': encoded_jwt}
    try:
        response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}/', headers=headers)

        if response.status_code == 200:
            return json.loads(response.text)

        body = json.loads(response.body.decode('utf-8'))

        errors.extend(body['errors'])
        return None
    except Exception as e:
        errors.append(str(e))
        return None
