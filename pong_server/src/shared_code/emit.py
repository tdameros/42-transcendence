import logging

import socketio


async def emit(sio: socketio.AsyncServer,
               event: str,
               room: str,
               message: any,
               skip_sid: str | None = None):
    logging.info(f"emitting: event='{event}', message='{message}', room='{room}'"
                 f'{f", skip_sid='{skip_sid}'" if skip_sid is not None else ''})')
    await sio.emit(event, message, room=room, skip_sid=skip_sid)
