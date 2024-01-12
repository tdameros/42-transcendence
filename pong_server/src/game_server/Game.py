import sys

import src.game_server.rooms as rooms
from src.game_server.Scene import Scene
from src.game_server.vector_to_dict import vector_to_dict
from src.shared_code.emit import emit


class Game(object):
    def __init__(self):
        #                   list[user_id]
        self._players_list: list[str] = []

        #                 dict[sid: user_id]
        self._player_map: dict[str: str] = {}

        #              dict[user_id: sid]
        self._sid_map: dict[str: str] = {}

        #                       dict[user_id, index]
        self._player_index_map: dict[str: int] = {}

        self._scene: Scene | None = None

        self.has_started: bool = False

    def init_game_from_argv(self):
        for arg in sys.argv[1:]:
            self._players_list.append(arg)

        if len(self._players_list) == 0:
            raise Exception('Game is empty')
        if len(self._players_list) % 2 == 1:
            raise Exception(f'Game has an odd number of players '
                            f'(number of players: {len(self._players_list)})')

        self._scene = Scene(len(self._players_list))

    def get_player_list(self):
        return self._players_list

    def is_user_part_of_game(self, user_id: str) -> bool:
        return user_id in self._players_list

    def get_user_sid(self, user_id: str) -> str:
        return self._sid_map.get(user_id)

    async def add_user(self, user_id: str, sid: str, sio):
        self._player_map[sid] = user_id
        self._sid_map[user_id] = sid
        self._player_index_map[sid] = self._players_list.index(user_id)
        await sio.enter_room(sid, rooms.ALL_PLAYERS)

    async def remove_user(self, sid: str, sio):
        user_id = self._player_map.pop(sid)
        if user_id is not None:
            del self._sid_map[user_id]
        del self._player_index_map[sid]
        await sio.leave_room(sid, rooms.ALL_PLAYERS)

    def have_all_players_joined(self) -> bool:
        return len(self._sid_map.keys()) == len(self._players_list)

    def get_scene(self):
        return self._scene

    def get_player_index(self, sid: str) -> int:
        return self._player_index_map[sid]

    async def set_player_movement_and_position(self,
                                               sio,
                                               skip_sid,
                                               player_index,
                                               direction,
                                               player_position):
        self._scene.set_player_movement(player_index, direction)
        self._scene.set_player_position(player_index, player_position)
        await emit(sio, 'update_player', rooms.ALL_PLAYERS,
                   {
                       'player_index': player_index,
                       'direction': direction,
                       'position': vector_to_dict(player_position)
                   },
                   skip_sid)
