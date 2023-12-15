import asyncio
from aiohttp import web
import socketio
from urllib.parse import parse_qs
from typing import AnyStr

from Game import Game

#      Dict[GameID, Game]
games: dict[str, Game] = {"game_1": Game(["player_1"])}
# TODO get all games from server

sio = socketio.AsyncServer(cors_allowed_origins=["http://localhost:5173"])
app = web.Application()
sio.attach(app)


async def get_query_string(sid, environ) -> dict[AnyStr, list[AnyStr]] | None:
    query_string = environ.get("QUERY_STRING", None)
    if query_string is None:
        await sio.emit("error",
                       "environ does not contain query string",
                       room=sid)
        return None
    return parse_qs(query_string)


async def get_json_web_token(sid, query_string):
    json_web_token = query_string.get("Json-Web-Token", None)
    if json_web_token is None:
        await sio.emit("error",
                       "Json-Web-Token was not found in query string",
                       room=sid)
        return None
    if len(json_web_token) == 0:
        await sio.emit("error",
                       "Json-Web-Token field is empty in query string",
                       room=sid)
        return None
    json_web_token = json_web_token[0]
    # TODO check jwt validity
    return json_web_token


async def get_user_name_from_json_web_token(sid, token) -> str | None:
    user_name = token.get("user_name", None)
    if user_name is None:
        await sio.emit("error",
                       "Json-Web-Token did not contain a user_name field",
                       room=sid)
        return None
    if not isinstance(user_name, str):
        await sio.emit("error",
                       "Json-Web-Token user_name field must be a string",
                       room=sid)
        return None
    return user_name


async def get_game_id(sid, query_string) -> str | None:
    game_id = query_string.get("game_id", None)
    if game_id is None:
        await sio.emit("error",
                       "game_id was not found in query string",
                       room=sid)
        return None
    if len(game_id) == 0:
        return None
    if not isinstance(game_id[0], str):
        await sio.emit("error",
                       "Json Web Token game_id field must be a string",
                       room=sid)
        return None
    return game_id[0]


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
    await sio.emit("error", f"Game: {game_id} was not found", room=sid)
    return None


async def redirect_user(sid, user_name: str, game: Game, game_id: str):
    if not game.was_server_created():
        game.create_server()
        if not game.was_server_created():
            await sio.emit("error",
                           f"Failed to create server for game {game_id}",
                           room=sid)
            return

    await sio.emit("game-server",
                   {"ip": game.get_ip(), "port": game.get_port()},
                   room=sid)


@sio.event
async def connect(sid, environ, auth):
    query_string = await get_query_string(sid, environ)
    if query_string is None:
        return False

    json_web_token = await get_json_web_token(sid, query_string)
    if json_web_token is None:
        return False

    user_name = await get_user_name_from_json_web_token(sid, json_web_token)
    if user_name is None:
        return False

    game_id = await get_game_id(sid, query_string)
    if game_id is None:
        return False

    update_game_database()

    game_client_is_in = await get_game_client_is_in(sid, game_id)
    if game_client_is_in is None:
        return False

    await redirect_user(sid, user_name, game_client_is_in, game_id)
    return False


@sio.event
def disconnect(sid):
    pass


if __name__ == '__main__':
    web.run_app(app, port=4242)
