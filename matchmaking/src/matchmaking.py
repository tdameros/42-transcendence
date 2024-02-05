import asyncio
import json
import logging
from time import time
from typing import Optional

from aiohttp import web
import socketio

import src.settings as settings

from .authenticate import authenticate_user
from .logging import setup_logging


class Matchmaking:

    def __init__(self):
        self.queue = []
        # TODO: change allowed origin to real client address
        # for now the allowed address is the test server
        self.sio = socketio.AsyncServer(
            cors_allowed_origins=['http://localhost:5000'],
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

    # TODO: Send proper match notification when game creation is implemented
    async def matchmaking(self) -> None:
        while True:
            for player in self.queue:
                opponent = self.search_opponent(player)
                if opponent is not None:
                    self.queue.remove(player)
                    self.queue.remove(opponent)
                    await self.send_match(player, opponent)
            await asyncio.sleep(2)

    def search_opponent(self, player: dict) -> Optional[dict]:
        match_found = False
        elo_threshold = self.get_elo_threshold(player)

        for opponent in self.queue:
            if opponent == player:
                continue
            if Matchmaking.elo_gap(player, opponent) < elo_threshold:
                if not match_found:
                    closest_opponent = opponent
                    match_found = True
                elif Matchmaking.elo_gap(player, opponent) < Matchmaking.elo_gap(player, closest_opponent):
                    closest_opponent = opponent
        return closest_opponent if match_found else None

    async def send_match(self, player1: dict, player2: dict) -> None:
        data = [
            {
                'user_id': player1.get('user_id'),
                'elo': player1.get('elo'),
            },
            {
                'user_id': player2.get('user_id'),
                'elo': player2.get('elo'),
            }
        ]
        data = json.dumps(data)
        await self.sio.emit('match', data, room=player1.get('sid'))
        await self.sio.emit('match', data, room=player2.get('sid'))

    @staticmethod
    def get_elo_threshold(player: dict) -> int:
        elapsed_time = time() - player.get('timestamp')
        queue_time = elapsed_time / settings.QUEUE_MAX_TIME
        queue_time = min(queue_time, 1)
        elo_threshold = settings.ELO_MAX_THRESHOLD * queue_time

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
        for user in self.queue:
            if user.get('sid') == sid:
                self.queue.remove(user)

    async def queue_info(self, sid, data):
        await self.sio.emit('queue_info', json.dumps(self.queue), room=sid)


if __name__ == '__main__':
    setup_logging()
    matchmaking = Matchmaking()
    matchmaking.start()
