from typing import *

from Player import Player
from GameScene import GameScene
from vector_to_dict import vec3_to_dict


class Game(object):
    def __init__(self, game_id: int):
        print(f"Creating game {game_id}")
        self._id: int = game_id
        self._players_score: List[int] = []
        self._players: List[Player] = []
        self._room: str = f"game_room_{game_id}"

    def get_id(self) -> int:
        return self._id

    async def add_player(self, sio, player: Player):
        print(f"Added player {player.get_id()} to game {self._id}")
        self._players.append(player)
        self._players_score.append(0)
        await sio.enter_room(player.get_sid(), self._room)

    async def start(self, sio):
        self._init_scene()
        await sio.emit("scene", self._scene.to_json(), room=self._room)
        print(f"Game {self._id} started")

    def _init_scene(self):
        self._scene = GameScene()
        self._scene.init_2_player_game()

    async def stop_game(self, sio, server):
        for player in self._players:
            await sio.leave_room(player.get_sid(), self._room)
            server.add_player_to_players_without_a_game(player)
            player.game = None
