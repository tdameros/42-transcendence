import abc
from typing import Optional

import numpy

import settings
from EventEmitter import EventEmitter
from Game.Player.Paddle import Paddle
from Segment2 import Segment2


class _APhysicalObject(abc.ABC):
    def __init__(self):
        self.intersection: numpy.array = None
        self.t: float = None
        pass

    @abc.abstractmethod
    def intersect(self,
                  _travel: Segment2,
                  _current_closest_physical_object_hit: Optional['_APhysicalObject']
                  ) -> Optional['_APhysicalObject']:
        pass

    @abc.abstractmethod
    async def handle_collision(self,
                               _travel: Segment2,
                               _ball,
                               _collision_handler: 'CollisionHandler',
                               _match_location) -> Optional[Segment2]:
        pass


class _Wall(_APhysicalObject):
    def __init__(self, is_top: bool):
        super().__init__()
        self.is_top: bool = is_top
        if self.is_top:
            self.y: float = settings.BOARD_SIZE[1] * 0.5
        else:
            self.y: float = settings.BOARD_SIZE[1] * -0.5

    def intersect(self,
                  travel: Segment2,
                  current_closest_physical_object_hit: Optional[_APhysicalObject]
                  ) -> Optional[_APhysicalObject]:
        if self.is_top:
            travel_top = travel.end[1] + settings.BALL_RADIUS
            if travel_top < self.y:
                return current_closest_physical_object_hit
            self.intersection = ((travel.vector / travel.vector[1]
                                 * (self.y - travel.begin[1] - settings.BALL_RADIUS))
                                 + travel.begin)
        else:
            travel_bottom = travel.end[1] - settings.BALL_RADIUS
            if travel_bottom > self.y:
                return current_closest_physical_object_hit
            self.intersection = ((travel.vector / travel.vector[1]
                                 * (self.y - travel.begin[1] + settings.BALL_RADIUS))
                                 + travel.begin)

        self.t = (self.intersection[0] - travel.begin[0]) / travel.vector[0]

        if current_closest_physical_object_hit is None:
            return self
        if self.t < current_closest_physical_object_hit.t:
            return self
        return current_closest_physical_object_hit

    async def handle_collision(self,
                               travel: Segment2,
                               ball,
                               collision_handler: 'CollisionHandler',
                               _match_location) -> Optional[Segment2]:
        ball.set_movement_y(ball.get_movement()[1] * -settings.BALL_ACCELERATION)
        new_travel_vector = travel.vector * (1 - self.t)
        new_travel_vector[1] *= -settings.BALL_ACCELERATION
        return Segment2(self.intersection,
                        self.intersection + new_travel_vector,
                        new_travel_vector)


class _Goal(_APhysicalObject):
    def __init__(self, is_right: bool):
        super().__init__()
        self.is_right: bool = is_right
        if self.is_right:
            self.x: float = settings.BOARD_SIZE[0]
        else:
            self.x: float = -settings.BOARD_SIZE[0]

    def intersect(self,
                  travel: Segment2,
                  current_closest_physical_object_hit: Optional[_APhysicalObject]
                  ) -> Optional[_APhysicalObject]:
        if self.is_right:
            travel_right = travel.end[0] + settings.BALL_RADIUS
            if travel_right < self.x:
                return current_closest_physical_object_hit
            self.intersection = ((travel.vector / travel.vector[0]
                                 * (self.x - travel.begin[0] - settings.BALL_RADIUS))
                                 + travel.begin)
        else:
            travel_left = travel.end[0] - settings.BALL_RADIUS
            if travel_left > self.x:
                return current_closest_physical_object_hit
            self.intersection = ((travel.vector / travel.vector[0]
                                 * (self.x - travel.begin[0] + settings.BALL_RADIUS))
                                 + travel.begin)

        self.t = (self.intersection[0] - travel.begin[0]) / travel.vector[0]

        if current_closest_physical_object_hit is None:
            return self
        if self.t < current_closest_physical_object_hit.t:
            return self
        return current_closest_physical_object_hit

    async def handle_collision(self,
                               _travel: Segment2,
                               _ball,
                               _collision_handler: 'CollisionHandler',
                               match) -> Optional[Segment2]:
        await match.player_marked_point(1 - int(self.is_right))
        return None


