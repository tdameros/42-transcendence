import numpy

AUTHORIZED_DELAY = 0.1

PLAYER_MOVE_SPEED = 15.

BOARD_SIZE = numpy.array([20., 27.5, 0.])

PADDLE_SIZE = numpy.array([1., 5., 1.])
PADDLE_MOVE_SPEED = 9.
PADDLE_X_POSITION = BOARD_SIZE[0] * 0.5 - PADDLE_SIZE[0] * 0.75

BALL_RADIUS = 1.
