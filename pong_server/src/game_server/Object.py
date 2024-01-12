import random

import numpy

from src.game_server import settings
from src.game_server.vector_to_dict import vector_to_dict


class Player(object):
    def __init__(self, x: float, y: float, z: float):
        self._position = numpy.array([x, y, z])
        self._move_direction = 0.

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'move_direction': 0.
        }

    def set_movement(self, movement):
        if movement == 'up':
            self._move_direction = settings.PLAYER_MOVE_SPEED
        elif movement == 'down':
            self._move_direction = -settings.PLAYER_MOVE_SPEED
        else:
            self._move_direction = 0.

    def get_movement(self):
        return self._move_direction

    def update_position(self, time_delta: float):
        self._position += self._move_direction * time_delta

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position


class Board(object):
    def __init__(self, x: float, y: float, z: float):
        self._position = numpy.array([x, y, z])
        self._move_direction = numpy.array([0., 0., 0.])

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'move_direction': vector_to_dict(self._move_direction)
        }

    def update_position(self, time_delta: float):
        self._position += self._move_direction * time_delta


class Ball(object):
    def __init__(self, x: float, y: float, z: float):
        self._position = numpy.array([x, y, z])
        if random.randint(0, 1) == 0:
            x = -5.5
        else:
            x = 5.5
        rand = random.randint(0, 2)
        if rand == 0:
            y = -2.8
        elif rand == 1:
            y = 2.8
        else:
            y = 0.
        self._move_direction = numpy.array([x, y, 0.])

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'move_direction': vector_to_dict(self._move_direction)
        }

    def update_position(self, time_delta: float):
        self._position += self._move_direction * time_delta
