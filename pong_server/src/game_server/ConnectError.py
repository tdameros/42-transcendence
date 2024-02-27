import json

from socketio.exceptions import ConnectionRefusedError


class ConnectError(Exception):
    def __init__(self, message: str, status_code: int):
        self._message = message
        self._status_code = status_code

    def to_socket_io_exception(self):
        return ConnectionRefusedError(json.dumps(self.to_dict()))

    def to_dict(self):
        return {
            'message': self._message,
            'status_code': self._status_code,
        }
