import shared_code.settings as settings
from PostSender._ABaseAPI import ABaseAPI
from PostSender._DevAPI import DevAPI
from PostSender._TournamentAPI import TournamentAPI
from PostSender._UserStatsAPI import UserStatsAPI


class PostSender(ABaseAPI):
    _api: ABaseAPI

    @staticmethod
    def init(api_name: str):
        if api_name == settings.TOURNAMENT:
            PostSender._api = TournamentAPI
        elif api_name == settings.USER_STATS:
            PostSender._api = UserStatsAPI
        else:
            PostSender._api = DevAPI

    @staticmethod
    async def post_start_match(game_id: int, player_1_id: int, player_2_id: int):
        await PostSender._api.post_start_match(game_id, player_1_id, player_2_id)

    @staticmethod
    async def post_add_point(game_id: int, id_of_player_that_marked_a_point: int):
        await PostSender._api.post_add_point(game_id, id_of_player_that_marked_a_point)

    @staticmethod
    async def post_end_match(game_id: int,
                             winner_id: int,
                             winner_score: int,
                             looser_id: int,
                             looser_score: int):
        await PostSender._api.post_end_match(
            game_id, winner_id, winner_score, looser_id, looser_score
        )
