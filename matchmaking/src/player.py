from time import time


class Player:

    def __init__(self, sid, user_id, elo):
        self.sid = sid
        self.user_id = user_id
        self.elo = elo
        self.timestamp = time()
