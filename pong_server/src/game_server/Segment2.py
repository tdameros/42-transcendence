from typing import Optional

import numpy


class Segment2(object):
    def __init__(self, begin: numpy.ndarray, end: numpy.ndarray):
        self._begin = begin.copy()
        self._end = end.copy()

    def intersect(self,
                  segment2) -> (Optional[numpy.ndarray], Optional[float]):
        s2 = segment2

        t1_top = ((s2._end[0] - s2._begin[0])
                  * (self._begin[1] - s2._begin[1])
                  - (s2._end[1] - s2._begin[1]) * (self._begin[0] - s2._begin[0]))

        t2_top = ((s2._begin[1] - self._begin[1])
                  * (self._begin[0] - self._end[0])
                  - (s2._begin[0] - self._begin[0]) * (self._begin[1] - self._end[1]))

        bottom = ((s2._end[1] - s2._begin[1])
                  * (self._end[0] - self._begin[0])
                  - (s2._end[0] - s2._begin[0]) * (self._end[1] - self._begin[1]))

        if bottom == 0:
            return None, None

        t1 = t1_top / bottom
        if t1 < 0 or t1 > 1:
            return None, None

        t2 = t2_top / bottom
        if t2 < 0 or t2 > 1:
            return None, None

        return (
            numpy.array([self._begin[0] + t1 * (self._end[0] - self._begin[0]),
                         self._begin[1] + t1 * (self._end[1] - self._begin[1])]),
            t1
        )
