import os
import subprocess
from typing import AnyStr, Optional

from api import error_messages
from api.JsonResponseException import JsonResponseException


class GameCreator(object):
    @staticmethod
    def create_game_server(game_id: int, players: list[Optional[int]]) -> str:
        process: subprocess.Popen = GameCreator._start_server(game_id, players)

        while process.poll() is None:
            line = process.stdout.readline()
            uri = GameCreator._parse_subprocess_line(line)
            if uri is not None:
                return uri

        remaining_output = process.communicate()[0]
        for line in remaining_output.splitlines():
            GameCreator._parse_subprocess_line(line)

        raise JsonResponseException({'errors': 'Error creating game server: undefined error'},
                                    status=500)

    @staticmethod
    def _start_server(game_id: int, players: list[Optional[int]]) -> subprocess.Popen:
        try:
            command = ['python3', '-m', 'src.game_server', str(game_id)]
            for player in players:
                command.append(str(player))
            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    cwd=os.getenv('PONG_GAME_APP_PATH'),
                                    universal_newlines=True)
        except Exception as e:
            error = error_messages.popen_failed_to_run_command(str(e))
            raise JsonResponseException({'errors': [error]}, status=500)

    @staticmethod
    def _parse_subprocess_line(line: AnyStr) -> Optional[str]:
        if not line:
            return None

        if line.startswith('uri: '):
            return line[len('uri: '):-1]

        if line.startswith('Error: '):
            error = error_messages.error_creating_game_server(line[len('Error: '):-1])
            raise JsonResponseException({'errors': [error]}, status=500)

        return None
