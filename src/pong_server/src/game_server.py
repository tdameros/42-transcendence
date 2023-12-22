import asyncio
from aiohttp import web
import socketio
import subprocess
import os
import socket
from typing import AnyStr
from urllib.parse import unquote
import json

sio = socketio.AsyncServer(cors_allowed_origins=['http://localhost:5173'])
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ, auth):
    print(f'{sid} connected')
    return True


@sio.event
async def disconnect(sid):
    print(f'{sid} disconnected')


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

    print(get_server_uri())

    while True:
        await sio.sleep(3)
        # print('background task')


# The app arguments is not used but is required
# for app.on_startup.append(start_background_task)
async def start_background_task(app):
    sio.start_background_task(background_task)


app.on_startup.append(start_background_task)
if __name__ == '__main__':
    # web.run_app(app, port=4242)
    web.run_app(app, host='localhost', port=0)
