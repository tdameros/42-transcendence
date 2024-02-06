import asyncio
import logging
import os
import sys

import socketio
from aiohttp import web
from socketio.exceptions import ConnectionRefusedError

from src.game_server.Clock import Clock
from src.game_server.Game import Game
from src.game_server.update_player_movement_and_position import \
    update_player_direction_and_position
from src.shared_code import error_messages
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string
from src.shared_code.setup_logging import setup_logging

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)
should_exit = False
exit_code = 0

game: Game | None = None


async def add_user_to_game(user_id: int, sid: str):
    if not game.is_user_part_of_game(user_id):
        raise Exception('You are not part of this game')

    previous_sid: str | None = game.get_sid_from_user_id(user_id)
    if previous_sid is not None:
        await sio.disconnect(previous_sid)

    await game.add_user(user_id, sid, sio)


@sio.event
async def connect(sid, environ, auth):
    logging.info(f'{sid} connected')

    try:
        query_string = get_query_string(environ)
        json_web_token = get_json_web_token(query_string)
        await add_user_to_game(json_web_token['user_id'], sid)
        if game.has_started:
            await emit(sio, 'scene', sid,
                       {'scene': game.get_scene().to_json(),
                        'player_location': game.get_player_location(sid).to_json()})
    except Exception as e:
        raise ConnectionRefusedError(str(e))


@sio.event
async def disconnect(sid):
    await game.remove_user(sid, sio)


@sio.event
async def update_player(sid, player_data):
    try:
        client_player_position = player_data['client_player_position']
        direction = player_data['direction']
    except KeyError:
        return
    await update_player_direction_and_position(sio,
                                               sid,
                                               game,
                                               client_player_position,
                                               direction)


async def wait_for_all_players_to_join():
    while not game.have_all_players_joined():
        # TODO Add a time out and make the players that don't join forfeit
        #      their games
        await sio.sleep(.3)

    scene = game.get_scene().to_json()
    for player in game.PLAYERS_LIST:
        player_sid = game.get_sid_from_user_id(player)
        player_location = game.get_player_location(player_sid)
        if player_sid is not None:
            await emit(sio, 'scene', player_sid,
                       {'scene': scene,
                        'player_location': player_location.to_json()})
    game.has_started = True


async def game_loop():
    clock = Clock()
    while True:
        await game.get_scene().update(sio, clock.get_delta())
        await sio.sleep(0.01)


async def background_task():
    try:
        await wait_for_all_players_to_join()

        await game_loop()

    except Exception as e:
        try:  # Attempt graceful exit
            print(f'Error: in background_task: {e}')
            """ Do not use logging! This should always be printed as the game
                creator will read it """
            logging.critical(f'Error in background_task: {e}')
            global exit_code
            global should_exit
            exit_code = 2
            should_exit = True
            await sio.sleep(30)
            # If everything goes well, the process will exit(exit_code) before this line
            # (see main())
            exit(3)
        except Exception:  # Graceful exit failed!
            exit(4)


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)


async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()

    start_port = int(os.getenv('PONG_GAME_SERVERS_MIN_PORT'))
    end_port = int(os.getenv('PONG_GAME_SERVERS_MAX_PORT'))
    logging.debug(f'start_port: {start_port}, end_port: {end_port}')

    for port in range(start_port, end_port + 1):
        try:
            server = web.TCPSite(runner, '0.0.0.0', port)
            await server.start()
            return port
        except OSError:
            continue

    raise Exception(error_messages.NO_AVAILABLE_PORTS)


async def main():
    try:
        setup_logging(f'Game Server({os.getpid()}): ')
        logging.debug(f'Starting Game Server({os.getpid()})')

        global game
        game = Game(sys.argv[1:])

        port = await start_server()
        uri = f'http://localhost:{port}'  # TODO should be 42.shiftcode.fr in prod
        print(f'uri: {uri}')
        """ Do not use logging! This should always be printed as the redirection
            server will read it """
        sys.stdout.flush()
    except Exception as e:
        print(f'Error: {str(e)}')
        """ Do not use logging! This should always be printed as the game
            creator will read it """
        sys.stdout.flush()
        logging.error(f'Game Server({os.getpid()}) failed to open: {str(e)}')
        exit(1)

    logging.info(f'Game Server({os.getpid()}) started with uri {uri}')

    while True:
        await sio.sleep(5)
        if should_exit:  # set to True by background_task
            exit(exit_code)


if __name__ == '__main__':
    asyncio.run(main())
