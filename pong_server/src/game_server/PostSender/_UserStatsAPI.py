from common.src import settings
from PostSender._ABaseAPI import ABaseAPI


class UserStatsAPI(ABaseAPI):
    @staticmethod
    async def post_start_match(_game_id: int, _player_1_id: int, _player_2_id: int):
        # Nothing to do for UserStatsAPI
        pass

    @staticmethod
    async def post_add_point(_game_id: int, _id_of_player_that_marked_a_point: int):
        # Nothing to do for UserStatsAPI
        pass

    @staticmethod
    async def post_end_match(_game_id: int,
                             winner_id: int,
                             winner_score: int,
                             looser_id: int,
                             looser_score: int):
        await UserStatsAPI._post(f'{settings.USER_STATS_URL}statistics/match/', {
            'winner_id': winner_id,
            'winner_score': winner_score,
            'loser_id': looser_id,
            'loser_score': looser_score
        })
