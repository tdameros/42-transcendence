import numpy

from Game.bounding_boxes import BallBoundingBox, PaddleBoundingBox

AUTHORIZED_DELAY: float = 0.1

PLAYER_MOVE_SPEED: float = 15.

BOARD_SIZE: numpy.ndarray = numpy.array([20., 27.5, 0.])
MATCH_SIZE: numpy.ndarray = numpy.array([BOARD_SIZE[0] * 2., BOARD_SIZE[1]])
MATCHES_X_OFFSET: float = MATCH_SIZE[0] / 4.
MATCHES_Y_OFFSET: float = MATCH_SIZE[1] / 4.

BALL_RADIUS: float = 1.
BALL_ACCELERATION: float = 1.1
BALL_BOUNDING_BOX: BallBoundingBox = BallBoundingBox()
BALL_WAITING_TIME_SEC: float = 2.

PADDLE_SIZE: numpy.ndarray = numpy.array([1., 5., 1.])
PADDLE_MOVE_SPEED: float = 9.
PADDLE_X_POSITION: float = BOARD_SIZE[0] * 0.5 - BALL_RADIUS * 1.5 - PADDLE_SIZE[0] * 0.5
PADDLE_BOUNDING_BOX: PaddleBoundingBox = PaddleBoundingBox()

POINTS_TO_WIN_MATCH: int = 5

BASE_OFFSET: float = MATCHES_X_OFFSET
