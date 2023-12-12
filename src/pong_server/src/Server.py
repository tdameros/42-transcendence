import asyncio
from typing import *

from Player import Player
from Game import Game


class Server(object):
    def __init__(self, sio):
        # Dict[sid, Player]
        self._players: Dict[str, Player] = {}

        self._players_without_a_game: List[Player] = []

        self._next_game_id: int = 1
        # Dict[game_id, Game]
        self._games: Dict[int, Game] = {}

        self.sio = sio

    async def _add_player(self, sid: str, player: Player):
        print(f"Adding player {player.get_id()} to Server")
        self._players[sid] = player

        if len(self._players_without_a_game) < 1:
            self._players_without_a_game.append(player)
            return

        new_game = Game(self._next_game_id)
        self._games[self._next_game_id] = new_game
        self._next_game_id += 1

        await asyncio.gather(self._players_without_a_game[0].join_game(self.sio,
                                                                       new_game),
                             player.join_game(self.sio, new_game))
        del self._players_without_a_game[0]

        await new_game.start(self.sio)

    def add_player_to_players_without_a_game(self, player: Player):
        self._players_without_a_game.append(player)

    async def register(self, sid: str, query):
        await self._add_player(sid, Player(query, sid))

    def disconnect(self, sid: str, sio):
        player: Player = self._players.pop(sid, None)
        if player is None:
            return

        player.game.stop_game(sio, self)

        # TODO will need to do other things