class _PhysicalPaddle(_APhysicalObject):
    def __init__(self, paddle: Paddle):
        super().__init__()
        self.top: Segment2 = paddle.get_top_collision_segment()
        self.front: Segment2 = paddle.get_front_collision_segment()
        self.bottom: Segment2 = paddle.get_bottom_collision_segment()

        # Used to prevent the ball from getting stuck in the paddle
        self._paddle_was_already_hit: bool = False

        self._closest_side_hit: Optional[str] = None

    def intersect(self,
                  travel: Segment2,
                  current_closest_physical_object_hit: Optional[_APhysicalObject]
                  ) -> Optional[_APhysicalObject]:
        if self._paddle_was_already_hit:
            return current_closest_physical_object_hit
        self._calculate_closest_side_hit(travel)
        if self._closest_side_hit is None:
            return current_closest_physical_object_hit
        if current_closest_physical_object_hit is None:
            return self
        if self.t < current_closest_physical_object_hit.t:
            return self
        return current_closest_physical_object_hit

    def _calculate_closest_side_hit(self, travel: Segment2):
        self._closest_side_hit = None
        self._intersect_top(travel)
        self._intersect_front(travel)
        self._intersect_bottom(travel)

    def _intersect_top(self, travel: Segment2):
        if travel.vector[1] > 0:
            return
        intersection, t = _PhysicalPaddle._circle_segment_intersection(travel, self.top)
        if intersection is None:
            return
        if self.t is None or self.t > t:
            self._closest_side_hit = 'top'
            self.t = t
            self.intersection = intersection

    def _intersect_front(self, travel: Segment2):
        intersection, t = _PhysicalPaddle._circle_segment_intersection(travel, self.front)
        if intersection is None:
            return
        if self.t is None or self.t > t:
            self._closest_side_hit = 'front'
            self.t = t
            self.intersection = intersection

    def _intersect_bottom(self, travel: Segment2):
        if travel.vector[1] < 0:
            return
        intersection, t = _PhysicalPaddle._circle_segment_intersection(travel, self.bottom)
        if intersection is None:
            return
        if self.t is None or self.t > t:
            self._closest_side_hit = 'bottom'
            self.t = t
            self.intersection = intersection

    @staticmethod
    def _circle_segment_intersection(travel: Segment2,
                                     segment: Segment2
                                     ) -> (Optional[numpy.ndarray], Optional[float]):
        # This is not a perfect solution to calculate the intersection between a
        # moving circle and a segment, but it is good enough for our use case
        radius_helper = travel.vector / numpy.linalg.norm(travel.vector) * settings.BALL_RADIUS
        travel_helper: Segment2 = Segment2(travel.begin, travel.end + radius_helper)
        intersection: Optional[numpy.ndarray] = travel_helper.intersect(segment)[0]
        if intersection is None:
            return None, None
        intersection -= radius_helper
        t: float = (intersection[0] - travel.begin[0]) / travel.vector[0]
        return intersection, t

    async def handle_collision(self,
                               travel: Segment2,
                               ball,
                               collision_handler: 'CollisionHandler',
                               match) -> Optional[Segment2]:
        self._paddle_was_already_hit = True
        new_travel_vector = travel.vector * (1. - self.t)
        if self._closest_side_hit == 'up' or self._closest_side_hit == 'down':
            ball.set_movement_y(ball.get_movement()[1] * -settings.BALL_ACCELERATION)
            new_travel_vector[1] *= -settings.BALL_ACCELERATION
        else:
            ball.set_movement_x(ball.get_movement()[0] * -settings.BALL_ACCELERATION)
            new_travel_vector[0] *= -settings.BALL_ACCELERATION
            ball.set_position(self.intersection)
            await EventEmitter.update_ball(
                match.LOCATION, ball.get_position(), ball.get_movement()
            )
        return Segment2(self.intersection,
                        self.intersection + new_travel_vector,
                        new_travel_vector)


class CollisionHandler(object):
    def __init__(self, paddle: Paddle):
        self.TOP_WALL: _Wall = _Wall(True)
        self.BOTTOM_WALL: _Wall = _Wall(False)

        self.RIGHT_GOAL: _Goal = _Goal(True)
        self.LEFT_GOAL: _Goal = _Goal(False)

        self.physical_paddle: _PhysicalPaddle = _PhysicalPaddle(paddle)

    async def update_ball_position_and_movement(self,
                                                ball,
                                                time_delta: float,
                                                match):
        travel: Optional[Segment2] = Segment2(
            ball.get_position(),
            ball.get_position() + ball.get_movement() * time_delta
        )
        while travel is not None:
            closest_object_hit: Optional[_APhysicalObject] = self._get_closest_object_hit(
                travel, self.physical_paddle
            )
            if closest_object_hit is None:
                ball.set_position(travel.end)
                return
            travel = await closest_object_hit.handle_collision(
                travel, ball, self, match
            )

    def _get_closest_object_hit(self, travel, physical_paddle: _PhysicalPaddle):
        closest_object_hit: Optional[_APhysicalObject] = self.TOP_WALL.intersect(travel, None)
        closest_object_hit = self.BOTTOM_WALL.intersect(travel, closest_object_hit)
        closest_object_hit = self.LEFT_GOAL.intersect(travel, closest_object_hit)
        closest_object_hit = self.RIGHT_GOAL.intersect(travel, closest_object_hit)
        return physical_paddle.intersect(travel, closest_object_hit)
