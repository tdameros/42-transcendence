import time


class Clock(object):
    def __init__(self):
        self._last_recorded_time = time.time()

    def get_time(self) -> (float, float):
        """ Returns the current time and the time since the last call to this method. """

        current_time = time.time()

        delta = current_time - self._last_recorded_time

        self._last_recorded_time = current_time

        return current_time, delta
