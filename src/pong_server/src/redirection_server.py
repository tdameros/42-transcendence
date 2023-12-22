from aiohttp import web
import socketio
from typing import AnyStr
from urllib.parse import unquote
import json

from Game import Game

#      dict[GameID, Game]
games: dict[str, Game] = {'game_1': Game(['player_1'])}
# TODO get all games from server

sids_to_disconnect = []
is_sids_to_disconnect_being_used = False
time_to_wait_for_sids_to_disconnect = 1
sid_being_disconnected = ""

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)


async def add_sid_to_sids_to_disconnect(sid):
    global is_sids_to_disconnect_being_used
    while is_sids_to_disconnect_being_used:
        print('add_sid_to_sids_to_disconnect loop')
        await sio.sleep(time_to_wait_for_sids_to_disconnect)

    is_sids_to_disconnect_being_used = True
    sids_to_disconnect.append(sid)
    is_sids_to_disconnect_being_used = False


async def get_query_string(sid, environ) -> dict[AnyStr, list[AnyStr]] | None:
    query_string = environ.get('QUERY_STRING', None)
    if query_string is None:
        await sio.emit('error',
                       'environ does not contain query string',
                       room=sid)
        return None

    query_string = unquote(query_string).split('=undefined')
    if len(query_string) == 0:
        await sio.emit('error',
                       f'invalid query string: {environ.get('QUERY_STRING')}',
                       room=sid)
        return None

    query_string = query_string[0]

    try:
        return json.loads(query_string)
    except json.JSONDecodeError as e:
        await sio.emit('error',
                       f'Failed to parse query string: {e}',
                       room=sid)
        return None


async def get_json_web_token(sid, query_string):
    json_web_token = query_string.get('json_web_token', None)
    if json_web_token is None:
        await sio.emit('error',
                       'json_web_token was not found in query string',
                       room=sid)
        return None
    # TODO check jwt validity
    return json_web_token


async def get_user_id_from_json_web_token(sid, token) -> str | None:
    user_id = token.get('user_id', None)
    if user_id is None:
        await sio.emit('error',
                       'json_web_token did not contain a user_id field',
                       room=sid)
        return None
    if not isinstance(user_id, str):
        await sio.emit('error',
                       'json_web_token user_id field must be a string',
                       room=sid)
        return None
    return user_id


async def get_game_id(sid, query_string) -> str | None:
    game_id = query_string.get('game_id', None)
    if game_id is None:
        await sio.emit('error',
                       'game_id was not found in query string',
                       room=sid)
        return None
    if len(game_id) == 0:
        return None
    if not isinstance(game_id, str):
        await sio.emit('error',
                       'game_id must be a string',
                       room=sid)
        return None
    if games.get(game_id) is None:
        await sio.emit('error',
                       f'game {game_id} does not exist',
                       room=sid)
        return None
    return game_id


def update_game_database():
    remove_finished_games()
    get_newly_created_games()


def remove_finished_games():
    # TODO request finished games from server and remove them from games
    pass


def get_newly_created_games():
    # TODO request newly created games from server and add them to games
    pass


async def get_game_client_is_in(sid, game_id: str) -> Game | None:
    game_client_is_in = games.get(game_id, None)
    if game_client_is_in is not None:
        return game_client_is_in
    await sio.emit('error', f'Game: {game_id} was not found', room=sid)
    return None


async def redirect_user(sid, user_id: str, game: Game, game_id: str):
    if user_id not in game.get_clients():
        await sio.emit('error',
                       f'User {user_id} is not part of game {game_id}',
                       room=sid)
        return
    if not game.was_server_created():
        game.create_server()
        if not game.was_server_created():
            await sio.emit('error',
                           f'Failed to create server for game {game_id}',
                           room=sid)
            return
    await sio.emit('game_server_uri', game.get_uri(), room=sid)


@sio.event
async def connect(sid, environ, auth):
    print(f'{sid} connected')
    query_string = await get_query_string(sid, environ)
    if query_string is None:
        await add_sid_to_sids_to_disconnect(sid)
        return True

    json_web_token = await get_json_web_token(sid, query_string)
    if json_web_token is None:
        await add_sid_to_sids_to_disconnect(sid)
        return True

    user_id = await get_user_id_from_json_web_token(sid, json_web_token)
    if user_id is None:
        await add_sid_to_sids_to_disconnect(sid)
        return True

    game_id = await get_game_id(sid, query_string)
    if game_id is None:
        await add_sid_to_sids_to_disconnect(sid)
        return True

    update_game_database()

    game_client_is_in = await get_game_client_is_in(sid, game_id)
    if game_client_is_in is None:
        await add_sid_to_sids_to_disconnect(sid)
        return True

    await redirect_user(sid, user_id, game_client_is_in, game_id)
    await add_sid_to_sids_to_disconnect(sid)
    return True


@sio.event
async def disconnect(sid):
    if sid == sid_being_disconnected:
        return

    print(f'{sid} disconnected')

    global is_sids_to_disconnect_being_used
    while is_sids_to_disconnect_being_used:
        print('disconnect loop')
        await sio.sleep(time_to_wait_for_sids_to_disconnect)

    is_sids_to_disconnect_being_used = True
    global sids_to_disconnect
    sids_to_disconnect = [elem for elem in sids_to_disconnect if elem != sid]
    is_sids_to_disconnect_being_used = False


# This function is for disconnecting clients that don't disconnect themselves
# (Should never happen with the official client, might happen with a poorly
# coded unofficial client or a malicious client)
async def background_task():
    global is_sids_to_disconnect_being_used
    global sid_being_disconnected

    while True:
        await sio.sleep(3)

        while is_sids_to_disconnect_being_used:
            print('background_task loop')
            await sio.sleep(time_to_wait_for_sids_to_disconnect)

        is_sids_to_disconnect_being_used = True
        for sid in sids_to_disconnect:
            print(f'Disconnecting {sid}, they did not disconnect themself')
            sid_being_disconnected = sid
            await sio.disconnect(sid)
        sid_being_disconnected = ""
        sids_to_disconnect.clear()
        is_sids_to_disconnect_being_used = False


# The app arguments is not used but is required
# for app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    # web.run_app(app, port=4242)
    web.run_app(app, host='localhost', port=4242)
