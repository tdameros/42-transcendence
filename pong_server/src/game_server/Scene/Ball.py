import random

import numpy

from src.game_server import settings
from src.game_server.vector_to_dict import vector_to_dict


class Ball(object):
    def __init__(self):
        self._position: numpy.ndarray = numpy.array([0.,
                                                     0.,
                                                     settings.BALL_RADIUS / 2.])

        x = -5.5 if random.randint(0, 1) == 0 else 5.5
        rand = random.randint(0, 2)
        if rand == 0:
            y = -2.8
        elif rand == 1:
            y = 2.8
        else:
            y = 0.
        self._movement: numpy.ndarray = numpy.array([x, y, 0.])

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'movement': vector_to_dict(self._movement),
            'radius': settings.BALL_RADIUS
        }

    def update_position(self, time_delta: float):
        self._position += self._movement * time_delta
