import time

import numpy
import socketio

import settings
from Scene.Match import Match
from Scene.Player.Player import Player
from Scene.PlayerFinder.PlayerLocation import PlayerLocation


class Scene(object):
    def __init__(self, nb_of_players: int):

        self._matches: list[Match] = []

        match_x_position: float = 0.
        for i in range(int(nb_of_players / 2)):
            match_position = numpy.array([match_x_position, 0., 0.])
            self._matches.append(Match(match_position, i))
            match_x_position += settings.BOARD_SIZE[0] * 2. + settings.BOARD_SIZE[0] / 2.

    def to_json(self):
        return {
            "matches": [match.to_json() for match in self._matches]
        }

    async def start_game(self, sio: socketio.AsyncServer):
        for match in self._matches:
            await match.start_game(sio)

    async def update(self, sio: socketio.AsyncServer, time_delta: float):
        current_time = time.time()
        for match in self._matches:
            await match.update(sio, time_delta, current_time)

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
