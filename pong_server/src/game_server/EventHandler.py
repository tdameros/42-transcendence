import logging
from typing import Optional

from socketio.exceptions import ConnectionRefusedError

from AntiCheat import AntiCheat
from ClientManager import ClientManager
from EventEmitter import EventEmitter
from Game.GameManager import GameManager
from Server import Server
from shared_code.get_json_web_token import get_json_web_token
from shared_code.get_query_string import get_query_string


class EventHandler(object):
    @staticmethod
    def init():
        Server.sio.on('connect')(EventHandler._connect)
        Server.sio.on('disconnect')(EventHandler._disconnect)
        Server.sio.on('update_paddle')(EventHandler._update_paddle)

    @staticmethod
    async def _connect(sid: str, environ, auth):
        logging.info(f'{sid} connected')

        user_id = get_json_web_token(get_query_string(environ))['user_id']
        if user_id not in ClientManager.CLIENTS_IDS:
            raise ConnectionRefusedError('You are not part of this game')

        previous_sid = ClientManager.get_user_sid(user_id)
        if previous_sid:
            await Server.sio.disconnect(previous_sid)

        await ClientManager.add_newly_connected_user(user_id, sid)
        if GameManager.has_game_started():
            await EventEmitter.scene(sid,
                                     GameManager.get_player(user_id).get_location(),
                                     GameManager.get_scene())

    @staticmethod
    async def _disconnect(sid: str):
        await ClientManager.remove_disconnected_user(sid)

    @staticmethod
    async def _update_paddle(sid: str, player_data):
        if not GameManager.has_game_started():
            return

        user_id = ClientManager.get_user_id(sid)
        player = GameManager.get_player(user_id)

        success, client_paddle_position, direction = (EventHandler
                                                      ._get_update_paddle_args(player_data))
        if not success:
            return

        if player.get_location().is_looser:
            paddle_position = player.get_paddle().get_position()
            paddle_position[1] = client_paddle_position
            await EventEmitter.update_paddle(
                player.get_location(), direction, paddle_position, None
            )
        else:
            await AntiCheat.update_paddle_position_and_direction(client_paddle_position,
                                                                 direction,
                                                                 player,
                                                                 sid)

    @staticmethod
    def _get_update_paddle_args(player_data) -> (bool, Optional[float], Optional[str]):
        """ Returns success, client_paddle_position, direction """
        try:
            client_paddle_position = player_data['client_paddle_position']
            if not isinstance(client_paddle_position, (float, int)):
                return False, None, None

            direction = player_data['direction']
            if direction not in ('up', 'down', 'none'):
                return False, None, None

            return (True,
                    float(client_paddle_position),
                    direction)

        except Exception:
            return False, None, None
