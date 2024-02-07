import numpy

from Scene.bounding_boxes import BallBoundingBox, PaddleBoundingBox

AUTHORIZED_DELAY: float = 0.1

PLAYER_MOVE_SPEED: float = 15.

BOARD_SIZE: numpy.ndarray = numpy.array([20., 27.5, 0.])

BALL_RADIUS: float = 1.
BALL_ACCELERATION: float = 1.1
BALL_BOUNDING_BOX: BallBoundingBox = BallBoundingBox()
BALL_WAITING_TIME_SEC: float = 2.

PADDLE_SIZE: numpy.ndarray = numpy.array([1., 5., 1.])
PADDLE_MOVE_SPEED: float = 9.
PADDLE_X_POSITION: float = BOARD_SIZE[0] * 0.5 - BALL_RADIUS * 1.5 - PADDLE_SIZE[0] * 0.5
PADDLE_BOUNDING_BOX: PaddleBoundingBox = PaddleBoundingBox()

POINTS_TO_WIN: int = 5
