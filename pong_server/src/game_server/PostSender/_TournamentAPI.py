import logging

from common.src import settings
from PostSender._ABaseAPI import ABaseAPI


class TournamentAPI(ABaseAPI):
    @staticmethod
    async def post_start_match(game_id: int, player_1_id: int, player_2_id: int):
        uri: str = f'{settings.TOURNAMENT_URL}tournament/{game_id}/match/start/'
        body: dict = {
            "player1": player_1_id,
            "player2": player_2_id
        }

        logging.info(f'Posting to {uri} with body: {body}')
        await TournamentAPI._post(uri, body)

    @staticmethod
    async def post_add_point(game_id: int, id_of_player_that_marked_a_point: int):
        uri: str = f'{settings.TOURNAMENT_URL}tournament/{game_id}/match/add-point/'
        body: dict = {'player': id_of_player_that_marked_a_point}

        logging.info(f'Posting to {uri} with body: {body}')
        await TournamentAPI._post(uri, body)

    @staticmethod
    async def post_end_match(game_id: int,
                             winner_id: int,
                             _winner_score: int,
                             _looser_id: int,
                             _looser_score: int):
        uri: str = f'{settings.TOURNAMENT_URL}tournament/{game_id}/match/end/'
        body: dict = {'winner': winner_id}

        logging.info(f'Posting to {uri} with body: {body}')
        await TournamentAPI._post(uri, body)
