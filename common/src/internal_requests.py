import datetime

import requests

from common.src.jwt_managers import ServiceAccessJWT


class InternalRequests:

    @staticmethod
    def post(url, data=None, json=None, **kwargs):
        kwargs.setdefault('verify', False)
        return requests.post(url, data=data, json=json, **kwargs)

    @staticmethod
    def get(url, **kwargs):
        kwargs.setdefault('verify', False)
        return requests.get(url, **kwargs)

    @staticmethod
    def put(url, data=None, **kwargs):
        kwargs.setdefault('verify', False)
        return requests.put(url, data=data, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        kwargs.setdefault('verify', False)
        return requests.delete(url, **kwargs)

    @staticmethod
    def patch(url, data=None, **kwargs):
        kwargs.setdefault('verify', False)
        return requests.patch(url, data=data, **kwargs)


class InternalAuthRequests:
    service_token = None

    @staticmethod
    def post(url, data=None, json=None, headers=None, **kwargs):
        InternalAuthRequests.update_service_token()
        headers = headers or {}
        headers['Authorization'] = InternalAuthRequests.service_token
        return InternalRequests.post(url, data=data, json=json, headers=headers, **kwargs)

    @staticmethod
    def get(url, headers=None, **kwargs):
        InternalAuthRequests.update_service_token()
        headers = headers or {}
        headers['Authorization'] = InternalAuthRequests.service_token
        return InternalRequests.get(url, headers=headers, **kwargs)

    @staticmethod
    def put(url, data=None, headers=None, **kwargs):
        InternalAuthRequests.update_service_token()
        headers = headers or {}
        headers['Authorization'] = InternalAuthRequests.service_token
        return InternalRequests.put(url, data=data, headers=headers, **kwargs)

    @staticmethod
    def delete(url, headers=None, **kwargs):
        InternalAuthRequests.update_service_token()
        headers = headers or {}
        headers['Authorization'] = InternalAuthRequests.service_token
        return InternalRequests.delete(url, headers=headers, **kwargs)

    @staticmethod
    def patch(url, data=None, headers=None, **kwargs):
        InternalAuthRequests.update_service_token()
        headers = headers or {}
        headers['Authorization'] = InternalAuthRequests.service_token
        return InternalRequests.patch(url, data=data, headers=headers, **kwargs)

    @staticmethod
    def update_service_token():
        valid, token, errors = ServiceAccessJWT.decode_jwt(
            InternalAuthRequests.service_token
        )
        if not valid:
            valid, InternalAuthRequests.service_token, errors = ServiceAccessJWT.generate_jwt()
            return
        expiration_time = token.get('exp')
        expiration_time = datetime.datetime.fromtimestamp(expiration_time, datetime.UTC)
        now = datetime.datetime.now(datetime.UTC)
        if now + datetime.timedelta(seconds=10) > expiration_time:
            valid, InternalAuthRequests.service_token, errors = ServiceAccessJWT.generate_jwt()
