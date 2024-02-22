import json
import logging
import traceback
from abc import ABC, abstractmethod

import requests
from requests import Response

from common.src.internal_requests import InternalAuthRequests
from EventEmitter import EventEmitter
from Server import Server


class ABaseAPI(ABC):
    @staticmethod
    @abstractmethod
    async def post_start_match(game_id: int, player_1_id: int, player_2_id: int):
        pass

    @staticmethod
    @abstractmethod
    async def post_add_point(game_id: int, id_of_player_that_marked_a_point: int):
        pass

    @staticmethod
    @abstractmethod
    async def post_end_match(game_id: int,
                             winner_id: int,
                             winner_score: int,
                             looser_id: int,
                             looser_score: int):
        pass

    @staticmethod
    async def _post(uri: str, json_dict: dict):
        try:
            response: Response = InternalAuthRequests.post(uri, data=json.dumps(json_dict))
        except requests.exceptions.RequestException as e:
            await ABaseAPI._handle_error(
                f'Connection error during {ABaseAPI._get_caller_info()}: {e}'
            )
            return
        if not response.ok:
            try:
                error = response.json()['errors']
            except Exception:
                error = response.text

            await ABaseAPI._handle_error(
                f'Server error {response.status_code} during {ABaseAPI._get_caller_info()}: '
                f'{error}'
            )
            return

    @staticmethod
    def _get_caller_info() -> str:
        return traceback.format_stack()[-3].split('\n')[1].strip()

    @staticmethod
    async def _handle_error(error: str):
        logging.critical(error)
        await EventEmitter.fatal_error(error)
        await Server.sio.sleep(10)  # Wait for the clients to receive the error message
        Server.exit_code = 5
        Server.should_stop = True
