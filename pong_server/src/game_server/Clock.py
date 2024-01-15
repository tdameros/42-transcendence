import datetime


class Clock(object):
    def __init__(self):
        self._last_recorded_time = datetime.datetime.now()

    def get_delta(self):
        current_time = datetime.datetime.now()
        delta = current_time - self._last_recorded_time
        self._last_recorded_time = current_time
        return delta.total_seconds()
