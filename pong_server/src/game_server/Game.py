import sys


class Game(object):
    def __init__(self):
        self._players: list[str] = []

    def read_argv(self):
        for arg in sys.argv[1:]:
            self._players.append(arg)

        if len(self._players) == 0:
            raise Exception("Game is empty")
        if len(self._players) % 2 == 1:
            raise Exception(f"Game has an odd number of players "
                            f"(number of players: {len(self._players)})")
