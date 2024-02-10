from types import NotImplementedType


class MatchLocation(object):
    def __init__(self, game_round: int, match: int):
        self.game_round: int = game_round
        self.match: int = match

    def to_json(self) -> dict:
        return {
            'game_round': self.game_round,
            'match': self.match
        }

    def __key(self) -> tuple[int, int]:
        return self.game_round, self.match

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool | NotImplementedType:
        if isinstance(other, MatchLocation):
            return self.__key() == other.__key()
        return NotImplemented
