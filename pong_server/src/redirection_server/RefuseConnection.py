import json
import logging

from socketio.exceptions import ConnectionRefusedError


class RefuseConnection(ConnectionRefusedError):
    def __init__(self, error_message: str):
        super().__init__(json.dumps({'error': error_message}))
        logging.error(f"SendURI({ {'error': error_message} })")
