import json
import logging

from socketio.exceptions import ConnectionRefusedError


class SendURI(ConnectionRefusedError):
    def __init__(self, game_server_uri: str):
        super().__init__(json.dumps({'game_server_uri': game_server_uri}))
        logging.info(f"SendURI({ {'game_server_uri': game_server_uri} })")
