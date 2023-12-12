from aiohttp import web
import socketio
from urllib.parse import parse_qs

from Server import Server

sio = socketio.AsyncServer(cors_allowed_origins=["http://localhost:5173"])
app = web.Application()
sio.attach(app)

server = Server(sio)


@sio.event
async def connect(sid, environ, auth):
    if False:  # TODO check json web token
        raise ConnectionRefusedError('authentication failed')
    query = parse_qs(environ["QUERY_STRING"])
    await server.register(sid, query)


@sio.event
async def move_up_pressed(sid, data):
    await server.set_player_movement(sid, sio, 9.)


@sio.event
async def move_down_pressed(sid, data):
    await server.set_player_movement(sid, sio, -9.)


@sio.event
async def move_up_released(sid, data):
    await server.set_player_movement(sid, sio, 0.)


@sio.event
async def move_down_released(sid, data):
    await server.set_player_movement(sid, sio, 0.)


@sio.event
async def disconnect(sid):
    print('disconnect ', sid)
    await server.disconnect(sid, sio)


if __name__ == '__main__':
    web.run_app(app, port=4242)
