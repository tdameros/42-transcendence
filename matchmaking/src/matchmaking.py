import asyncio
import json
import logging
from time import time
from typing import Optional, Any

import socketio
import requests
from aiohttp import web

import src.settings as settings
import src.error_message as error
import common.src.settings as common_settings
from common.src.internal_requests import InternalRequests

from .authenticate import authenticate_user
from .logging import setup_logging


class Matchmaking:

    def __init__(self):
        self.queue = []
        self.player_to_remove = []
        self.found_matches = []
        self.sio = socketio.AsyncServer(
            cors_allowed_origins='*',
            logger=False,
            engineio_logger=False,
        )
        self.app = web.Application()
        self.sio.attach(self.app)
        self.sio.on('connect')(self.connect)
        self.sio.on('disconnect')(self.disconnect)
        self.sio.on('queue_info')(self.queue_info)
        self.app.on_startup.append(self.start_matchmaking)

    def start(self) -> None:
        web.run_app(self.app, host=settings.MATCHMAKING_HOST, port=settings.MATCHMAKING_PORT)

    async def matchmaking(self) -> None:
        while True:
            for index, player in enumerate(self.queue):
                opponent = self.search_opponent(player, index)
                if opponent is not None:
                    self.found_matches.append((player, opponent))
            for player, opponent in self.found_matches:
                    await self.find_match(player, opponent)
            self.found_matches = []
            for player in self.player_to_remove:
                logging.debug(f'Player removed from the queue: {player}')
                await self.sio.disconnect(player['sid'])
            self.player_to_remove = []
            await asyncio.sleep(2)

    def search_opponent(self, player: dict, index: int) -> Optional[dict]:
        if len(self.queue) - 1 == index:
            return None
        match_found = False
        elo_threshold = self.get_elo_threshold(player)
        for opponent in self.queue[index + 1:]:
            if Matchmaking.elo_gap(player, opponent) < elo_threshold:
                if not match_found:
                    closest_opponent = opponent
                    match_found = True
                elif Matchmaking.elo_gap(player, opponent) < Matchmaking.elo_gap(player, closest_opponent):
                    closest_opponent = opponent
        return closest_opponent if match_found else None

    async def find_match(self, player_1: dict, player_2: dict) -> None:
        logging.debug(f'find_match: {player_1.get("user_id")} vs {player_2.get("user_id")}')
        data = {
            'request_issuer': 'matchmaking',
            'game_id': 0,
            'players': [
                player_1.get('user_id'),
                player_2.get('user_id'),
            ]
        }
        try:
            response = InternalRequests.post(
                f'{common_settings.GAME_CREATOR_CREATE_GAME_ENDPOINT}',
                data=json.dumps(data),
            )
        except requests.exceptions.RequestException as e:
            logging.debug(e)
            await self.disconnect_player(player_1, player_2, error.GAME_CREATOR_CONNECT_ERROR)
            return
        if not response.ok:
            logging.debug(f'response: {response.text}')
            if response.status_code != 503:
                await self.disconnect_player(player_1, player_2, error.GAME_CREATOR_CREATE_GAME_ERROR)
            return
        self.player_to_remove.append(player_1)
        self.player_to_remove.append(player_2)
        await self.send_match_uri(player_1, player_2, response.json())

    async def send_match_uri(self, player1: dict, player2: dict, data: Any) -> None:
        data = json.dumps(data)
        await self.sio.emit('match', data, room=player1.get('sid'))
        await self.sio.emit('match', data, room=player2.get('sid'))

    async def disconnect_player(self, player_1: dict, player_2: dict, error_message: str):
        logging.debug('disconnect_player')
        await self.send_error(player_1, error_message)
        await self.send_error(player_2, error_message)
        self.player_to_remove.append(player_1)
        self.player_to_remove.append(player_2)

    async def send_error(self, player: dict, error_message: str) -> None:
        logging.debug('send_error')
        data = {'error': error_message}
        await self.sio.emit('error', data, room=player.get('sid'))


    @staticmethod
    def get_elo_threshold(player: dict) -> int:
        elapsed_time = time() - player.get('timestamp')
        threshold_factor = elapsed_time / settings.THRESHOLD_TIME
        elo_threshold = settings.ELO_THRESHOLD * threshold_factor

        return elo_threshold

    @staticmethod
    def elo_gap(player1: dict, player2: dict) -> int:
        return abs(player1.get('elo') - player2.get('elo'))

    async def start_matchmaking(self, app: web.Application) -> None:
        self.sio.start_background_task(self.matchmaking)

    async def connect(self, sid, environ, auth):
        logging.debug(f'New connection: {sid}')
        user, errors = authenticate_user(auth)
        if user is None:
            logging.debug(str(errors))
            raise socketio.exceptions.ConnectionRefusedError(str(errors))
        player = {
            'sid': sid,
            'user_id': user['id'],
            'elo': user['elo'],
            'timestamp': time(),
        }
        self.queue.append(player)
        logging.debug(f'User added to the queue: {user}')
        return True

    def disconnect(self, sid):
        logging.debug('disconnect')
        for user in self.queue:
            if user.get('sid') == sid:
                self.queue.remove(user)
                break

    async def queue_info(self, sid, data):
        await self.sio.emit('queue_info', json.dumps(self.queue), room=sid)


if __name__ == '__main__':
    setup_logging()
    matchmaking = Matchmaking()
    matchmaking.start()
