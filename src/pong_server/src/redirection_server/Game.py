import subprocess


class Game(object):
    def __init__(self, clients: list[str]):
        self._clients: list[str] = clients
        self._uri: str | None = None

    def create_server(self):
        """ Can Raise Exception """

        process = subprocess.Popen(['python3', '-m', 'src.game_server'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        # TODO handle errors when the command doesn't work

        while process.poll() is None:
            line = process.stdout.readline()
            if self.parse_subprocess_line(line):
                return
        remaining_output = process.communicate()[0]
        for line in remaining_output.splitlines():
            if self.parse_subprocess_line(line):
                return
        raise Exception('Error creating game server: Undefined Error')
        # TODO handle errors when the server fails starting

    def parse_subprocess_line(self, line):
        """ Can Raise Exception """

        if not line:
            return False

        if line.startswith('uri: '):
            self._uri = line[len('uri: '):-1]
            print(f'Created game server with uri {self._uri}')
            return True

        if line.startswith('Error: '):
            raise Exception(f'Error creating game server: '
                            f'{line[len('Error: '):-1]}')

        return False

    def was_server_created(self) -> bool:
        return self._uri is not None

    def get_clients(self) -> list[str]:
        return self._clients

    def get_uri(self) -> str | None:
        return self._uri
