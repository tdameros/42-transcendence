import socketio
from aiohttp import web

from src.redirection_server.Game import Game
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string

#      dict[GameID, Game]
games: dict[str, Game] = {'game_1': Game(['player_1'])}
# TODO get all games from server

sids_to_disconnect = []
is_sids_to_disconnect_being_used = False
time_to_wait_for_sids_to_disconnect = 1
sid_being_disconnected = ''

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)


def get_game_id(query_string) -> str:
    game_id = query_string.get('game_id')
    if game_id is None:
        raise Exception('game_id was not found in query string')
    if not isinstance(game_id, str):
        raise Exception('game_id must be a string')
    if len(game_id) == 0:
        raise Exception('game_id may not be an empty string')
    if games.get(game_id) is None:
        raise Exception(f'game {game_id} does not exist')
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


def get_game(game_id: str, user_id: str) -> Game:
    game = games.get(game_id)
    if game is None:
        raise Exception(f'Game: {game_id} was not found')
    if user_id not in game.get_clients():
        raise Exception(f'User {user_id} is not part of game {game_id}')
    return game


def create_game_server_if_needed(game: Game):
    if not game.was_server_created():
        game.create_server()


async def add_sid_to_sids_to_disconnect(sid):
    global is_sids_to_disconnect_being_used
    while is_sids_to_disconnect_being_used:
        print('add_sid_to_sids_to_disconnect loop')
        await sio.sleep(time_to_wait_for_sids_to_disconnect)

    is_sids_to_disconnect_being_used = True
    sids_to_disconnect.append(sid)
    is_sids_to_disconnect_being_used = False


@sio.event
async def connect(sid, environ, auth):
    print(f'{sid} connected')
    try:
        query_string = get_query_string(environ)
        json_web_token = get_json_web_token(query_string)
        game_id = get_game_id(query_string)
        update_game_database()
        game = get_game(game_id, json_web_token['user_id'])
        create_game_server_if_needed(game)
        await emit(sio, 'game_server_uri', sid, game.get_uri())
    except Exception as e:
        await emit(sio, 'error', sid, str(e))

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
        sid_being_disconnected = ''
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
