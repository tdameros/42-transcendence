from src.shared_code.log import log

TIME_TO_WAIT_FOR_SIDS_TO_DISCONNECT = 1


class UserKicker(object):
    def __init__(self, sio):
        self._kick_queue = []
        self._is_kick_queue_being_used = False
        self._sio = sio
        self._sid_being_kicked = ''

    async def add_sid_to_kick_queue(self, sid):
        while self._is_kick_queue_being_used:
            await self._sio.sleep(TIME_TO_WAIT_FOR_SIDS_TO_DISCONNECT)

        self._is_kick_queue_being_used = True
        self._kick_queue.append(sid)
        self._is_kick_queue_being_used = False

    async def remove_sid_from_kick_queue(self, sid):
        if sid == self._sid_being_kicked:
            return

        log(f'{sid} disconnected')

        while self._is_kick_queue_being_used:
            await self._sio.sleep(TIME_TO_WAIT_FOR_SIDS_TO_DISCONNECT)

        self._is_kick_queue_being_used = True
        self._kick_queue = [elem for elem in self._kick_queue if elem != sid]
        self._is_kick_queue_being_used = False

    async def kick_users(self):
        while self._is_kick_queue_being_used:
            await self._sio.sleep(TIME_TO_WAIT_FOR_SIDS_TO_DISCONNECT)

        self._is_kick_queue_being_used = True
        for sid in self._kick_queue:
            log(f'Disconnecting {sid}, they did not disconnect themself')
            self._sid_being_kicked = sid
            await self._sio.disconnect(sid)
        self._sid_being_kicked = ''
        self._kick_queue.clear()
        self._is_kick_queue_being_used = False
