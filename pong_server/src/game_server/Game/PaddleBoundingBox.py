import settings as settings


class PaddleBoundingBox(object):
    def __init__(self):
        self._y_max = settings.BOARD_SIZE[1] * 0.5 - settings.PADDLE_SIZE[1] * 0.5
        self._y_min = -self._y_max

    def get_y_min(self):
        return self._y_min

    def get_y_max(self):
        return self._y_max
