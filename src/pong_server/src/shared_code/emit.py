import src.shared_code.settings as settings


async def emit(sio, event, message, room):
    if settings.DEBUG:
        print(f'emit("{event}", "{message}", room="{room}")')
    await sio.emit(event, message, room=room)
