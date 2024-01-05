import asyncio

from Game import Game
from Player import Player


class Server(object):
    def __init__(self, sio):
        # dict[sid, Player]
        self._players: dict[str, Player] = {}

        self._players_without_a_game: list[Player] = []

        self._next_game_id: int = 1
        # dict[game_id, Game]
        self._games: dict[int, Game] = {}

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

    def get_player_by_sid(self, sid):
        return self._players.get(sid, None)

    async def set_player_movement(self, sid, sio, movement):
        player = self.get_player_by_sid(sid)
        if player is not None:
            await player.set_movement(sio, movement)

    def remove_game(self, game: Game):
        self._games.pop(game.get_id(), None)

    async def disconnect(self, sid: str, sio):
        player: Player = self._players.pop(sid, None)
        if player is None:
            return

        player.disconnect()
        player_game = player.get_game()
        if player_game is not None:
            await player_game.stop_game(sio, self)

        # TODO will need to do other things
