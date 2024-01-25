from src.game_server.Scene.Player.Player import Player


class Scene(object):
    """ Forward declaration since Scene import Player I can't import
        Scene in this file """
    pass


class PlayerLocation(object):
    def __init__(self, match_index: int, player_index: int):
        self._is_in_a_match: bool = True
        self._match_index: int = match_index
        self._player_index: int = player_index

    def to_json(self) -> dict:
        return {
            'is_in_a_match': self._is_in_a_match,
            'match_index': self._match_index,
            'player_index': self._player_index,
        }

    def get_match_index(self) -> int | None:
        if not self._is_in_a_match:
            return None
        return self._match_index

    def get_player_index(self) -> int | None:
        if not self._is_in_a_match:
            return None
        return self._player_index

    def get_player_from_scene(self, scene: Scene) -> Player:
        return scene.get_match(self._match_index).get_player(self._player_index)
