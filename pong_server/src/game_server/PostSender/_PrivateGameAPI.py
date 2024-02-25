from PostSender._ABaseAPI import ABaseAPI


class PrivateGameAPI(ABaseAPI):
    @staticmethod
    async def post_create_game(players: list[int], request_issuer: str) -> int:
        pass

    @staticmethod
    async def post_add_point(game_id: int, id_of_player_that_marked_a_point: int):
        pass

    @staticmethod
    async def post_end_game(game_id: int, winner_id: int):
        pass
