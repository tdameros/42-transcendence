import settings
from vector_to_dict import vector_to_dict


class _Board(object):
    """ This class is empty.
        it exists to facilitate potential changes to the way boards work """

    def __init__(self):
        pass

    @staticmethod
    def to_json() -> dict:
        return {
            'size': vector_to_dict(settings.BOARD_SIZE)
        }

    def update(self, time_delta: float):
        pass
