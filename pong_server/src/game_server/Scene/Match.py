import numpy

from src.game_server.Scene.Ball import Ball
from src.game_server.Scene.Player.Player import Player
from src.game_server.vector_to_dict import vector_to_dict


class Match(object):
    def __init__(self, position: numpy.ndarray):
        self._position = position.copy()

        self._players: list[Player] = [Player(is_player_on_the_right=False),
                                       Player(is_player_on_the_right=True)]

        self._ball: Ball = Ball()

    def to_json(self) -> dict:
        return {
            'position': vector_to_dict(self._position),
            'players': [player.to_json() for player in self._players],
            'ball': self._ball.to_json()
        }

    def update_positions(self, time_delta: float):
        self._players[0].update_position(time_delta)
        self._players[1].update_position(time_delta)
        self._ball.update_position(time_delta)

    def get_player(self, index: int) -> Player:
        return self._players[index]
