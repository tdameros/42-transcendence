from src.game_server.Object import Ball, Board, Player


class Scene(object):
    def __init__(self, nb_of_players: int):
        self._boards: list[Board] = []
        self._balls: list[Ball] = []
        self._players: list[Player] = []

        # TODO this should work for n players, it generates a 2 players scene
        #      for now so that I can run tests
        self._boards.append(Board(0., 0., 0.))

        self._balls.append(Ball(0., 0., 0.5))

        self._players.append(Player(-18.5, 0., 0.5))
        self._players.append(Player(18.5, 0., 0.5))

    def to_json(self):
        return {
            'boards': [board.to_json() for board in self._boards],
            'balls': [ball.to_json() for ball in self._balls],
            'players': [player.to_json() for player in self._players],
        }

    def set_player_movement(self, player_index, movement):
        self._players[player_index].set_movement(movement)
