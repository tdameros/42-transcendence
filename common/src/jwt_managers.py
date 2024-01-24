from datetime import datetime, timedelta, timezone

import jwt

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

    def generate_token(self, payload_arg: dict) -> (bool, str | None, list[str] | None):
        """ returns: Success, jwt, [error messages] """

        now = datetime.now(timezone.utc)
        expiration_time_minutes = now + timedelta(minutes=self.expiration_time_minutes)

        payload = {'exp': expiration_time_minutes}
        for key, value in payload_arg.items():
            payload[key] = value

        try:
            token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        except Exception as e:
            return False, None, [str(e)]
        return True, token, None

    def decode_jwt(self, encoded_jwt: str) -> (bool, dict | None, list[str] | None):
        """ returns: Success, payload, error message """

        try:
            decoded_payload = jwt.decode(encoded_jwt, self.public_key, algorithms=[self.algorithm])
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

        success, decoded_payload, error_decode = UserAccessJWTDecoder.JWT_MANAGER.decode_jwt(encoded_jwt)
        if not success:
            return False, None, error_decode

        user_id = decoded_payload.get('user_id')
        if user_id is None or user_id == '':
            return False, None, ['No user_id in payload']

        return True, decoded_payload, None
