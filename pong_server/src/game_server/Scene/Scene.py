import numpy

from src.game_server import settings
from src.game_server.Scene.Match import Match
from src.game_server.Scene.Player.Player import Player
from src.game_server.Scene.PlayerFinder.PlayerLocation import PlayerLocation


class Scene(object):
    def __init__(self, nb_of_players: int):

        self._matches: list[Match] = []

        match_x_position: float = 0.
        for i in range(int(nb_of_players / 2)):
            self._matches.append(Match(numpy.array([match_x_position,
                                                    0.,
                                                    0.])))
            match_x_position += settings.BOARD_SIZE[0] * 2. + settings.BOARD_SIZE[0] / 2.

    def to_json(self):
        return {
            "matches": [match.to_json() for match in self._matches]
        }

    def update(self, time_delta: float):
        for match in self._matches:
            match.update_positions(time_delta)

    def get_match(self, index: int):
        return self._matches[index]

    def set_player_paddle_position(self,
                                   player_location: PlayerLocation,
                                   player_position: numpy.ndarray):
        match: Match = self._matches[player_location.get_match_index()]
        player: Player = match.get_player(player_location.get_player_index())
        player.set_paddle_position(player_position)

    def get_player_paddle_position(self,
                                   player_location: PlayerLocation) -> numpy.ndarray:
        match: Match = self._matches[player_location.get_match_index()]
        player: Player = match.get_player(player_location.get_player_index())
        return player.get_paddle_position()

    def set_player_paddle_direction(self,
                                    player_location: PlayerLocation,
                                    direction: str):
        match: Match = self._matches[player_location.get_match_index()]
        player: Player = match.get_player(player_location.get_player_index())
        player.set_paddle_direction(direction)

    def get_player_paddle_movement(self,
                                   player_location: PlayerLocation) -> numpy.ndarray:
        match: Match = self._matches[player_location.get_match_index()]
        player: Player = match.get_player(player_location.get_player_index())
        return player.get_paddle_movement()
