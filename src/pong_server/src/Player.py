class Player(object):
    def __init__(self, query, sid: str):
        self._id = query.get("player_id", [''])[0]
        self._sid = sid
        self._game = None

    def get_id(self) -> str:
        return self._id

    def get_sid(self) -> str:
        return self._sid

    async def join_game(self, sio, game):
        self._game = game
        await game.add_player(sio, self)
