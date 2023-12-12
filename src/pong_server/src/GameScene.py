from typing import List
import Object


class GameScene(object):
    def __init__(self):
        self._boards: List[Object.Board] = []
        self._balls: List[Object.Ball] = []
        self._players: List[Object.PlayerObject] = []

    def to_json(self):
        return {
            "boards": [board.to_json() for board in self._boards],
            "balls": [ball.to_json() for ball in self._balls],
            "players": [player.to_json() for player in self._players],
        }

    def init_2_player_game(self):
        self._boards.append(Object.Board(0., 0., 0.))

        self._balls.append(Object.Ball(0., 0., 0.5))

        self._players.append(Object.PlayerObject(-18.5, 0., 0.5))
        self._players.append(Object.PlayerObject(18.5, 0., 0.5))
