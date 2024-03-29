import numpy

import settings
from Segment2 import Segment2
from vector_to_dict import vector_to_dict


class Paddle(object):
    def __init__(self, position: numpy.ndarray, player):
        self._position: numpy.ndarray = position.copy()
        self._movement: numpy.ndarray = numpy.array([0., 0., 0.], dtype=float)

        self._paddle_is_on_the_right: bool = self._position[0] > 0.

        self._player = player

        self._set_collision_segments()

    def to_json(self) -> dict:
        return {
            'size': vector_to_dict(settings.PADDLE_SIZE),
            'position': vector_to_dict(self._position),
            'movement': vector_to_dict(self._movement),
            'move_speed': settings.PADDLE_MOVE_SPEED
        }

    def update(self, time_delta: float):
        self._position += self._movement * time_delta

        if self._position[1] <= settings.PADDLE_BOUNDING_BOX.get_y_min():
            self._position[1] = settings.PADDLE_BOUNDING_BOX.get_y_min()
        elif self._position[1] >= settings.PADDLE_BOUNDING_BOX.get_y_max():
            self._position[1] = settings.PADDLE_BOUNDING_BOX.get_y_max()

        self._set_collision_segments()

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

        self._set_collision_segments()

    def set_y_position(self, y: float):
        self._position[1] = y

        self._set_collision_segments()

    def get_position(self):
        return self._position

    def get_top_collision_segment(self) -> Segment2:
        return self._top_collision_segment

    def get_front_collision_segment(self) -> Segment2:
        return self._front_collision_segment

    def get_bottom_collision_segment(self) -> Segment2:
        return self._bottom_collision_segment

    def is_paddle_on_the_right(self) -> bool:
        return self._paddle_is_on_the_right

    def change_side(self):
        self._position[0] *= -1
        self._paddle_is_on_the_right = not self._paddle_is_on_the_right

    def _set_collision_segments(self):
        player_position = self._player.get_position()
        x_left = (player_position[0] + self._position[0]
                  - settings.PADDLE_SIZE[0] * 0.5)
        x_right = (player_position[0] + self._position[0]
                   + settings.PADDLE_SIZE[0] * 0.5)

        y_top = (player_position[1] + self._position[1]
                 + settings.PADDLE_SIZE[1] * 0.5)
        y_bottom = (player_position[1] + self._position[1]
                    - settings.PADDLE_SIZE[1] * 0.5)

        top_left = numpy.array([x_left, y_top], dtype=float)
        top_right = numpy.array([x_right, y_top], dtype=float)
        bottom_right = numpy.array([x_right, y_bottom], dtype=float)
        bottom_left = numpy.array([x_left, y_bottom], dtype=float)

        self._top_collision_segment: Segment2 = Segment2(top_left, top_right)
        self._bottom_collision_segment: Segment2 = Segment2(bottom_left, bottom_right)
        if self._paddle_is_on_the_right:
            self._front_collision_segment: Segment2 = Segment2(bottom_left, top_left)
        else:
            self._front_collision_segment: Segment2 = Segment2(bottom_right, top_right)
