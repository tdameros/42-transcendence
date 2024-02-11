from .server import Server
from .logging import setup_logging

if __name__ == '__main__':
    setup_logging()
    server = Server()
    server.start()
