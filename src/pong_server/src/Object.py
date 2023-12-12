import numpy
import random


def vector_to_dict(vector: numpy.ndarray) -> dict:
    return {"x": vector[0], "y": vector[1], "z": vector[2]}


class PlayerObject(object):
    def __init__(self, x: float, y: float, z: float):
        self.position = numpy.array([x, y, z])
        self.move_direction = numpy.array([0., 0., 0.])

    def to_json(self) -> dict:
        return {
            "position": vector_to_dict(self.position),
            "move_direction": vector_to_dict(self.move_direction)
        }


class Board(object):
    def __init__(self, x: float, y: float, z: float):
        self.position = numpy.array([x, y, z])
        self.move_direction = numpy.array([0., 0., 0.])

    def to_json(self) -> dict:
        return {
            "position": vector_to_dict(self.position),
            "move_direction": vector_to_dict(self.move_direction)
        }


class Ball(object):
    def __init__(self, x: float, y: float, z: float):
        self.position = numpy.array([x, y, z])
        if random.randint(0, 1) == 0:
            x = -2.
        else:
            x = 2.
        rand = random.randint(0, 2)
        if rand == 0:
            y = -.1
        elif rand == 1:
            y = .1
        else:
            y = 0.
        self.move_direction = numpy.array([x, y, 0.])

    def to_json(self) -> dict:
        return {
            "position": vector_to_dict(self.position),
            "move_direction": vector_to_dict(self.move_direction)
        }
