import logging

import socketio
from aiohttp import web

from src.redirection_server.Game import Game
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string
from src.shared_code.setup_logging import setup_logging
from src.shared_code.UserKicker import UserKicker

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)

user_kicker = UserKicker(sio)

# TODO get all games from server
#      dict[GameID, Game]
games: dict[str, Game] = {'game_1': Game(['0', '1'])}


def get_game_id(query_string) -> str:
    game_id = query_string.get('game_id')
    if game_id is None:
        raise Exception('game_id was not found in query string')
    if not isinstance(game_id, str):
        raise Exception('game_id must be a string')
    if len(game_id) == 0:
        raise Exception('game_id must not be empty')
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
        raise Exception(f'Game {game_id} does not exist')
    if user_id not in game.get_clients():
        raise Exception(f'User {user_id} is not part of game {game_id}')
    return game


def create_game_server_if_needed(game: Game):
    if not game.was_server_created():
        game.create_server()


i = 0  # TODO remove me


@sio.event
async def connect(sid, environ, auth):
    logging.info(f'{sid} connected')

    try:
        query_string = get_query_string(environ)
        json_web_token = get_json_web_token(query_string)
        game_id = get_game_id(query_string)
        update_game_database()
        game = get_game(game_id, json_web_token['user_id'])
        create_game_server_if_needed(game)
        global i  # TODO remove this line
        # TODO send game.get_uri() instead of [game.get_uri(), str(i % 2)]
        #      It is like this for now so that I can run test, the i % 2
        #      serves as the client nickname for the game server
        await emit(sio, 'game_server_uri', sid, [game.get_uri(), str(i % 2)])
        i += 1  # TODO remove this line
    except Exception as e:
        await emit(sio, 'error', sid, str(e))

    user_kicker.add_sid_to_kick_queue(sid)


@sio.event
async def disconnect(sid):
    user_kicker.remove_sid_from_kick_queue(sid)


# This function is for disconnecting clients that don't disconnect themselves
#   (Should never happen with the official client, might happen with a poorly
#   coded unofficial client or a malicious client)
async def background_task():
    while True:
        await sio.sleep(3)
        await user_kicker.kick_users()


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    setup_logging()
    # web.run_app(app, port=4242)
    web.run_app(app, host='localhost', port=4242, access_log=None)
