from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.conf import settings
from user.models import User
import jwt


def user_exist(user_id: int) -> bool:
    if (user_id is None
            or user_id == ''
            or type(user_id) != int
            or user_id < 0
            or user_id > settings.MAX_USER_ID):
        return False
    return User.objects.filter(id=user_id).exists()


class JWTManager:
    def __init__(self, token_type: str, payload: dict = None):
        if token_type == 'access':
            self.private_key = settings.ACCESS_KEY
            self.public_key = settings.ACCESS_KEY
            self.algorithm = 'HS256'
            self.expire_minutes_reference = settings.ACCESS_EXPIRATION_MINUTES
        elif token_type == 'refresh':
            self.private_key = settings.REFRESH_PRIVATE_KEY
            self.public_key = settings.REFRESH_PUBLIC_KEY
            self.algorithm = 'RS256'
            self.expire_minutes_reference = settings.REFRESH_EXPIRATION_MINUTES
        else:
            raise Exception('Invalid token type')
        self.token_type = token_type
        self.payload = payload

    def decode_jwt(self, encoded_jwt: str) -> (bool, dict, str):
        try:
            decoded_payload = jwt.decode(encoded_jwt, self.public_key, algorithms=[self.algorithm])
            return True, decoded_payload, None
        except Exception as e:
            return False, None, str(e)

    def generate_token(self, user_id: int) -> (bool, str, str):
        if not user_exist(user_id):
            return False, None, 'User does not exist'
        try:
            now = datetime.utcnow()
            expiration_time = now + timedelta(minutes=self.expire_minutes_reference)
            payload = {
                'user_id': user_id,
                'exp': expiration_time,
                'token_type': self.token_type
            }
            token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        except Exception as e:
            return False, None, str(e)
        return True, token, None

    def is_authentic_and_valid_request(self, encoded_jwt: str) -> (bool, list, int):
        success, decoded_payload, error_decode = self.decode_jwt(encoded_jwt)
        errors = []
        if not success:
            errors.append(error_decode)
        elif decoded_payload is None:
            errors.append('Token expired')
        elif decoded_payload == {}:
            errors.append('Empty payload')
        if errors:
            return False, errors, None

        exp_date = decoded_payload.get('exp')
        exp_date_formatted = datetime.utcfromtimestamp(exp_date)
        if exp_date_formatted < datetime.utcnow():
            errors.append(f'Token expired : {exp_date_formatted} < {datetime.utcnow()}')
        user_id = decoded_payload.get('user_id')
        if user_id is None or user_id == '':
            errors.append('No user_id in payload')
        elif not user_exist(user_id):
            errors.append('User does not exist')
        if errors:
            return False, errors, None
        return True, None, user_id
