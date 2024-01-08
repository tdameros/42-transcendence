import logging


async def emit(sio, event, room, message, skip_sid=None):
    logging.info(f"emitting: event='{event}', message='{message}', room='{room}'"
                 f'{f", skip_sid='{skip_sid}'" if skip_sid is not None else ''})')
    await sio.emit(event, message, room=room)
