import logging
from typing import Optional

import jwt
import requests

import src.settings as settings


def authenticate_user(auth: str) -> (Optional[dict], list):
    errors = []
    if auth is None:
        errors.append('`auth` field is missing')
        return None, errors
    token = auth.get('token')
    if token is None:
        errors.append('`token` field is missing')
        return None, errors
    logging.debug(f'token: {token}')
    payload = decode_jwt(token, errors)
    logging.debug(f'payload: {payload}')
    if payload is None:
        return None, errors
    user_id = payload.get('user_id')
    if user_id is None:
        return None, errors
    user = get_user(user_id, token, errors)
    return user, None


def decode_jwt(token: str, error: list) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_KEY,
            algorithms=[settings.DECODE_ALGORITHM],
        )
        return payload
    except Exception as e:
        error.append(str(e))
        return None


def get_user(user_id: int, token: str, error: list) -> Optional[dict]:
    headers = {'Authorization': token}
    try:
        response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}', headers=headers)
    except Exception as e:
        error.append(str(e))
        return None
    if response.status_code == 200:
        return response.json()
    return None
