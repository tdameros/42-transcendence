from typing import Optional

import rooms
from Server import Server


class ClientManager(object):
    #            list[user_id]
    CLIENTS_IDS: list[int] = []
    #         dict[user_id, sid]
    _sid_map: dict[int, str] = {}
    #             dict[sid, user_id]
    _user_id_map: dict[str, int] = {}

    @staticmethod
    def init(clients_ids: list[int]):
        ClientManager.CLIENTS_IDS = clients_ids

    @staticmethod
    def have_all_players_joined():
        return len(ClientManager._sid_map) == len(ClientManager.CLIENTS_IDS)

    @staticmethod
    def get_user_sid(user_id: int) -> Optional[str]:
        return ClientManager._sid_map.get(user_id)

    @staticmethod
    def get_user_id(sid: str) -> Optional[int]:
        return ClientManager._user_id_map.get(sid)

    @staticmethod
    async def add_newly_connected_user(user_id: int, sid: str):
        ClientManager._sid_map[user_id] = sid
        ClientManager._user_id_map[sid] = user_id
        await Server.sio.enter_room(sid, rooms.ALL_PLAYERS)

    @staticmethod
    async def remove_disconnected_user(sid: str):
        user_id = ClientManager._user_id_map[sid]
        del ClientManager._sid_map[user_id]
        del ClientManager._user_id_map[sid]
        await Server.sio.leave_room(sid, rooms.ALL_PLAYERS)

    @staticmethod
    async def disconnect_all_users():
        while len(ClientManager._user_id_map) != 0:
            await Server.sio.disconnect(list(ClientManager._sid_map.values())[0])
