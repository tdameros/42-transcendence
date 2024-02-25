import asyncio
import logging
import os
import ssl
import sys
from typing import Optional

from ClientManager import ClientManager
from EventHandler import EventHandler
from Game.GameManager import GameManager
from PostSender.PostSender import PostSender
from Server import Server
from shared_code.setup_logging import setup_logging


async def background_task():
    try:
        while not ClientManager.have_all_players_joined():
            # TODO Add a time out and make the players that don't join forfeit
            #      their games
            await Server.sio.sleep(.3)

        await GameManager.start_game()  # Blocks till the game is over

        await Server.sio.sleep(10)  # Give the clients time to receive the game_over event

        await ClientManager.disconnect_all_users()

        Server.should_stop = True

    except Exception as e:
        try:  # Attempt graceful exit
            print(f'Error: in background_task: {e}')
            """ Do not use logging! This should always be printed as the game
                creator may read it """
            logging.critical(f'Error in background_task: {e}')
            Server.exit_code = 2
            Server.should_stop = True
            await Server.sio.sleep(30)
            # If everything goes well, the process will exit(exit_code) before this line
            # (see main())
            exit(3)
        except Exception:  # Graceful exit failed!
            exit(4)


async def init():
    setup_logging(f'Game Server {os.getpid()}: ')
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.debug(f'Starting Game Server({os.getpid()})')

    players: list[Optional[int]] = [int(player) if player != 'None' else None
                                    for player in sys.argv[3:]]
    logging.info(f'Players: {players}')

    PostSender.init(sys.argv[2])
    await GameManager.init(int(sys.argv[1]), players)
    Server.init(background_task)
    ClientManager.init([player for player in players if player is not None])
    EventHandler.init()


def get_ssl_context() -> ssl.SSLContext:
    path: str = os.getenv('PATH_TO_SSL_CERTS')

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(f'{path}certificate.crt', f'{path}private.key')

    return ssl_context


async def main() -> int:
    try:
        await init()
        await Server.start('0.0.0.0',
                           int(os.getenv('PONG_GAME_SERVERS_MIN_PORT')),
                           int(os.getenv('PONG_GAME_SERVERS_MAX_PORT')),
                           get_ssl_context())

        print(f'port: {Server.PORT}')
        """ Do not use logging! This should always be printed as the game
            creator will read it """
        sys.stdout.flush()
    except Exception as e:
        print(f'Error: {str(e)}')
        """ Do not use logging! This should always be printed as the game
            creator will read it """
        sys.stdout.flush()
        logging.critical(f'failed to start: {str(e)}')
        return 1

    exit_code: int = await Server.wait_for_server_to_stop()
    logging.info(f'Exiting with code {exit_code}')
    return exit_code


if __name__ == '__main__':
    exit(asyncio.run(main()))
