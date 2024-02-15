from .logging import setup_logging
from .server import Server

if __name__ == '__main__':
    setup_logging()
    server = Server()
    server.start()
