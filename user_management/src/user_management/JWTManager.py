import base64
import json

from django.conf import settings
from django.http import HttpRequest

import common.src.settings as common_settings
from common.src.jwt_managers import JWTManager, UserAccessJWTDecoder
from user.models import User


def user_exist(user_id: int) -> bool:
    if (user_id is None
            or user_id == ''
            or type(user_id) is not int
            or user_id < 0):
        return False
    return User.objects.filter(id=user_id).exists()


class UserRefreshJWTManager:
    JWT_MANAGER = JWTManager(settings.REFRESH_KEY,
                             settings.REFRESH_KEY,
                             'HS256',
                             settings.REFRESH_EXPIRATION_MINUTES)

    @staticmethod
    def generate_jwt(user_id: int) -> (bool, str | None, list[str] | None):
        """ returns: Success, jwt, [error messages] """

        if not user_exist(user_id):
            return False, None, ['User does not exist']
        return UserRefreshJWTManager.JWT_MANAGER.generate_jwt({'user_id': user_id, 'token_type': 'refresh'})  # Common

    @staticmethod
    def authenticate(encoded_jwt: str) -> (bool, int | None, list[str] | None):
        """ returns: Success, user_id, [error messages] """

        success, payload, error_list = UserRefreshJWTManager.JWT_MANAGER.decode_jwt(encoded_jwt)  # Common
        if not success:
            return False, None, error_list

        user_id = payload.get('user_id')
        if user_id is None or user_id == '':
            return False, None, ['No user_id in payload']
        elif not user_exist(user_id):
            return False, None, ['User does not exist']
        return True, user_id, None


def get_user_id(request: HttpRequest) -> int:
    jwt = request.headers.get('Authorization')
    split_jwt = jwt.split('.')
    payload = base64.b64decode(split_jwt[1] + '===')

    payload_dict = json.loads(payload)
    return int(payload_dict['user_id'])


class UserAccessJWTManager:
    # Never provide the public key as we must use common.UserAccessJWTDecoder to decode
    JWT_MANAGER = JWTManager(settings.ACCESS_PRIVATE_KEY,
                             None,
                             common_settings.ACCESS_ALGORITHM,
                             settings.ACCESS_EXPIRATION_MINUTES)

    @staticmethod
    def generate_jwt(user_id: int) -> (bool, str | None, list[str] | None):
        """ returns: Success, jwt, [error messages] """

        if not user_exist(user_id):
            return False, None, ['User does not exist']
        return UserAccessJWTManager.JWT_MANAGER.generate_jwt({'user_id': user_id, 'token_type': 'access'})  # Common

    @staticmethod
    def authenticate(encoded_jwt: str) -> (bool, str | None, list[str]):
        """ returns: Success, user_id, [error messages] """

        success, payload, error_decode = UserAccessJWTDecoder.authenticate(encoded_jwt)  # Common
        if not success:
            return False, None, error_decode

        user_id = payload['user_id']
        if not user_exist(user_id):
            return False, None, ['User does not exist']

        return True, user_id, None
