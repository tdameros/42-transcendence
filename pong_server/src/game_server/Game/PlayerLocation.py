from Game.MatchLocation import MatchLocation


class PlayerLocation(object):
    def __init__(self,
                 game_round: int,
                 match: int,
                 player_index: int,
                 is_looser: bool = False):
        self.is_looser: bool = is_looser

        if is_looser:
            self.match_location: MatchLocation = MatchLocation(-1, -1)
        else:
            self.match_location: MatchLocation = MatchLocation(game_round, match)

        self.player_index: int = player_index

    def to_json(self) -> dict:
        return {
            'is_looser': self.is_looser,
            'match_location': self.match_location.to_json(),
            'player_index': self.player_index
        }
