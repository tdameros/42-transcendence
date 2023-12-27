from datetime import datetime, timedelta

import jwt
from django.conf import settings

from user.models import User


def user_exist(user_id):
    return User.objects.filter(id=user_id).exists()


class JWTManager:
    def __init__(self, token_type, payload=None):
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

    def decode_jwt(self, encoded_jwt):
        try:
            decoded_payload = jwt.decode(encoded_jwt, self.public_key, algorithms=[self.algorithm])
            return True, decoded_payload
        except Exception:
            return False, None

    def generate_token(self, user_id):
        now = datetime.utcnow()
        expiration_time = now + timedelta(minutes=self.expire_minutes_reference)
        payload = {
            'user_id': user_id,
            'exp': expiration_time,
            'token_type': self.token_type
        }
        token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return token

    def is_authentic_and_valid_request(self, request):
        encoded_jwt = request.headers.get('Authorization')
        success, decoded_payload = self.decode_jwt(encoded_jwt)
        if not success:
            return False, 'Invalid token', None
        if decoded_payload is None:
            return False, 'Empty payload', None
        if decoded_payload.get('exp') < datetime.now():
            return False, 'Token expired', None
        user_id = decoded_payload.get('user_id')
        if user_id is None:
            return False, 'No user_id in payload', None
        if user_exist(user_id):
            return True, None, user_id
        return False, 'User does not exist', None
