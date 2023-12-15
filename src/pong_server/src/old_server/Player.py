class Player(object):
    def __init__(self, query, sid: str):
        self._id = query.get("player_id", [''])[0]
        self._sid = sid
        self._game = None
        self._is_connected = True

    def get_id(self) -> str:
        return self._id

    def get_sid(self) -> str:
        return self._sid

    async def join_game(self, sio, game):
        self._game = game
        await game.add_player(sio, self)

    def is_connected(self):
        return self._is_connected

    def disconnect(self):
        self._is_connected = False

    async def set_movement(self, sio, movement):
        if self._game is None:
            return

        await self._game.set_player_movement(sio, self, movement)

    def get_game(self):
        return self._game
