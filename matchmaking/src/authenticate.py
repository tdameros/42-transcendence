from typing import Optional

import jwt
import requests

import src.settings as settings


def authenticate_user(auth: str) -> (Optional[dict], list):
    if auth is None:
        return None, '`auth` field is missing'
    token = auth.get('token')
    if token is None:
        return None, '`token` field is missing'
    valid, payload, error_msg = decode_jwt(token)
    if not valid:
        return None, error_msg
    user_id = payload.get('user_id')
    if user_id is None:
        return None, '`user_id` field is missing'
    valid, elo, error = request_user_elo(user_id, token)
    if not valid:
        return None, error
    user = {
        'id': user_id,
        'elo': elo,
    }
    return user, None


def decode_jwt(token: str) -> (bool, Optional[dict], Optional[str]):
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_KEY,
            algorithms=[settings.DECODE_ALGORITHM],
        )
        return True, payload, None
    except Exception as e:
        return False, None, str(e)


def request_user_elo(user_id: int, token: str) -> (bool, Optional[int], Optional[str]):
    headers = {
        'Authorization': token,
    }
    try:
        response = requests.get(f'{settings.USER_STATS_USER_ENDPOINT}{user_id}/', headers=headers)
    except requests.exceptions.RequestException:
        return False, None, 'Could not connect to user stats'
    if not response.ok:
        return False, None, 'Could not get user elo'
    user_data = response.json()
    return True, user_data.get('elo'), None
