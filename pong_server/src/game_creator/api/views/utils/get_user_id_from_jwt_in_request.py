import base64
import json

from django.http import HttpRequest


def get_user_id_from_jwt_in_request(request: HttpRequest) -> int:
    jwt = request.headers.get('Authorization')
    split_jwt = jwt.split('.')
    payload = base64.b64decode(split_jwt[1] + '===')

    payload_dict = json.loads(payload)
    return int(payload_dict['user_id'])
