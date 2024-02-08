import time
from typing import Optional

import numpy
import socketio

import rooms
import settings
from Scene.Ball import Ball
from Scene.Player.Player import Player
from shared_code.emit import emit
from vector_to_dict import vector_to_dict


class Match(object):
    def __init__(self, position: numpy.ndarray, match_index: int):
        self.MATCH_INDEX = match_index
        self._position = position.copy()

        self._players: list[Player] = [Player(is_player_on_the_right=False),
                                       Player(is_player_on_the_right=True)]

        self._points: list[int] = [0, 0]

        self._ball: Ball = Ball()
        self._ball_is_waiting: bool = True
        self._ball_start_time: Optional[float] = None

    def to_json(self) -> dict:
        if self._ball_start_time is None:
            ball_start_time = None
        else:
            ball_start_time = self._ball_start_time

        return {
            'position': vector_to_dict(self._position),
            'players': [player.to_json() for player in self._players],
            'ball': self._ball.to_json(),
            'ball_is_waiting': self._ball_is_waiting,
            'ball_start_time': ball_start_time,
        }

    def get_index(self) -> int:
        return self.MATCH_INDEX

    async def start_game(self, sio: socketio.AsyncServer):
        await self.prepare_ball_for_match(sio)

    async def update(self, sio: socketio.AsyncServer, time_delta: float, current_time: float):
        self._players[0].update(time_delta)
        self._players[1].update(time_delta)

        if self._ball_is_waiting and current_time >= self._ball_start_time:
            self._ball_is_waiting = False
        if not self._ball_is_waiting:
            await self._ball.update(sio,
                                    time_delta,
                                    self._players[0].get_paddle(),
                                    self._players[1].get_paddle(),
                                    self)

    async def player_marked_point(self, sio: socketio.AsyncServer, player_index: int):
        self._points[player_index] += 1

        if self._points[player_index] >= settings.POINTS_TO_WIN:
            await self._finish_match(sio, player_index)
            return

        await self.prepare_ball_for_match(sio)

        # TODO send point update to tournament / matchmaking

    async def _finish_match(self, sio: socketio.AsyncServer, winner_index: int):
        await self.prepare_ball_for_match(sio)  # TODO delete this once this
        #                                              function is implemented

        # TODO send match finish to tournament / matchmaking

    async def prepare_ball_for_match(self, sio: socketio.AsyncServer):
        self._ball.prepare_for_match()
        self._ball_is_waiting = True
        self._ball_start_time = time.time() + settings.BALL_WAITING_TIME_SEC
        await emit(sio, 'prepare_ball_for_match', rooms.ALL_PLAYERS, {
            'match_index': self.MATCH_INDEX,
            'ball_start_time': self._ball_start_time,
            'ball_movement': vector_to_dict(self._ball.get_movement()),
        })

    def get_player(self, index: int) -> Player:
        return self._players[index]
