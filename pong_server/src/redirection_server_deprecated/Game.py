import logging
import subprocess

import src.shared_code.settings as settings


class Game(object):
    def __init__(self, clients: list[int]):
        self._clients: list[int] = clients
        self._uri: str | None = None

    def create_server(self):
        """ Can Raise Exception """

        process: subprocess.Popen = self._start_server()
        output: list[str] = []
        while process.poll() is None:
            line = process.stdout.readline()
            if self._parse_subprocess_line(line):
                return
            if settings.LOG_LEVEL != settings.NO_LOGS:
                output.append(line)
        remaining_output = process.communicate()[0]
        for line in remaining_output.splitlines():
            self._parse_subprocess_line(line)  # Will throw if the server
            #                                    printed an error message
            if settings.LOG_LEVEL != settings.NO_LOGS:
                output.append(line)

        raise Exception('Error creating game server: undefined error')

    def _start_server(self) -> subprocess.Popen:
        """ Can Raise Exception """

        try:
            command = ['python3', '-m', 'src.game_server', '0']
            for player in self._clients:
                command.append(str(player))
            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
        except Exception as e:
            raise Exception(f'Failed to run command to start new game '
                            f'server: {e}')

    def _parse_subprocess_line(self, line):
        """ Can Raise Exception """

        if not line:
            return False

        if line.startswith('uri: '):
            self._uri = line[len('uri: '):-1]
            logging.info(f'Created game server with uri {self._uri}')
            return True

        if line.startswith('Error: '):
            raise Exception(f'Error creating game server: '
                            f'{line[len('Error: '):-1]}')

        return False

    def was_server_created(self) -> bool:
        return self._uri is not None

    def get_clients(self) -> list[int]:
        return self._clients

    def get_uri(self) -> str | None:
        return self._uri
