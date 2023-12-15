class Game(object):
    def __init__(self, clients: list[str]):
        self._clients: list[str] = clients
        self._was_server_created: bool = False
        self._ip: str | None = None
        self._port: str | None = None

    def create_server(self):
        pass

    def was_server_created(self):
        return self._was_server_created

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port
