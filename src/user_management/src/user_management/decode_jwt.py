from django.conf import settings
from user.models import User
import jwt


def authenticate_request(request):
    encoded_jwt = request.headers.get('Authorization')
    if encoded_jwt is None:
        return None
    payload = decode_jwt(encoded_jwt)
    if payload is None:
        return None
    user_id = payload.get('user_id')
    if user_id is None:
        return None
    if user_exist(user_id):
        return user_id
    return None


def decode_jwt(encoded_jwt):
    try:
        decoded_payload = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except:
        return None


def user_exist(user_id):
    return User.objects.filter(id=user_id).exists()
