from src.game_server.Scene.Player.Player import Player
from src.game_server.Scene.PlayerFinder.PlayerLocation import PlayerLocation
from src.game_server.Scene.Scene import Scene


class PlayerFinder:
    def __init__(self, players_id: list[str]):
        #                             dict[user_id: PlayerData]
        self._user_id_to_player_data: dict[str: PlayerLocation] = {}
        i: int = 0
        for player_id in players_id:
            self._user_id_to_player_data[player_id] = PlayerLocation(int(i / 2), i % 2)
            i += 1

        #                         dict[sid, PlayerData]
        self._sid_to_player_data: dict[str: PlayerLocation] = {}

    def add_player(self, user_id: str, sid: str):
        player_data: PlayerLocation | None = self._user_id_to_player_data.get(user_id)
        if player_data is not None:
            self._sid_to_player_data[sid] = player_data

    def remove_player(self, sid: str):
        del self._sid_to_player_data[sid]

    def get_player_location_from_sid(self, sid: str) -> PlayerLocation | None:
        return self._sid_to_player_data.get(sid)

    def get_player_location_from_user_id(self, user_id: str):
        return self._user_id_to_player_data.get(user_id)

    def get_player(self, scene: Scene, sid: str) -> Player | None:
        player_data: PlayerLocation | None = self.get_player_location_from_sid(sid)
        if player_data is None:
            return None
        return player_data.get_player_from_scene(scene)
