import logging
import subprocess
import threading

import src.shared_code.settings as settings


class _GameServerLogger(threading.Thread):
    def __init__(self, process: subprocess.Popen, server_uri: str):
        super().__init__(daemon=True)
        self._process: subprocess.Popen = process
        self._uri = server_uri

    def run(self):
        while self._process.poll() is None:
            line = self._process.stderr.readline()
            if len(line) > 0:
                print(f'\tServer({self._uri}): '
                      f'{line[:-1] if line[-1] == '\n' else line}')
        remaining_output = self._process.communicate()[0]
        for line in remaining_output.splitlines():
            if len(line) > 0:
                print(f'\tServer({self._uri}): '
                      f'{line[:-1] if line[-1] == '\n' else line}')
        logging.info(f'\tServer({self._uri}) has stopped')


class Game(object):
    def __init__(self, clients: list[str]):
        self._clients: list[str] = clients
        self._uri: str | None = None

    def create_server(self):
        """ Can Raise Exception """

        process: subprocess.Popen = self._start_server()

        output: list[str] = []
        while process.poll() is None:
            line = process.stdout.readline()
            if self._parse_subprocess_line(line):
                self._start_game_server_logger(process, self._uri)
                return
            if settings.LOG_LEVEL != settings.NO_LOGS:
                output.append(line)
        remaining_output = process.communicate()[0]
        for line in remaining_output.splitlines():
            self._parse_subprocess_line(line)  # Will throw if the server
            #                                    printed an error message
            if settings.LOG_LEVEL != settings.NO_LOGS:
                output.append(line)

        Game._print_program_output_on_error(output)

        raise Exception('Error creating game server: undefined error')

    def _start_server(self) -> subprocess.Popen:
        try:
            command = ['python3', '-m', 'src.game_server']
            for player in self._clients:
                command.append(player)
            return subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
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

    @staticmethod
    def _start_game_server_logger(process: subprocess.Popen, server_uri: str):
        if settings.LOG_LEVEL == settings.NO_LOGS:
            return
        game_server_logger = _GameServerLogger(process, server_uri)
        game_server_logger.start()

    @staticmethod
    def _print_program_output_on_error(output: list[str]):
        if settings.LOG_LEVEL == settings.NO_LOGS:
            return
        logging.error('\tError creating a new server, output:')
        for line in output:
            if len(line) > 0:
                logging.error(f'\t\t{line[:-1] if line[-1] == '\n' else line}')

    def was_server_created(self) -> bool:
        return self._uri is not None

    def get_clients(self) -> list[str]:
        return self._clients

    def get_uri(self) -> str | None:
        return self._uri
