import datetime
import logging

WAIT_TIME_BEFORE_KICK = 10


def enough_time_has_passed_to_kick_user(start_time: datetime.datetime):
    delta_to_kick = datetime.timedelta(seconds=WAIT_TIME_BEFORE_KICK)
    current_delta = datetime.datetime.now() - start_time
    return current_delta >= delta_to_kick


class UserKicker(object):
    def __init__(self, sio):
        #                 list[list[sid, time_when_added_to_queue]]
        self._kick_queue: list[list[str: datetime]] = []
        self._sio = sio
        self._sid_being_kicked: str = ''

    def add_sid_to_kick_queue(self, sid):
        self._kick_queue.append([sid, datetime.datetime.now()])

    def remove_sid_from_kick_queue(self, sid):
        if sid == self._sid_being_kicked:
            self._sid_being_kicked = ''
            return

        logging.info(f'{sid} disconnected')

        self._kick_queue = [
            elem for elem in self._kick_queue
            if elem[0] != sid
        ]

    async def kick_users(self):
        while len(self._kick_queue) > 0:
            if not enough_time_has_passed_to_kick_user(self._kick_queue[0][1]):
                return
            sid, timestamp = self._kick_queue.pop(0)
            logging.info(f'Disconnecting {sid}, they did not disconnect '
                         f'themself')
            self._sid_being_kicked = sid
            await self._sio.disconnect(sid)
