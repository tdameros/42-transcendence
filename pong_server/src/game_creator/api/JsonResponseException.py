from django.http import JsonResponse


class JsonResponseException(BaseException):
    def __init__(self, data: dict, status):
        self._data = data
        self._status = status

    def to_json_response(self):
        return JsonResponse(self._data, status=self._status)
