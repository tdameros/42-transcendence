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
        # Storing player id for communication with matchmaking / tournament server
        self.PLAYER_ID: int = player_id
        self._player_location: PlayerLocation = player_location

        sign = 1. if is_player_on_the_right else -1.
        self._position: numpy.ndarray = numpy.array([settings.BOARD_SIZE[0] / 2. * sign,
                                                     0.,
                                                     0.],
                                                    dtype=float)
        self._paddle: Paddle = Paddle(numpy.array([settings.PADDLE_X_POSITION * sign,
                                                   0.,
                                                   settings.PADDLE_SIZE[2] / 2. + 0.001],
                                                  dtype=float),
                                      self._position)
        self._board: _Board = _Board()

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'move_speed': settings.PLAYER_MOVE_SPEED,
            'board': self._board.to_json(),
            'paddle': self._paddle.to_json()
        }

    def update(self, time_delta: float):
        self._paddle.update(time_delta)
        self._board.update(time_delta)

    def get_location(self) -> PlayerLocation:
        return self._player_location

    def set_location(self, player_location: PlayerLocation):
        if self._player_location.player_index != player_location.player_index:
            self._position[0] *= -1
            self._paddle.set_paddle_is_on_the_right(bool(player_location.player_index))
        self._player_location = player_location

    def get_position(self) -> numpy.ndarray:
        return self._position

    def set_position(self, position: numpy.ndarray):
        self._position = position.copy()

    def get_paddle(self):
        return self._paddle
