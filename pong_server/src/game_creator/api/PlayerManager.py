from typing import Optional

from django.core.cache import cache


class PlayerManager(object):
    @staticmethod
    def add_players(players: list[Optional[int]], game_port: int) -> None:
        for player in players:
            if player is not None:
                cache.set(player, game_port)

    @staticmethod
    def remove_players(players: list[int]) -> None:
        for player in players:
            cache.delete(player)

    @staticmethod
    def get_player_game_port(player: int) -> Optional[int]:
        return cache.get(player)

    @staticmethod
    def clear():
        cache.clear()
