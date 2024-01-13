from typing import Optional

import jwt
import requests

import src.settings as settings


def authenticate_user(token: str) -> Optional[dict]:
    payload = decode_jwt(token)
    if payload is None:
        return None
    user_id = payload.get('user_id')
    if user_id is None:
        return None
    # TODO: Uncomment the following lines when the `user/` endpoint is implemented
    # user = get_user(user_id, token)
    # return user
    return payload


def decode_jwt(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.VALID_TOKEN,
            algorithms=[settings.DECODE_ALGORITHM],
        )
        return payload
    except Exception:
        return None


def get_user(user_id: int, token: str) -> Optional[dict]:
    headers = {'Authorization': token}
    try:
        response = requests.get(f'{settings.USER_MANAGEMENT_USER_ENDPOINT}{user_id}', headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None
