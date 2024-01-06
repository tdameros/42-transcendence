import sys


class Game(object):
    def __init__(self):
        #                   list[user_id]
        self._players_list: list[str] = []

        #                 dict[sid: user_id]
        self._player_map: dict[str: str] = {}

        #              dict[user_id: sid]
        self._sid_map: dict[str: str] = {}

    def init_game_from_argv(self):
        for arg in sys.argv[1:]:
            self._players_list.append(arg)

        if len(self._players_list) == 0:
            raise Exception("Game is empty")
        if len(self._players_list) % 2 == 1:
            raise Exception(f"Game has an odd number of players "
                            f"(number of players: {len(self._players_list)})")

    def is_user_part_of_game(self, user_id: str) -> bool:
        return user_id in self._players_list

    def get_user_sid(self, user_id: str) -> str:
        return self._sid_map.get(user_id)

    def add_user(self, user_id: str, sid: str):
        self._player_map[sid] = user_id
        self._sid_map[user_id] = sid

    def remove_user(self, sid: str):
        user_id = self._player_map.pop(sid)
        if user_id is not None:
            del self._sid_map[user_id]
