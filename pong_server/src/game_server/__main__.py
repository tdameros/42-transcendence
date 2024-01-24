import logging
import sys

import socketio
from aiohttp import web
from socketio.exceptions import ConnectionRefusedError

from src.game_server.Clock import Clock
from src.game_server.Game import Game
from src.game_server.print_server_uri import print_server_uri
from src.game_server.update_player_movement_and_position import \
    update_player_direction_and_position
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string
from src.shared_code.setup_logging import setup_logging

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)

game: Game | None = None


async def add_user_to_game(user_id: str, sid: str):
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


async def background_task():
    await print_server_uri(sio)

    await wait_for_all_players_to_join()

    clock = Clock()
    while True:
        game.get_scene().update(clock.get_delta())
        await sio.sleep(0.1)


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    try:
        setup_logging()
        game = Game(sys.argv[1:])
        # web.run_app(app, port=4242)
        web.run_app(app, host='localhost', port=0, access_log=None)
    except Exception as e:
        print(f'Error: {e}')
        """ Do not use logging! This should always be printed as the redirection
            server will read it """
