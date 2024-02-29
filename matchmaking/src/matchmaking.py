import asyncio
from time import time
from typing import Any, Optional

import src.error_message as error
import src.settings as settings

from .player import Player


class Matchmaking:

    def __init__(self, server: Any):
        self.server = server
        self.queue = []
        self.found_matches = []

    async def routine(self) -> None:
        while True:
            for index, player in enumerate(self.queue):
                opponent = self.search_opponent(player, index)
                if opponent is not None:
                    self.found_matches.append((player, opponent))
            for player, opponent in self.found_matches:
                await self.server.send_match(player, opponent)
            self.found_matches = []
            await asyncio.sleep(2)

    def search_opponent(self, player: Player, index: int) -> Optional[Player]:
        if index == len(self.queue) - 1:
            return None
        closest_opponent = None
        elo_threshold = self.get_elo_threshold(player)
        for opponent in self.queue[index + 1:]:
            if Matchmaking.elo_gap(player, opponent) < elo_threshold:
                if closest_opponent is None:
                    closest_opponent = opponent
                elif Matchmaking.elo_gap(player, opponent) < Matchmaking.elo_gap(player, closest_opponent):
                    closest_opponent = opponent
        return closest_opponent

    def add_player(self, player: Player) -> Optional[str]:
        for queue_player in self.queue:
            if queue_player.sid == player.sid:
                return error.ALREADY_IN_QUEUE
        self.queue.append(player)
        return None

    def remove_player(self, sid) -> None:
        for player in self.queue:
            if player.sid == sid:
                self.queue.remove(player)
                return

    @staticmethod
    def get_elo_threshold(player: Player) -> int:
        elapsed_time = time() - player.timestamp
        threshold_factor = elapsed_time / settings.THRESHOLD_TIME
        elo_threshold = settings.ELO_THRESHOLD * threshold_factor
        return elo_threshold

    @staticmethod
    def elo_gap(player1: Player, player2: Player) -> int:
        return abs(player1.elo - player2.elo)
