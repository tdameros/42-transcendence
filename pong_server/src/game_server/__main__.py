import os
import subprocess
import sys

import socketio
from aiohttp import web
from src.game_server.Game import Game
from src.shared_code.emit import emit
from src.shared_code.get_json_web_token import get_json_web_token
from src.shared_code.get_query_string import get_query_string
from src.shared_code.log import log
from src.shared_code.UserKicker import UserKicker

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)

game: Game = Game()

user_kicker = UserKicker(sio)


async def add_user_to_game(user_id: str, sid: str):
    if not game.is_user_part_of_game(user_id):
        raise Exception("You are not part of this game")

    previous_sid = game.get_user_sid(user_id)
    if previous_sid is not None:
        await sio.disconnect(previous_sid)

    game.add_user(user_id, sid)


@sio.event
async def connect(sid, environ, auth):
    log(f'{sid} connected')

    try:
        query_string = get_query_string(environ)
        json_web_token = get_json_web_token(query_string)
        await add_user_to_game(json_web_token['user_id'], sid)
        # TODO Handle success
    except Exception as e:
        await emit(sio, 'error', sid, str(e))
        await user_kicker.add_sid_to_kick_queue(sid)


@sio.event
async def disconnect(sid):
    game.remove_user(sid)

    await user_kicker.remove_sid_from_kick_queue(sid)


def get_server_uri():
    command = (f'lsof -a -p {os.getpid()} -i6'
               f" | awk '{{print $9}}'"
               f' | tail -n +2')
    """ gets all open ipv6 sockets for current process
                | gets the column with the uri of the socket
                | removes the first line which only contains the name
                  of the column """

    return f"http://{subprocess.check_output(command, shell=True).decode()}"


async def background_task():
    await sio.sleep(0.1)
    """ The async sleep is here so that the server starts before
        this function is executed """

    print(f'uri: {get_server_uri()}')
    """ Do not use log()! This should always be printed as the redirection
        server will read it """

    sys.stdout.flush()
    while True:
        await sio.sleep(3)
        await user_kicker.kick_users()


# The app arguments is not used but is required by
#   app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    try:
        game.init_game_from_argv()
        # web.run_app(app, port=4242)
        web.run_app(app, host='localhost', port=0)
    except Exception as e:
        print(f"Error: {e}")
        """ Do not use log()! This should always be printed as the redirection
            server will read it """
