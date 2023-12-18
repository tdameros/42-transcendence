class Game(object):
    def __init__(self, clients: list[str]):
        self._clients: list[str] = clients
        self._uri: str | None = None

    def create_server(self):
        print("Created server")

    def was_server_created(self) -> bool:
        return self._uri is not None

    def get_clients(self) -> list[str]:
        return self._clients

    def get_uri(self) -> str | None:
        return self._uri
