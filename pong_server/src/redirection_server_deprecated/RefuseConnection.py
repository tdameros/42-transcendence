import json
import logging

from socketio.exceptions import ConnectionRefusedError


class RefuseConnection(ConnectionRefusedError):
    def __init__(self, error_message: str):
        error = {'error': error_message}
        super().__init__(json.dumps(error))
        logging.error(f"SendURI({error})")
