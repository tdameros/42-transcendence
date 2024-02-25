import os
import subprocess
from typing import AnyStr, Optional

import shared_code.error_messages
from api import error_messages
from api.JsonResponseException import JsonResponseException


class GameCreator(object):
    @staticmethod
    def create_game_server(game_id: int,
                           players: list[Optional[int]],
                           api_name: str) -> int:
        process: subprocess.Popen = GameCreator._start_server(game_id, players, api_name)

        while process.poll() is None:
            line = process.stdout.readline()
            port: Optional[int] = GameCreator._parse_subprocess_line(line)
            if port is not None:
                return port

        remaining_output = process.communicate()[0]
        for line in remaining_output.splitlines():
            GameCreator._parse_subprocess_line(line)

        raise JsonResponseException({'errors': 'Error creating game server: undefined error'},
                                    status=500)

    @staticmethod
    def _start_server(game_id: int,
                      players: list[Optional[int]],
                      api_name: str) -> subprocess.Popen:
        try:
            command = ['python3', 'main.py', str(game_id), api_name]
            for player in players:
                command.append(str(player))
            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    cwd=os.getenv('GAME_SERVER_PATH'),
                                    universal_newlines=True)
        except Exception as e:
            error = error_messages.popen_failed_to_run_command(str(e))
            raise JsonResponseException({'errors': [error]}, status=500)

    @staticmethod
    def _parse_subprocess_line(line: AnyStr) -> Optional[int]:
        if not line:
            return None

        if line.startswith('port: '):
            return int(line[len('port: '):-1])

        if line.startswith('Error: '):
            error = line[len('Error: '):-1]
            if error == shared_code.error_messages.NO_AVAILABLE_PORTS:
                raise JsonResponseException({
                    'errors': [error]
                }, status=503)
            raise JsonResponseException({
                'errors': [error_messages.error_creating_game_server(error)]
            }, status=500)

        return None
