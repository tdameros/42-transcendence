from typing import Optional


class PlayerManager(object):
    #       dict[user_id, game_port]
    _users: dict[int, int] = {}

    @staticmethod
    def add_players(players: list[Optional[int]], game_port: int) -> None:
        for player in players:
            if player is not None:
                PlayerManager._users[player] = game_port

    @staticmethod
    def remove_players(players: list[int]) -> None:
        for player in players:
            PlayerManager._users.pop(player, None)

    @staticmethod
    def get_player_game_port(player: int) -> Optional[int]:
        return PlayerManager._users.get(player)
