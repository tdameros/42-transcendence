from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from django.http import JsonResponse

import common.src.settings as settings


class JWTManager:
    def __init__(self,
                 private_key: str | None,
                 public_key: str | None,
                 algorithm: str,
                 expiration_time_minutes: int | None):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.expiration_time_minutes = expiration_time_minutes

    def generate_jwt(self, payload_arg: dict) -> (bool, str | None, list[str] | None):
        """ returns: Success, jwt, [error messages] """

        now = datetime.now(timezone.utc)
        expiration_time_minutes = now + timedelta(minutes=self.expiration_time_minutes)

        payload: dict = {}
        for key, value in payload_arg.items():
            payload[key] = value
        payload['exp'] = expiration_time_minutes

        try:
            token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        except Exception as e:
            return False, None, [str(e)]
        return True, token, None

    def decode_jwt(self, encoded_jwt: str) -> (bool, dict | None, list[str] | None):
        """ returns: Success, payload, error message """

        try:
            decoded_payload = jwt.decode(
                encoded_jwt, self.public_key, algorithms=[self.algorithm]
            )
            if decoded_payload.get('exp') is None:
                return False, None, ["No expiration date found"]
            return True, decoded_payload, None
        except Exception as e:
            return False, None, [str(e)]


class UserAccessJWTDecoder:
    JWT_MANAGER = JWTManager(None,
                             settings.ACCESS_PUBLIC_KEY,
                             settings.ACCESS_ALGORITHM,
                             None)

    @staticmethod
    def authenticate(encoded_jwt: str) -> (bool, dict, list[str] | None):
        """ returns: Success, payload, error message """

        success, decoded_payload, error_decode = UserAccessJWTDecoder.JWT_MANAGER.decode_jwt(
            encoded_jwt
        )
        if not success:
            return False, None, error_decode

        user_id = decoded_payload.get('user_id')
        if user_id is None or user_id == '':
            return False, None, ['No user_id in payload']

        return True, decoded_payload, None


class ServiceAccessJWT(JWTManager):
    JWT_MANAGER = JWTManager(
        settings.SERVICE_KEY,
        settings.SERVICE_KEY,
        settings.SERVICE_ACCESS_ALGORITHM,
        settings.SERVICE_EXPIRATION_TIME,
    )

    @staticmethod
    def generate_jwt() -> (bool, str | None, list[str] | None):
        """ returns: Success, jwt, [error messages] """

        return ServiceAccessJWT.JWT_MANAGER.generate_jwt({})

    @staticmethod
    def decode_jwt(encoded_jwt: str) -> (bool, dict | None, list[str] | None):
        """ returns: Success, payload, error message """

        return ServiceAccessJWT.JWT_MANAGER.decode_jwt(encoded_jwt)

    @staticmethod
    def authenticate(token: str) -> (bool, list[str] | None):
        """ returns: Success, error message """

        success, decoded_payload, error_decode = ServiceAccessJWT.JWT_MANAGER.decode_jwt(token)
        if not success:
            return False, error_decode
        return True, None


def user_authentication(methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method in methods:
                token = request.headers.get('Authorization')
                valid, user, errors = UserAccessJWTDecoder.authenticate(token)
                if not valid:
                    return JsonResponse({'errors': errors}, status=401)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def service_authentication(methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method in methods:
                token = request.headers.get('Authorization')
                valid, errors = ServiceAccessJWT.authenticate(token)
                if not valid:
                    return JsonResponse({'errors': errors}, status=401)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
