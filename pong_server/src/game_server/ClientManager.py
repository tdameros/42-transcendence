import json
import logging
from typing import Optional

import requests

import rooms
from common.src.internal_requests import InternalAuthRequests
from common.src.settings import \
    GAME_CREATOR_REMOVE_PLAYERS_CURRENT_GAME_ENDPOINT
from Server import Server


class ClientManager(object):
    #            list[user_id]
    CLIENTS_IDS: list[int] = []

    #                                    list[user_id]
    _clients_registered_in_game_creator: list[int] = []

    #         dict[user_id, sid]
    _sid_map: dict[int, str] = {}
    #             dict[sid, user_id]
    _user_id_map: dict[str, int] = {}

    _ready_players: set[int] = set()

    @staticmethod
    def init(clients_ids: list[int]):
        ClientManager.CLIENTS_IDS = clients_ids
        ClientManager._clients_registered_in_game_creator = clients_ids.copy()

    @staticmethod
    def are_all_players_ready():
        return len(ClientManager._ready_players) == len(ClientManager.CLIENTS_IDS)

    @staticmethod
    def add_ready_player(user_id: int):
        if user_id not in ClientManager._ready_players:
            ClientManager._ready_players.add(user_id)

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
        try:
            user_id = ClientManager._user_id_map[sid]
            del ClientManager._sid_map[user_id]
            del ClientManager._user_id_map[sid]
            ClientManager._ready_players.remove(user_id)
            await Server.sio.leave_room(sid, rooms.ALL_PLAYERS)
        except KeyError:
            pass

    @staticmethod
    async def disconnect_all_users():
        while len(ClientManager._user_id_map) != 0:
            await Server.sio.disconnect(list(ClientManager._sid_map.values())[0])

    @staticmethod
    def unregister_player(player_id: int):
        if ClientManager._post_remove_players_current_game(
                [player_id], 'ClientManager.unregister_player()'):
            ClientManager._clients_registered_in_game_creator.remove(player_id)

    @staticmethod
    def unregister_all_players():
        if ClientManager._post_remove_players_current_game(
                ClientManager._clients_registered_in_game_creator,
                'ClientManager.unregister_all_players()'):
            ClientManager._clients_registered_in_game_creator.clear()

    @staticmethod
    def _post_remove_players_current_game(players: list[int],
                                          calling_function_name: str) -> bool:
        url: str = GAME_CREATOR_REMOVE_PLAYERS_CURRENT_GAME_ENDPOINT
        body: dict = {'players': players}

        logging.info(f'POST request to {url} with body {body} during '
                     f'{calling_function_name}')
        try:
            response = InternalAuthRequests.post(url, json.dumps(body))
        except requests.exceptions.RequestException as e:
            logging.critical(f'Connection error during {calling_function_name}: {e}')
            return False
        if not response.ok:
            try:
                error = response.json()['errors']
            except Exception:
                error = response.text

            logging.critical(f'Server error {response.status_code} during'
                             f'{calling_function_name}: {error}')
            return False
        return True
