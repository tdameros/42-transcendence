import src.shared_code.settings as settings


async def emit(sio, event, room, message):
    if settings.DEBUG:
        print(f'\tsio.emit("{event}", "{message}", room="{room}")')
    await sio.emit(event, message, room=room)
