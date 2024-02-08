import logging
from typing import Optional

import numpy
import socketio

import rooms as rooms
from Scene.PlayerFinder.PlayerFinder import PlayerFinder
from Scene.PlayerFinder.PlayerLocation import PlayerLocation
from Scene.Scene import Scene
from shared_code.emit import emit
from vector_to_dict import vector_to_dict


class Game(object):
    def __init__(self, args: list[str]):
        self._game_id: int = int(args[0])

        #            const list[user_id]
        self.PLAYERS_LIST: list[Optional[int]] = []
        for player in args[1:]:
            try:
                self.PLAYERS_LIST.append(int(player))
            except ValueError:
                self.PLAYERS_LIST.append(None)
        logging.debug(f'Successfully parsed arguments: {args}')

        if len(self.PLAYERS_LIST) == 0:
            raise Exception('Game is empty')

        #                  dict[sid, user_id]
        self._user_id_map: dict[str: int] = {}
        #                     dict[user_id, sid]
        self._player_sid_map: dict[int: str] = {}

        self._player_finder: PlayerFinder = PlayerFinder(self.PLAYERS_LIST)

        self._scene: Scene = Scene(len(self.PLAYERS_LIST))

        self.has_started: bool = False

    def is_user_part_of_game(self, user_id: int) -> bool:
        return user_id in self.PLAYERS_LIST

    def get_sid_from_user_id(self, user_id: int) -> str | None:
        return self._player_sid_map.get(user_id)

    async def add_user(self, user_id: int, sid: str, sio: socketio.AsyncServer):
        self._player_sid_map[user_id] = sid
        self._player_finder.add_player(user_id, sid)
        await sio.enter_room(sid, rooms.ALL_PLAYERS)

    async def remove_user(self, sid: str, sio: socketio.AsyncServer):
        try:
            user_id: int | None = self._user_id_map.pop(sid)
            if user_id is not None:
                del self._player_sid_map[user_id]
            self._player_finder.remove_player(sid)
            await sio.leave_room(sid, rooms.ALL_PLAYERS)
        except KeyError:
            pass

    def have_all_players_joined(self) -> bool:
        return len(self._player_sid_map.keys()) == len(self.PLAYERS_LIST)

    def get_scene(self) -> Scene:
        return self._scene

    def get_player_location(self, sid: str) -> PlayerLocation | None:
        return self._player_finder.get_player_location_from_sid(sid)

    async def set_player_movement_and_position(self,
                                               sio: socketio.AsyncServer,
                                               player_location: PlayerLocation,
                                               direction: str,
                                               player_position: numpy.ndarray,
                                               skip_sid: str | None = None):
        self._scene.set_player_paddle_direction(player_location, direction)
        self._scene.set_player_paddle_position(player_location, player_position)
        await emit(sio, 'update_player', rooms.ALL_PLAYERS,
                   {
                       'player_location': player_location.to_json(),
                       'direction': direction,
                       'position': vector_to_dict(player_position)
                   },
                   skip_sid)
