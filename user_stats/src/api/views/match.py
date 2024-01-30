import json
from typing import Any, Optional
from dateutil import parser

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user_stats import settings
import api.error_message as error
from api.models import User
from api.models import Match


@method_decorator(csrf_exempt, name='dispatch')
class MatchView(View):

    @staticmethod
    def post(request: HttpRequest):
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        valid, errors = MatchView.validate_post_request(json_body)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        winner_match_id, loser_match_id = MatchView.post_match_data(json_body)
        return JsonResponse({
            'winner_match_id': winner_match_id,
            'loser_match_id': loser_match_id
        }, status=201)

    @staticmethod
    def validate_post_request(json_body: dict) -> (bool, list[str]):
        errors = []
        winner_id = json_body.get('winner_id')
        loser_id = json_body.get('loser_id')
        winner_score = json_body.get('winner_score')
        loser_score = json_body.get('loser_score')
        date = json_body.get('date')

        valid, error = MatchView.validate_player_id(winner_id)
        if not valid:
            errors.append(error)
        valid, error = MatchView.validate_player_id(loser_id)
        if not valid:
            errors.append(error)
        valid, error = MatchView.validate_score(winner_score)
        if not valid:
            errors.append(error)
        valid, error = MatchView.validate_score(loser_score)
        if not valid:
            errors.append(error)
        valid, error = MatchView.validate_date(date)
        if not valid:
            errors.append(error)
        if errors:
            return False, errors
        return True, errors

    @staticmethod
    def post_match_data(json_body: Any):
        winner = User.objects.get(pk=json_body['winner_id'])
        loser = User.objects.get(pk=json_body['loser_id'])
        previous_winner_elo = winner.elo
        previous_loser_elo = loser.elo

        MatchView.update_player_stats(winner, loser)
        winner_match = MatchView.init_match(winner, True, json_body)
        loser_match = MatchView.init_match(loser, False, json_body)
        winner_match.user_elo_delta = winner.elo - previous_winner_elo
        loser_match.user_elo_delta = loser.elo - previous_loser_elo
        winner_match.save()
        loser_match.save()
        return winner_match.id, loser_match.id

    @staticmethod
    def init_match(user: User, result: bool, json_body: Any) -> Match:
        match = Match()
        user_score = json_body['winner_score'] if result else json_body['loser_score']
        opponent_score = json_body['loser_score'] if result else json_body['winner_score']
        opponent_id = json_body['loser_id'] if result else json_body['winner_id']

        match.user = user
        match.opponent = User.objects.get(pk=opponent_id)
        match.user_score = user_score
        match.opponent_score = opponent_score
        match.result = result
        match.user_elo = user.elo
        match.user_win_rate = user.win_rate
        match.user_expected_result = MatchView.calculate_expected_result(user.elo, match.opponent.elo)
        match.date = parser.isoparse(json_body['date'])
        return match

    @staticmethod
    def update_player_stats(winner: User, loser: User):
        winner_elo, loser_elo = MatchView.calculate_elo(winner, loser)

        winner.elo = winner_elo
        loser.elo = loser_elo
        winner.games_played += 1
        winner.games_won += 1
        winner.win_rate = winner.games_won / winner.games_played
        loser.games_played += 1
        loser.games_lost += 1
        loser.win_rate = loser.games_won / loser.games_played
        winner.save()
        loser.save()

    @staticmethod
    def calculate_elo(winner: User, loser: User) -> (int, int):
        winner_expected = MatchView.calculate_expected_result(winner.elo, loser.elo)
        loser_expected = MatchView.calculate_expected_result(loser.elo, winner.elo)
        winner_elo = winner.elo + settings.K_FACTOR * (1 - winner_expected)
        loser_elo = loser.elo + settings.K_FACTOR * (0 - loser_expected)
        return int(winner_elo), int(loser_elo)

    @staticmethod
    def calculate_expected_result(user_elo: int, loser_elo: int) -> float:
        return 1 / (1 + 10 ** ((loser_elo - user_elo) / 400))

    @staticmethod
    def validate_player_id(player_id: Any) -> (bool, Optional[str]):
        if player_id is None:
            return False, error.USER_ID_REQUIRED
        if not isinstance(player_id, int):
            return False, error.USER_ID_INVALID
        if player_id < 0:
            return False, error.USER_ID_INVALID
        try:
            User.objects.get(pk=player_id)
        except User.DoesNotExist:
            return False, error.USER_NOT_FOUND
        return True, None

    @staticmethod
    def validate_score(score: Any) -> (bool, Optional[str]):
        if score is None:
            return False, error.SCORE_REQUIRED
        if not isinstance(score, int):
            return False, error.SCORE_INVALID
        if score < 0:
            return False, error.SCORE_INVALID
        return True, None

    @staticmethod
    def validate_date(date: Any) -> (bool, Optional[str]):
        if date is None:
            return False, error.DATE_REQUIRED
        try:
            if parser.isoparse(date) is None:
                return False, error.DATE_INVALID
        except ValueError:
            return False, error.DATE_INVALID
        return True, None
