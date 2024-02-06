import requests


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
