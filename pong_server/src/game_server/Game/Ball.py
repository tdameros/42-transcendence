import random
import sys
from typing import Optional

import numpy

import settings
from EventEmitter import EventEmitter
from Game.Player.Paddle import Paddle
from Segment2 import Segment2
from vector_to_dict import vector_to_dict


class Ball(object):
    def __init__(self):
        self._position: numpy.ndarray = numpy.array([0.,
                                                     0.,
                                                     settings.BALL_RADIUS])

        self._movement: numpy.ndarray = numpy.array([0., 0., 0.])
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

    async def update(self,
                     match,
                     time_delta: float,
                     left_paddle: Paddle,
                     right_paddle: Paddle):
        if self._movement[0] == 0.:
            return

        previous_position: numpy.ndarray = numpy.array([self._position[0],
                                                        self._position[1]])
        radius_compensator = (self._movement / numpy.linalg.norm(self._movement)
                              * (settings.BALL_RADIUS / 2.))
        self._position += self._movement * time_delta + radius_compensator

        travel: Segment2 = Segment2(previous_position, self._position)

        should_emit_update_ball, should_fix_position = await self._handle_collisions(
            match,
            travel,
            left_paddle if self._movement[0] < 0. else right_paddle,
            time_delta,
        )

        if should_fix_position:
            self._position -= radius_compensator
        if should_emit_update_ball:
            await EventEmitter.update_ball(match.LOCATION, self._position, self._movement)

    async def _handle_collisions(self,
                                 match,
                                 travel: Segment2,
                                 paddle: Paddle,
                                 time_delta: float) -> (bool, bool):
        """ Returns (should_emit_update_ball: bool, should_fix_position: bool) """

        (collision_detected, should_emit_update_ball) = await self._handle_paddle_collision(
            travel, paddle, time_delta
        )
        if collision_detected:
            return should_emit_update_ball, True

        if await self._handle_match_point(match):
            return False, False

        self._handle_board_collision()
        return False, True

    async def _handle_paddle_collision(self,
                                       travel: Segment2,
                                       paddle: Paddle,
                                       time_delta: float) -> (bool, bool):
        """ Returns (collision_detected: bool, should_emit_update_ball: bool) """

        top_intersection, top_t = travel.intersect(paddle.get_top_collision_segment())
        front_intersection, front_t = travel.intersect(paddle.get_front_collision_segment())
        bottom_intersection, bottom_t = travel.intersect(paddle.get_bottom_collision_segment())

        (closest_intersection,
         closest_intersection_t,
         axe_to_change,
         y_direction) = self._get_closest_intersection(top_intersection, top_t,
                                                       front_intersection,
                                                       front_t,
                                                       bottom_intersection,
                                                       bottom_t)
        if closest_intersection is None:
            return False, None

        self._position = numpy.array([closest_intersection[0],
                                      closest_intersection[1],
                                      self._position[2]])
        if axe_to_change == 'x':
            self._movement[0] = -self._movement[0] * settings.BALL_ACCELERATION
        elif ((y_direction == '+' and self._movement[1] < 0.)
              or (y_direction == '-' and self._movement[1] > 0.)):
            self._movement[1] = -self._movement[1] * settings.BALL_ACCELERATION
        self._position += self._movement * (time_delta * (1. - closest_intersection_t))

        if axe_to_change == 'x':
            return True, True
        return True, False

    async def _handle_match_point(self, match) -> bool:
        if self._position[0] <= settings.BALL_BOUNDING_BOX.get_x_min():
            await match.player_marked_point(1)
            return True
        elif self._position[0] >= settings.BALL_BOUNDING_BOX.get_x_max():
            await match.player_marked_point(0)
            return True
        return False

    def _handle_board_collision(self):
        if self._position[1] < settings.BALL_BOUNDING_BOX.get_y_min():
            opposite_movement = ((settings.BALL_BOUNDING_BOX.get_y_min() - self._position[1])
                                 * settings.BALL_ACCELERATION)
            self._position[1] = settings.BALL_BOUNDING_BOX.get_y_min() + opposite_movement

            self._movement[1] = -self._movement[1] * settings.BALL_ACCELERATION

        elif self._position[1] > settings.BALL_BOUNDING_BOX.get_y_max():
            opposite_movement = ((settings.BALL_BOUNDING_BOX.get_y_max() - self._position[1])
                                 * settings.BALL_ACCELERATION)
            self._position[1] = settings.BALL_BOUNDING_BOX.get_y_max() + opposite_movement

            self._movement[1] = -self._movement[1] * settings.BALL_ACCELERATION

    @staticmethod
    def _get_closest_intersection(top_intersection: Optional[numpy.ndarray],
                                  top_t: Optional[float],
                                  front_intersection: Optional[numpy.ndarray],
                                  front_t: Optional[float],
                                  bottom_intersection: Optional[numpy.ndarray],
                                  bottom_t: Optional[float]):
        closest_intersection = None
        closest_t = sys.float_info.max
        axe_to_change = None
        y_direction = None

        if top_intersection is not None:
            closest_intersection = top_intersection
            closest_t = top_t
            axe_to_change = 'y'
            y_direction = '+'

        if front_intersection is not None:
            if front_t < closest_t:
                closest_intersection = front_intersection
                closest_t = front_t
                axe_to_change = 'x'

        if bottom_intersection is not None:
            if bottom_t < closest_t:
                return (bottom_intersection,
                        closest_t,
                        'y',
                        '-')

        return (closest_intersection,
                closest_t,
                axe_to_change,
                y_direction)
