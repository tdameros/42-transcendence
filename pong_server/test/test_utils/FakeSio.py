class EmittedEvent(object):
    def __init__(self,
                 event: str,
                 room: str,
                 message: any,
                 skip_sid: str | None = None):
        self.event: str = event
        self.message: str = message
        self.room: str = room
        self.skip_sid: str = skip_sid

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (self.event == other.event
                and self.message == other.message
                and self.room == other.room
                and self.skip_sid == other.skip_sid)

    def __repr__(self):
        return (f'EmittedEvent('
                f'event={self.event}, '
                f'message={self.message}, '
                f'room={self.room}, '
                f'skip_sid={self.skip_sid})')


class FakeSio(object):

    def __init__(self):
        self.emitted_events: list[EmittedEvent] = []

    async def emit(self,
                   event: str,
                   message: any,
                   room: str,
                   skip_sid: str | None):
        self.emitted_events.append(EmittedEvent(event,
                                                room,
                                                message,
                                                skip_sid))
