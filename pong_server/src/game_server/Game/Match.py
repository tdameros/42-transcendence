import time
from typing import Optional

import numpy

import settings
from EventEmitter import EventEmitter
from Game.Ball import Ball
from Game.MatchLocation import MatchLocation
from Game.MatchPositionCalculator import MatchPositionCalculator
from Game.Player.Player import Player
from PostSender.PostSender import PostSender
from vector_to_dict import vector_to_dict


class Match(object):
    GAME_ID: int  # Game ID is not the ID of the match, it is the ID of the game

    def __init__(self, game_id: int, match_location: MatchLocation):
        Match.GAME_ID = game_id

        self.LOCATION: MatchLocation = match_location
        self._points: list[int] = [0, 0]
        self._winner_index: Optional[int] = None

        self._position: numpy.ndarray = MatchPositionCalculator.get_position(match_location)

        self._players: list[Optional[Player]] = [None, None]

        self._ball: Ball = Ball()
        self._ball_is_waiting: bool = True
        self._ball_start_time: Optional[float] = None

    def to_json(self, should_include_players: bool = True) -> dict:
        if self._ball_start_time is None:
            ball_start_time = None
        else:
            ball_start_time = self._ball_start_time

        result: dict = {
            'location': self.LOCATION.to_json(),
            'position': vector_to_dict(self._position),
            'ball': self._ball.to_json(),
            'ball_is_waiting': self._ball_is_waiting,
            'ball_start_time': ball_start_time,
            'points': self._points,
        }
        if should_include_players:
            result['players'] = [player.to_json() if player else None
                                 for player in self._players]
        return result

    async def start_match(self):
        await self._prepare_ball_for_match()

    async def update(self, current_time: float, time_delta: float):
        if self._players[0]:
            self._players[0].update(time_delta)
        if self._players[1]:
            self._players[1].update(time_delta)

        if not self._ball_start_time:
            return

        if self._ball_is_waiting and current_time >= self._ball_start_time:
            self._ball_is_waiting = False
        if not self._ball_is_waiting:
            await self._ball.update(self,
                                    time_delta,
                                    self._players[0].get_paddle(),
                                    self._players[1].get_paddle())

    async def player_marked_point(self, player_index: int):
        self._points[player_index] += 1
        await PostSender.post_add_point(Match.GAME_ID, self._players[player_index].PLAYER_ID)

        if self._points[player_index] >= settings.POINTS_TO_WIN_MATCH:
            self._winner_index = player_index
            return

        await EventEmitter.player_scored_a_point(self._players[player_index].get_location())
        await self._prepare_ball_for_match()

    def is_full(self) -> bool:
        return self._players[0] is not None and self._players[1] is not None

    def is_over(self) -> bool:
        return self._winner_index is not None

    async def _prepare_ball_for_match(self):
        self._ball.prepare_for_match()
        self._ball_is_waiting = True
        self._ball_start_time = time.time() + settings.BALL_WAITING_TIME_SEC
        await EventEmitter.prepare_ball_for_match(self.LOCATION,
                                                  self._ball.get_movement(),
                                                  self._ball_start_time)

    def get_player(self, index: int) -> Optional[Player]:
        return self._players[index]

    def get_player_score(self, player_index: int) -> int:
        return self._points[player_index]

    def set_player(self, index: int, player: Player):
        self._players[index] = player

    def get_position(self) -> numpy.ndarray:
        return self._position

    def get_winner_index(self) -> Optional[int]:
        return self._winner_index
