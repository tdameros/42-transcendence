import logging

import socketio
from aiohttp import web

from src.game_server import rooms
from src.game_server.Clock import Clock
from src.game_server.Game import Game
from src.game_server.print_server_uri import print_server_uri
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string
from src.shared_code.setup_logging import setup_logging
from src.shared_code.UserKicker import UserKicker

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)

game: Game = Game()

user_kicker = UserKicker(sio)


async def add_user_to_game(user_id: str, sid: str):
    if not game.is_user_part_of_game(user_id):
        raise Exception('You are not part of this game')

    previous_sid = game.get_user_sid(user_id)
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
            await emit(sio, 'scene', sid, game.get_scene().to_json())
    except Exception as e:
        await emit(sio, 'error', sid, str(e))
        user_kicker.add_sid_to_kick_queue(sid)


@sio.event
async def disconnect(sid):
    await game.remove_user(sid, sio)

    user_kicker.remove_sid_from_kick_queue(sid)


async def background_task():
    await print_server_uri(sio)

    while not game.have_all_players_joined():
        # TODO Add a time out and make the players that don't join forfeit
        #      their games
        await sio.sleep(.3)

    await emit(sio, 'scene', rooms.ALL_PLAYERS, game.get_scene().to_json())
    game.has_started = True

    clock = Clock()
    while True:
        game.get_scene().update(clock.get_delta())
        await sio.sleep(0.1)
        await user_kicker.kick_users()


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    try:
        setup_logging()
        game.init_game_from_argv()
        # web.run_app(app, port=4242)
        web.run_app(app, host='localhost', port=0, access_log=None)
    except Exception as e:
        print(f'Error: {e}')
        """ Do not use logging! This should always be printed as the redirection
            server will read it """
