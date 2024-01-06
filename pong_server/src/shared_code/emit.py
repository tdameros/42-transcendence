from src.shared_code.log import log


async def emit(sio, event, room, message):
    log(f"\tsio.emit('{event}', '{message}', room='{room}')")
    await sio.emit(event, message, room=room)
