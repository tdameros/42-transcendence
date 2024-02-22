from PostSender._ABaseAPI import ABaseAPI


class DevAPI(ABaseAPI):
    @staticmethod
    async def post_start_match(_game_id: int, _player_1_id: int, _player_2_id: int):
        pass

    @staticmethod
    async def post_add_point(_game_id: int, _id_of_player_that_marked_a_point: int):
        pass

    @staticmethod
    async def post_end_match(_game_id: int,
                             _winner_id: int,
                             _winner_score: int,
                             _looser_id: int,
                             _looser_score: int):
        pass
