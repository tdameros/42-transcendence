from src.shared_code.log import log


async def emit(sio, event, room, message, skip_sid=None):
    log(f"\tsio.emit('{event}', '{message}', room='{room}')")
    await sio.emit(event, message, room=room)
