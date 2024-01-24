import numpy

from src.game_server import settings
from src.game_server.vector_to_dict import vector_to_dict


class _Paddle(object):
    def __init__(self, position: numpy.ndarray):
        self._position: numpy.ndarray = position.copy()
        self._movement: numpy.ndarray = numpy.array([0., 0., 0.])

    def to_json(self) -> dict:
        return {
            'size': vector_to_dict(settings.PADDLE_SIZE),
            'position': vector_to_dict(self._position),
            'movement': vector_to_dict(self._movement),
            'move_speed': settings.PADDLE_MOVE_SPEED
        }

    def update_position(self, time_delta: float):
        self._position += self._movement * time_delta

    def set_direction(self, direction: str):
        if direction == 'up':
            self._movement[1] = settings.PADDLE_MOVE_SPEED
        elif direction == 'down':
            self._movement[1] = -settings.PADDLE_MOVE_SPEED
        else:
            self._movement[1] = 0.

    def get_movement(self) -> numpy.ndarray:
        return self._movement

    def set_position(self, position: numpy.ndarray):
        self._position = position.copy()

    def get_position(self):
        return self._position
