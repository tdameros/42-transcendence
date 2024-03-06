import asyncio
import logging
from ssl import SSLContext
from typing import Optional

import socketio
from aiohttp import web

from shared_code import error_messages


class Server(object):
    sio: socketio.AsyncServer = socketio.AsyncServer(cors_allowed_origins='*')
    _app: web.Application = web.Application()
    _runner: web.AppRunner
    _is_running: bool = False
    PORT: int

    _background_task: callable

    should_stop: bool = False
    exit_code: int = 0

    @staticmethod
    def init(background_task: callable):
        Server.sio.attach(Server._app)
        Server._background_task = background_task
        Server._app.on_startup.append(Server._start_background_task)
        Server._runner = web.AppRunner(Server._app)

    @staticmethod
    async def start(host: str,
                    start_port: int,
                    end_port: int,
                    ssl_context: Optional[SSLContext] = None):
        if Server._is_running:
            raise Exception("Server is already running")

        await Server._runner.setup()

        logging.debug(f'start_port: {start_port}, end_port: {end_port}')

        for port in range(start_port, end_port + 1):
            try:
                server = web.TCPSite(Server._runner, host, port, ssl_context=ssl_context)
                await server.start()
                logging.info(f'started on port {port}')
                Server.PORT = port
                Server._is_running = True
                return
            except OSError:
                continue

        raise Exception(error_messages.NO_AVAILABLE_PORTS)

    @staticmethod
    async def wait_for_server_to_stop() -> int:
        while True:
            await Server.sio.sleep(5)
            if Server.should_stop:  # set to True by background task
                logging.debug('Cleaning up before exiting')
                await Server._app.shutdown()
                await Server._app.cleanup()
                await Server._runner.cleanup()
                return Server.exit_code

    @staticmethod
    async def emit(event: str,
                   room: str,
                   message: any,
                   skip_sid: str | None = None):
        logging.debug(f"emitting: event='{event}', message='{message}', room='{room}'"
                      f'{f", skip_sid='{skip_sid}'" if skip_sid is not None else ''})')
        await Server.sio.emit(event, message, room=room, skip_sid=skip_sid)

    @staticmethod
    async def _start_background_task(_app):
        Server.sio.start_background_task(Server._background_task)
