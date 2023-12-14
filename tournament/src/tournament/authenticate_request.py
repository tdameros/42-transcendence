import json
import jwt
import requests


def authenticate_request(request):
    encoded_jwt = request.headers.get('Authorization')
    errors = []
    if encoded_jwt is None:
        return None, errors
    payload = decode_jwt(encoded_jwt, errors)
    if payload is None:
        return None, errors
    user_id = payload.get('user_id')
    if user_id is None:
        return None, errors
    user = get_user(user_id, encoded_jwt, errors)
    if user is not None:
        return user, None
    return None, errors


def decode_jwt(encoded_jwt, errors):
    try:
        decoded_payload = jwt.decode(encoded_jwt, 'django-insecure-&r*!icx1$(sv7f-sj&ezvjxw+pljt-yz(r6yowfg18ihdu@15k',
                                     algorithms=["HS256"])
        return decoded_payload
    except Exception as e:
        errors.append(str(e))
        return None


def get_user(user_id, encoded_jwt, errors):
    headers = {'Authorization': encoded_jwt}
    try:
        response = requests.get(f'http://user-management-nginx/user/{user_id}', headers=headers)
        user = get_json_body(response)
        if response.status_code == 200:
            return user
        errors.append('Error in user-management service')
        # TODO: return errors from response.body
        # errors.append(json_body['errors'])
        return None
    except Exception as e:
        errors.append(str(e))
        return None


def get_json_body(response, errors):
    try:
        json_body = json.loads(response.body.decode('utf-8'))
        return json_body
    except Exception as e:
        errors.append(str(e))
        return None
