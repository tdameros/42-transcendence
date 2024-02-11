import logging

import socketio
from aiohttp import web

from Game import Game
from RefuseConnection import RefuseConnection
from SendURI import SendURI
from shared_code.get_json_web_token import get_json_web_token
from shared_code.get_query_string import get_query_string
from shared_code.setup_logging import setup_logging

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

number_of_test_players = 2  # TODO remove this

# TODO get all games from server
#      dict[GameID, Game]
games: dict[int, Game] = {
    1: Game([nb for nb in range(number_of_test_players)])
}


def get_game_id(query_string) -> int:
    game_id = query_string.get('game_id')
    if game_id is None:
        raise Exception('game_id was not found in query string')
    if not isinstance(game_id, int):
        raise Exception('game_id must be an int')
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


def get_game(game_id: int, user_id: int) -> Game:
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
def connect(sid, environ, auth):
    logging.info(f'{sid} connected')

    try:
        query_string = get_query_string(environ)
        json_web_token = get_json_web_token(query_string)
        game_id = get_game_id(query_string)
        update_game_database()
        game = get_game(game_id, json_web_token['user_id'])
        create_game_server_if_needed(game)
    except Exception as e:
        raise RefuseConnection(str(e))
    global i  # TODO remove this line
    i += 1  # TODO remove this line
    # TODO send game.get_uri() instead of
    #      [game.get_uri(), str(i % number_of_test_players)]
    #      It is like this for now so that I can run test, the i % number_of_test_players
    #      serves as the client nickname for the game server
    raise SendURI([game.get_uri(), i % number_of_test_players])


@sio.event
def disconnect(sid):
    pass


# This function is for disconnecting clients that don't disconnect themselves
#   (Should never happen with the official client, might happen with a poorly
#   coded unofficial client or a malicious client)
async def background_task():
    while True:
        await sio.sleep(3)
        # TODO check for ghost games


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    setup_logging()
    web.run_app(app,
                host='0.0.0.0',
                port=4242,
                access_log=None)
    # Port is hardcoded because this is the redirection server so we don't care
    # (The redirection server will soon be deleted)
