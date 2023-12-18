import asyncio
from aiohttp import web
import socketio
from typing import AnyStr
from urllib.parse import unquote
import json

from Game import Game

#      Dict[GameID, Game]
games: dict[str, Game] = {"game_1": Game(["player_1"])}
# TODO get all games from server

sids_to_disconnect = []
is_sids_to_disconnect_being_used = False

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

    query_string = unquote(query_string).split("=undefined")
    if len(query_string) == 0:
        await sio.emit("error",
                       f"invalid query string: {environ.get("QUERY_STRING")}",
                       room=sid)
        return None

    query_string = query_string[0]

    try:
        return json.loads(query_string)
    except json.JSONDecodeError as e:
        await sio.emit("error",
                       f"Failed to parse query string: {e}",
                       room=sid)
        return None


async def get_json_web_token(sid, query_string):
    json_web_token = query_string.get("json_web_token", None)
    if json_web_token is None:
        await sio.emit("error",
                       "json_web_token was not found in query string",
                       room=sid)
        return None
    # TODO check jwt validity
    return json_web_token


async def get_user_id_from_json_web_token(sid, token) -> str | None:
    user_id = token.get("user_id", None)
    if user_id is None:
        await sio.emit("error",
                       "json_web_token did not contain a user_id field",
                       room=sid)
        return None
    if not isinstance(user_id, str):
        await sio.emit("error",
                       "json_web_token user_id field must be a string",
                       room=sid)
        return None
    return user_id


async def get_game_id(sid, query_string) -> str | None:
    game_id = query_string.get("game_id", None)
    if game_id is None:
        await sio.emit("error",
                       "game_id was not found in query string",
                       room=sid)
        return None
    if len(game_id) == 0:
        return None
    if not isinstance(game_id, str):
        await sio.emit("error",
                       "json_web_token game_id field must be a string",
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
    await sio.emit("error", f"Game: {game_id} was not found", room=sid)
    return None


async def redirect_user(sid, user_id: str, game: Game, game_id: str):
    if user_id not in game.get_clients():
        await sio.emit("error",
                       f"User {user_id} is not part of game {game_id}",
                       room=sid)
        return
    if not game.was_server_created():
        game.create_server()
        if not game.was_server_created():
            await sio.emit("error",
                           f"Failed to create server for game {game_id}",
                           room=sid)
            return
    await sio.emit("game_server_uri", game.get_uri(), room=sid)


@sio.event
async def connect(sid, environ, auth):
    print(f"{sid} connected")
    query_string = await get_query_string(sid, environ)
    if query_string is None:
        sids_to_disconnect.append(sid)
        return True

    json_web_token = await get_json_web_token(sid, query_string)
    if json_web_token is None:
        sids_to_disconnect.append(sid)
        return True

    user_id = await get_user_id_from_json_web_token(sid, json_web_token)
    if user_id is None:
        sids_to_disconnect.append(sid)
        return True

    game_id = await get_game_id(sid, query_string)
    if game_id is None:
        sids_to_disconnect.append(sid)
        return True

    update_game_database()

    game_client_is_in = await get_game_client_is_in(sid, game_id)
    if game_client_is_in is None:
        sids_to_disconnect.append(sid)
        return True

    await redirect_user(sid, user_id, game_client_is_in, game_id)
    sids_to_disconnect.append(sid)
    return True


@sio.event
async def disconnect(sid):
    print(f"{sid} disconnected")
    global sids_to_disconnect
    global is_sids_to_disconnect_being_used

    while is_sids_to_disconnect_being_used:
        await asyncio.sleep(1)

    is_sids_to_disconnect_being_used = True
    sids_to_disconnect = [elem for elem in sids_to_disconnect if elem != sid]
    is_sids_to_disconnect_being_used = False


# This function is for disconnecting clients that don't disconnect themselves
# (Should never happen with the official client, might happen with a poorly
# coded unofficial client or a malicious client)
async def background_task():
    global is_sids_to_disconnect_being_used

    while True:
        await asyncio.sleep(3)
        while is_sids_to_disconnect_being_used:
            await asyncio.sleep(1)
        is_sids_to_disconnect_being_used = True
        if len(sids_to_disconnect) != 0:
            print("disconnecting all sids")
        for sid in sids_to_disconnect:
            print(f"Disconnecting {sid}, they did not disconnect themself")
            await sio.disconnect(sid)
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
