from typing import Optional

import numpy


class Segment2(object):
    def __init__(self,
                 begin: numpy.ndarray,
                 end: numpy.ndarray,
                 vector: Optional[numpy.ndarray] = None):
        self.begin = numpy.array([begin[0], begin[1]], dtype=float)
        self.end = numpy.array([end[0], end[1]], dtype=float)
        if vector is not None:
            self.vector = numpy.array([vector[0], vector[1]], dtype=float)
        else:
            self.vector = self.end - self.begin

    def intersect(self, segment2) -> (Optional[numpy.ndarray], Optional[float]):
        s2 = segment2

        t1_top = ((s2.end[0] - s2.begin[0])
                  * (self.begin[1] - s2.begin[1])
                  - (s2.end[1] - s2.begin[1]) * (self.begin[0] - s2.begin[0]))

        t2_top = ((s2.begin[1] - self.begin[1])
                  * (self.begin[0] - self.end[0])
                  - (s2.begin[0] - self.begin[0]) * (self.begin[1] - self.end[1]))

        bottom = ((s2.end[1] - s2.begin[1])
                  * (self.end[0] - self.begin[0])
                  - (s2.end[0] - s2.begin[0]) * (self.end[1] - self.begin[1]))

        if bottom == 0:
            return None, None

        t1 = t1_top / bottom
        if t1 < 0 or t1 > 1:
            return None, None

        t2 = t2_top / bottom
        if t2 < 0 or t2 > 1:
            return None, None

        return (
            numpy.array([self.begin[0] + t1 * (self.end[0] - self.begin[0]),
                         self.begin[1] + t1 * (self.end[1] - self.begin[1])],
                        dtype=float),
            t1
        )
