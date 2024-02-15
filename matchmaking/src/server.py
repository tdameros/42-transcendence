import json
import logging
from typing import Any

import requests
import socketio
from aiohttp import web

import common.src.settings as common_settings
import src.error_message as error
import src.settings as settings
from common.src.internal_requests import InternalRequests

from .authenticate import authenticate_user
from .matchmaking import Matchmaking
from .player import Player


class Server:
    def __init__(self):
        self.sio = socketio.AsyncServer(
            cors_allowed_origins='*',
            logger=False,
            engineio_logger=False,
        )
        self.app = web.Application()
        self.matchmaking = Matchmaking(self)
        self.sio.attach(self.app)
        self.sio.on('connect')(self.connect)
        self.sio.on('disconnect')(self.disconnect)
        self.app.on_startup.append(self.start_matchmaking)

    def start(self) -> None:
        web.run_app(self.app, host=settings.MATCHMAKING_HOST, port=settings.MATCHMAKING_PORT)

    async def connect(self, sid, environ, auth):
        logging.debug(f'New connection: {sid}')
        user, errors = authenticate_user(auth)
        if user is None:
            logging.debug(str(errors))
            raise socketio.exceptions.ConnectionRefusedError(str(errors))
        player = Player(sid, user['id'], user['elo'])
        self.matchmaking.add_player(player)
        logging.debug(f'User added to the queue: {user}')
        return True

    def disconnect(self, sid):
        logging.debug(f'Disconnect: {sid}')
        self.matchmaking.remove_player(sid)

    async def send_match_uri(self, player1: Player, player2: Player, data: Any) -> None:
        data = json.dumps(data)
        await self.sio.emit('match', data, room=player1.sid)
        await self.sio.emit('match', data, room=player2.sid)

    async def send_error(self, player_1: Player, player_2: Player, error_message: str) -> None:
        data = {'error': error_message}
        await self.sio.emit('error', data, room=player_1.sid)
        await self.sio.emit('error', data, room=player_2.sid)

    async def send_match(self, player_1: Player, player_2: Player) -> None:
        data = {
            'request_issuer': 'matchmaking',
            'game_id': 0,
            'players': [
                player_1.user_id,
                player_2.user_id,
            ]
        }
        try:
            response = InternalRequests.post(
                common_settings.GAME_CREATOR_CREATE_GAME_ENDPOINT,
                data=json.dumps(data),
            )
        except requests.exceptions.RequestException as e:
            logging.debug(e)
            await self.disconnect_players(player_1, player_2, error.GAME_CREATOR_CONNECT_ERROR)
            return
        if not response.ok:
            logging.debug(f'Request failed: {response.text}')
            if response.status_code != 503:
                await self.disconnect_players(player_1, player_2, error.GAME_CREATOR_CREATE_GAME_ERROR)
            return
        await self.send_match_uri(player_1, player_2, response.json())
        await self.remove_players(player_1, player_2)

    async def disconnect_players(self, player_1: Player, player_2: Player, error_message: str) -> None:
        await self.send_error(player_1, player_2, error_message)
        await self.remove_players(player_1, player_2)

    async def remove_players(self, player_1: Player, player_2: Player):
        self.matchmaking.remove_player(player_1.sid)
        self.matchmaking.remove_player(player_2.sid)
        await self.sio.disconnect(player_1.sid)
        await self.sio.disconnect(player_2.sid)

    async def start_matchmaking(self, app: web.Application) -> None:
        self.sio.start_background_task(self.matchmaking.routine)
