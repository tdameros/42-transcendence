import logging
from typing import Optional

from AntiCheat import AntiCheat
from ClientManager import ClientManager
from common.src.jwt_managers import UserAccessJWTDecoder
from ConnectError import ConnectError
from EventEmitter import EventEmitter
from Game.GameManager import GameManager
from Server import Server


class EventHandler(object):
    @staticmethod
    def init():
        Server.sio.on('connect')(EventHandler._connect)
        Server.sio.on('disconnect')(EventHandler._disconnect)
        Server.sio.on('player_is_ready')(EventHandler._player_is_ready)
        Server.sio.on('update_paddle')(EventHandler._update_paddle)

    @staticmethod
    async def _connect(sid: str, _environ, auth):
        try:
            logging.info(f'{sid} connected')
            if Server.should_stop or GameManager.is_game_over():
                raise ConnectError('The game is over', 0)

            user_id: int = EventHandler._authenticate_user(auth)
            previous_sid = ClientManager.get_user_sid(user_id)
            if previous_sid:
                await Server.sio.disconnect(previous_sid)

            await ClientManager.add_newly_connected_user(user_id, sid)
            await EventEmitter.scene(sid,
                                     GameManager.get_player(user_id).get_location(),
                                     GameManager.get_scene(),
                                     GameManager.has_game_started())
        except ConnectError as e:
            logging.warning(f'{sid} failed to connect: {e.MESSAGE} (status {e.STATUS_CODE})')
            raise e.to_socket_io_exception()

    @staticmethod
    def _authenticate_user(auth: Optional[dict]) -> int:
        """ This is not an event handler, but it is used by `connect` """
        if auth is None:
            raise ConnectError('auth data missing', 400)
        if not isinstance(auth, dict):
            raise ConnectError('auth data should be a dictionary', 400)
        token = auth.get('token')
        if token is None:
            raise ConnectError('Token field is not present in auth data', 401)
        success, payload, error = UserAccessJWTDecoder.authenticate(token)
        if not success:
            raise ConnectError(f'Invalid token: {error}', 401)
        user_id: int = int(payload['user_id'])
        if user_id not in ClientManager.CLIENTS_IDS:
            raise ConnectError('You are not part of this game', 1)
        return user_id

    @staticmethod
    async def _disconnect(sid: str):
        await ClientManager.remove_disconnected_user(sid)

    @staticmethod
    async def _player_is_ready(sid: str, _data):
        ClientManager.add_ready_player(ClientManager.get_user_id(sid))

    @staticmethod
    async def _update_paddle(sid: str, player_data):
        if not GameManager.has_game_started() or GameManager.is_game_over():
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
        """ This is not an event handler, but it is used by `update_paddle`
            Returns success, client_paddle_position, direction """
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
