class MatchLocation(object):
    def __init__(self, game_round: int, match: int):
        self.game_round: int = game_round
        self.match: int = match

    def to_json(self) -> dict:
        return {
            'game_round': self.game_round,
            'match': self.match
        }
