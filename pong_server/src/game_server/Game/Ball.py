import random

import numpy

import settings
from Game.CollisionHandler import CollisionHandler
from Game.Player.Paddle import Paddle
from vector_to_dict import vector_to_dict


class Ball(object):
    def __init__(self):
        self._position: numpy.ndarray = numpy.array([0.,
                                                     0.,
                                                     settings.BALL_RADIUS],
                                                    dtype=float)

        self._movement: numpy.ndarray = numpy.array([0., 0., 0.], dtype=float)
        self._set_random_movement()

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'movement': vector_to_dict(self._movement),
            'radius': settings.BALL_RADIUS,
            'acceleration': settings.BALL_ACCELERATION
        }

    def prepare_for_match(self):
        self._position[0] = 0.
        self._position[1] = 0.
        self._set_random_movement()

    def _set_random_movement(self):
        min_x = 7.
        max_x = 12.
        if random.randint(0, 1) == 0:
            self._movement[0] = random.uniform(-max_x, -min_x)
        else:
            self._movement[0] = random.uniform(min_x, max_x)

        min_y = 4.
        max_y = 5.
        if random.randint(0, 1) == 0:
            self._movement[1] = random.uniform(-max_y, -min_y)
        else:
            self._movement[1] = random.uniform(min_y, max_y)

    def get_movement(self) -> numpy.ndarray:
        return self._movement

    def set_movement_x(self, x: float):
        self._movement[0] = x

    def set_movement_y(self, y: float):
        self._movement[1] = y

    def set_position(self, position: numpy.ndarray):
        self._position[0] = position[0]
        self._position[1] = position[1]

    def get_position(self) -> numpy.ndarray:
        return self._position

    async def update(self,
                     match,
                     time_delta: float,
                     left_paddle: Paddle,
                     right_paddle: Paddle):
        if self._movement[0] == 0. or time_delta == 0.:
            return

        if self._movement[0] < 0.:
            collision_handler = CollisionHandler(left_paddle)
        else:
            collision_handler = CollisionHandler(right_paddle)
        await collision_handler.update_ball_position_and_movement(self, time_delta, match)
