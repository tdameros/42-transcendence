import time
from typing import Optional

import numpy

import settings
from EventEmitter import EventEmitter
from Game.Ball import Ball
from Game.MatchLocation import MatchLocation
from Game.Player.Player import Player
from vector_to_dict import vector_to_dict


class _MatchPositionFinder(object):
    # This is a cache to avoid calculating the same position multiple times
    match_positions: dict[MatchLocation, numpy.ndarray] = {}

    @staticmethod
    def get_position(match_location: MatchLocation) -> numpy.ndarray:
        match_position = _MatchPositionFinder.match_positions.get(match_location)
        if match_position:
            return match_position.copy()

        if match_location.game_round == 0:
            x: float = (match_location.game_round * settings.MATCH_SIZE[0]
                        + match_location.game_round * settings.MATCHES_X_OFFSET)
            match_position = numpy.array([x, 0., 0.])
        else:
            match_below_left: MatchLocation = MatchLocation(match_location.game_round - 1,
                                                            match_location.match * 2)
            match_below_right: MatchLocation = MatchLocation(match_below_left.game_round,
                                                             match_below_left.match + 1)
            x: float = ((_MatchPositionFinder._get_x_position(match_below_left)
                         + _MatchPositionFinder._get_x_position(match_below_right))
                        / 2)
            y: float = (match_location.game_round * settings.MATCH_SIZE[1]
                        + match_location.game_round * settings.MATCHES_Y_OFFSET)
            match_position = numpy.array([x, y, 0.])

        _MatchPositionFinder.match_positions[match_location] = match_position
        return match_position.copy()

    @staticmethod
    def _get_x_position(match_location: MatchLocation) -> float:
        match_position = _MatchPositionFinder.match_positions.get(match_location)
        if match_position:
            return match_position[0]
        return _MatchPositionFinder.get_position(match_location)[0]


class Match(object):
    def __init__(self, match_location: MatchLocation):
        self.LOCATION: MatchLocation = match_location
        self._points: list[int] = [0, 0]

        self._position: numpy.ndarray = _MatchPositionFinder.get_position(match_location)

        self._players: list[Optional[Player]] = [None, None]

        self._ball: Ball = Ball()
        self._ball_is_waiting: bool = True
        self._ball_start_time: Optional[float] = None

    def to_json(self) -> dict:
        if self._ball_start_time is None:
            ball_start_time = None
        else:
            ball_start_time = self._ball_start_time

        return {
            'location': self.LOCATION.to_json(),
            'position': vector_to_dict(self._position),
            'players': [player.to_json() if player else None for player in self._players],
            'ball': self._ball.to_json(),
            'ball_is_waiting': self._ball_is_waiting,
            'ball_start_time': ball_start_time,
        }

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
        # TODO Send point update to tournament / matchmaking

        if self._points[player_index] >= settings.POINTS_TO_WIN_MATCH:
            await self._finish_match(player_index)
            return

        await self._prepare_ball_for_match()

    async def _finish_match(self, winner_index: int):
        await self._prepare_ball_for_match()  # TODO Remove this line once the
        #                                       function is implemented

        pass
        # TODO Tell the GameManager that the match is finished
        # TODO Send match finish to tournament / matchmaking

    async def _prepare_ball_for_match(self):
        self._ball.prepare_for_match()
        self._ball_is_waiting = True
        self._ball_start_time = time.time() + settings.BALL_WAITING_TIME_SEC
        await EventEmitter.prepare_ball_for_match(self.LOCATION,
                                                  self._ball.get_movement(),
                                                  self._ball_start_time)

    def get_player(self, index: int) -> Optional[Player]:
        return self._players[index]

    def set_player(self, index: int, player: Player):
        self._players[index] = player

    def get_position(self) -> numpy.ndarray:
        return self._position
