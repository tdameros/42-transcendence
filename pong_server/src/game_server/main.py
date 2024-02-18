import asyncio
import logging
import os
import sys
from typing import Optional

from ClientManager import ClientManager
from EventHandler import EventHandler
from Game.GameManager import GameManager
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


async def main() -> int:
    try:
        setup_logging(f'Game Server {os.getpid()}: ')
        logging.getLogger('aiohttp').setLevel(logging.WARNING)
        logging.debug(f'Starting Game Server({os.getpid()})')

        players: list[Optional[int]] = [int(player) if player != 'None' else None
                                        for player in sys.argv[2:]]
        logging.info(f'Players: {players}')
        GameManager.init(players)

        Server.init(background_task)
        ClientManager.init([player for player in players if player is not None])
        EventHandler.init()
        port: int = await Server.start('0.0.0.0',
                                       int(os.getenv('PONG_GAME_SERVERS_MIN_PORT')),
                                       int(os.getenv('PONG_GAME_SERVERS_MAX_PORT')))

        print(f'port: {port}')
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
