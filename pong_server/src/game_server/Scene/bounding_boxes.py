import settings as settings


class BallBoundingBox(object):
    def __init__(self):
        half_radius = settings.BALL_RADIUS * 0.5
        self._y_max = settings.BOARD_SIZE[1] * 0.5 - half_radius
        self._y_min = -self._y_max
        self._x_max = settings.BOARD_SIZE[0] - half_radius
        self._x_min = -self._x_max

    def get_y_min(self):
        return self._y_min

    def get_y_max(self):
        return self._y_max

    def get_x_min(self):
        return self._x_min

    def get_x_max(self):
        return self._x_max


class PaddleBoundingBox(object):
    def __init__(self):
        self._y_max = settings.BOARD_SIZE[1] * 0.5 - settings.PADDLE_SIZE[1] * 0.5
        self._y_min = -self._y_max

    def get_y_min(self):
        return self._y_min

    def get_y_max(self):
        return self._y_max
