import jwt


def get_fake_headers(user_id: int) -> dict:
    fake_payload = {'user_id': user_id, 'username': 'admin'}
    fake_jwt = jwt.encode(fake_payload, key=None, algorithm=None)
    headers = {'Authorization': fake_jwt}
    return headers
