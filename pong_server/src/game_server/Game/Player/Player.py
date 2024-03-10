from typing import Optional

import numpy

import settings
from Game.Player._Board import _Board
from Game.Player.Paddle import Paddle
from Game.PlayerLocation import PlayerLocation
from vector_to_dict import vector_to_dict


class Player(object):

    def __init__(self,
                 player_id: int,
                 player_location: PlayerLocation,
                 is_player_on_the_right: bool):
        self.PLAYER_ID: int = player_id
        self._player_location: PlayerLocation = player_location
        self._is_animating: bool = False
        self._animation_start_time: float = 0.
        self._animation_end_time: float = 0.
        self._is_changing_side: bool = False
        self._index_when_lost_match: Optional[int] = None

        sign = 1. if is_player_on_the_right else -1.
        self._position: numpy.ndarray = numpy.array([settings.BOARD_SIZE[0] / 2. * sign,
                                                     0.,
                                                     0.],
                                                    dtype=float)
        self._destination: numpy.ndarray = self._position.copy()
        self._paddle: Paddle = Paddle(numpy.array([settings.PADDLE_X_POSITION * sign,
                                                   0.,
                                                   settings.PADDLE_SIZE[2] / 2. + 0.001],
                                                  dtype=float),
                                      self)
        self._board: _Board = _Board()

    def to_json(self) -> dict:
        result = {
            'position': vector_to_dict(self._position),
            'board': self._board.to_json(),
            'paddle': self._paddle.to_json()
        }
        if self._index_when_lost_match is not None:
            result['index_when_lost_match'] = self._index_when_lost_match
        else:
            result['destination'] = vector_to_dict(self._destination)
            result['is_animating'] = self._is_animating
            result['animation_start_time'] = self._animation_start_time
            result['animation_end_time'] = self._animation_end_time
            result['is_changing_side'] = self._is_changing_side
        return result

    def update(self, time_delta: float):
        self._paddle.update(time_delta)
        self._board.update(time_delta)

    def animate(self, current_time: float):
        if not self._is_animating:
            return False
        if current_time >= self._animation_end_time:
            self._position = self._destination.copy()
            if self._is_changing_side:
                self._paddle.change_side()
            self._is_animating = False
        return self._is_animating

    def start_animation(self,
                        current_time: float,
                        is_changing_side: bool,
                        finished_match,
                        new_match):
        self._is_changing_side = is_changing_side
        self._destination = self._position.copy()
        if self._is_changing_side:
            self._destination[0] *= -1
        self._position += finished_match.get_position() - new_match.get_position()
        self._is_animating = True
        self._animation_start_time = current_time
        self._animation_end_time = current_time + settings.ANIMATION_DURATION

        self._paddle.set_y_position(0.)

    def get_location(self) -> PlayerLocation:
        return self._player_location

    def set_location(self, player_location: PlayerLocation):
        self._player_location = player_location

    def get_position(self) -> numpy.ndarray:
        return self._position

    def set_position(self, position: numpy.ndarray):
        self._position = position.copy()

    def get_paddle(self):
        return self._paddle

    def set_index_when_lost_match(self, index: int):
        self._index_when_lost_match = index

    def is_animating(self) -> bool:
        return self._is_animating
