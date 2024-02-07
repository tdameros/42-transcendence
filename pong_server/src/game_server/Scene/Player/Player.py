import numpy

import settings
from Scene.Player._Board import _Board
from Scene.Player.Paddle import Paddle
from vector_to_dict import vector_to_dict


class Player(object):

    def __init__(self,
                 is_player_on_the_right: bool):
        sign = 1. if is_player_on_the_right else -1.
        self._position: numpy.ndarray = numpy.array([settings.BOARD_SIZE[0] / 2. * sign,
                                                     0.,
                                                     0.])
        self._paddle: Paddle = Paddle(numpy.array([settings.PADDLE_X_POSITION * sign,
                                                   0.,
                                                   settings.PADDLE_SIZE[2] / 2.]),
                                      self._position)
        self._board: _Board = _Board()

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'move_speed': settings.PLAYER_MOVE_SPEED,
            'board': self._board.to_json(),
            'paddle': self._paddle.to_json()
        }

    def update_position(self, time_delta: float):
        self._paddle.update_position(time_delta)
        self._board.update_position(time_delta)

    def set_paddle_direction(self, direction: str):
        self._paddle.set_direction(direction)

    def get_paddle_movement(self) -> numpy.ndarray:
        return self._paddle.get_movement()

    def set_paddle_position(self, position: numpy.ndarray):
        self._paddle.set_position(position)

    def get_paddle_position(self):
        return self._paddle.get_position()

    def get_paddle(self):
        return self._paddle
