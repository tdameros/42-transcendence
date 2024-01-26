import json
import math
import random
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Match, Player, Tournament
from tournament import settings
from tournament.authenticate_request import authenticate_request
from api.views.match_utils import MatchUtils


@method_decorator(csrf_exempt, name='dispatch')
class MatchesView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            matches = list(tournament.matches.all())
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.matches_to_json(matches), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ManageMatchesView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int, match_id: int):
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            match = Match.objects.get(tournament_id=tournament_id, match_id=match_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'match with id `{match_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.match_to_json(match), status=200)

    @staticmethod
    def patch(request: HttpRequest, tournament_id: int, match_id: int):
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            body = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            match = Match.objects.get(tournament_id=tournament_id, match_id=match_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'match with id `{match_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            update_errors = ManageMatchesView.update_match(body, match)
            if update_errors:
                return JsonResponse(data={'errors': update_errors}, status=400)
            match.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.match_to_json(match), status=200)

    @staticmethod
    def update_match(body: dict, match: Match) -> list[str]:
        update_errors = []

        if match.status == Match.FINISHED:
            return [error.MATCH_FINISHED]

        new_match_status_error = ManageMatchesView.update_match_status(body, match)
        new_player_1_error = ManageMatchesView.update_player_1(body, match)
        new_player_1_score_error = ManageMatchesView.update_player_1_score(body, match)
        new_player_2_error = ManageMatchesView.update_player_2(body, match)
        new_player_2_score_error = ManageMatchesView.update_player_2_score(body, match)
        new_winner_error = ManageMatchesView.update_winner(body, match)

        if new_match_status_error is not None:
            update_errors.append(new_match_status_error)
        if new_player_1_error is not None:
            update_errors.append(new_player_1_error)
        if new_player_2_error is not None:
            update_errors.append(new_player_2_error)
        if new_player_1_score_error is not None:
            update_errors.append(new_player_1_score_error)
        if new_player_2_score_error is not None:
            update_errors.append(new_player_2_score_error)
        if new_winner_error is not None:
            update_errors.append(new_winner_error)

        return update_errors

    @staticmethod
    def update_match_status(body: dict, match: Match) -> Optional[str]:
        new_status = body.get('status')
        if new_status is not None:
            if not isinstance(new_status, int):
                return error.MATCH_STATUS_NOT_INT
            if new_status < Match.NOT_PLAYED or new_status > Match.FINISHED:
                return error.MATCH_STATUS_INVALID
            match.status = new_status
        return None

    @staticmethod
    def update_player_1(body: dict, match: Match) -> Optional[str]:
        new_player_1 = body.get('player_1')
        if new_player_1 is not None:
            if not isinstance(new_player_1, int):
                return error.MATCH_PLAYER_NOT_INT
            try:
                match.player_1 = Player.objects.get(id=new_player_1)
            except ObjectDoesNotExist:
                return error.MATCH_PLAYER_NOT_EXIST
        return None

    @staticmethod
    def update_player_1_score(body: dict, match: Match) -> Optional[str]:
        new_player_1_score = body.get('player_1_score')
        if new_player_1_score is not None:
            if not isinstance(new_player_1_score, int):
                return error.MATCH_PLAYER_SCORE_NOT_INT
            if new_player_1_score < 0 or new_player_1_score > settings.MATCH_POINT_TO_WIN:
                return error.MATCH_PLAYER_SCORE_INVALID
            match.player_1_score = new_player_1_score
        return None

    @staticmethod
    def update_player_2_score(body: dict, match: Match) -> Optional[str]:
        new_player_2_score = body.get('player_2_score')
        if new_player_2_score is not None:
            if not isinstance(new_player_2_score, int):
                return error.MATCH_PLAYER_SCORE_NOT_INT
            if new_player_2_score < 0 or new_player_2_score > settings.MATCH_POINT_TO_WIN:
                return error.MATCH_PLAYER_SCORE_INVALID
            match.player_2_score = new_player_2_score
        return None

    @staticmethod
    def update_player_2(body: dict, match: Match) -> Optional[str]:
        new_player_2 = body.get('player_2')
        if new_player_2 is not None:
            if not isinstance(new_player_2, int):
                return error.MATCH_PLAYER_NOT_INT
            try:
                match.player_2 = Player.objects.get(id=new_player_2)
            except ObjectDoesNotExist:
                return error.MATCH_PLAYER_NOT_EXIST
        return None

    @staticmethod
    def update_winner(body: dict, match: Match) -> Optional[str]:
        new_winner = body.get('winner')
        if new_winner is not None:
            if not isinstance(new_winner, int):
                return error.MATCH_WINNER_NOT_INT
            try:
                match.winner = Player.objects.get(id=new_winner)
            except ObjectDoesNotExist:
                return error.MATCH_WINNER_NOT_EXIST
            match.status = Match.FINISHED
        return None
