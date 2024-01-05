import random

import numpy


def vector_to_dict(vector: numpy.ndarray) -> dict:
    return {"x": vector[0], "y": vector[1], "z": vector[2]}


class PlayerObject(object):
    def __init__(self, x: float, y: float, z: float):
        self._position = numpy.array([x, y, z])
        self._move_direction = 0.

    def to_json(self) -> dict:
        return {
            "position": vector_to_dict(self._position),
            "move_direction": 0.
        }

    def set_movement(self, movement):
        self._move_direction = movement


class Board(object):
    def __init__(self, x: float, y: float, z: float):
        self._position = numpy.array([x, y, z])
        self._move_direction = numpy.array([0., 0., 0.])

    def to_json(self) -> dict:
        return {
            "position": vector_to_dict(self._position),
            "move_direction": vector_to_dict(self._move_direction)
        }


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
            "position": vector_to_dict(self._position),
            "move_direction": vector_to_dict(self._move_direction)
        }
