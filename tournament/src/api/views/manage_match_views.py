import json
import math
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Match, Player, Tournament
from api.views.match_utils import MatchUtils


@method_decorator(csrf_exempt, name='dispatch')
class StartMatchView(View):
    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO: add service authentication when implemented

        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'Tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        player1 = body.get('player1')
        player2 = body.get('player2')
        is_valid, error_message = StartMatchView.is_valid_players(player1, player2)
        if not is_valid:
            return JsonResponse(data={'errors': [error_message]}, status=400)

        try:
            player1 = Player.objects.get(tournament_id=tournament_id, user_id=player1)
            player2 = Player.objects.get(tournament_id=tournament_id, user_id=player2)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_PLAYER_NOT_EXIST]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            match = StartMatchView.get_match(tournament_id, player1, player2)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_NOT_FOUND]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if match.tournament.status != Tournament.IN_PROGRESS:
            return JsonResponse({'errors': [error.TOURNAMENT_NOT_STARTED]}, status=400)

        match.status = Match.IN_PROGRESS
        match.player_1_score = 0
        match.player_2_score = 0

        try:
            match.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.match_to_json(match), status=200)

    @staticmethod
    def is_valid_players(player1: any, player2: any) -> tuple[bool, Optional[str]]:
        if player1 is not None and not isinstance(player1, int):
            return False, error.MATCH_PLAYER_NOT_INT
        if player2 is not None and not isinstance(player2, int):
            return False, error.MATCH_PLAYER_NOT_INT

        if player1 == player2:
            return False, error.MATCH_PLAYER_NOT_EXIST

        return True, None

    @staticmethod
    def get_match(tournament_id: int, player1: Player, player2: Player):
        return Match.objects.get(
            tournament_id=tournament_id,
            player_1=player1,
            player_2=player2,
            status=Match.NOT_PLAYED
        )


@method_decorator(csrf_exempt, name='dispatch')
class EndMatchView(View):
    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO: add service authentication when implemented

        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'Tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        winner = body.get('winner')
        if not isinstance(winner, int):
            return JsonResponse(data={'errors': [error.MATCH_WINNER_NOT_INT]}, status=400)
        try:
            winner = Player.objects.get(tournament_id=tournament_id, user_id=winner)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_PLAYER_NOT_EXIST]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            match = EndMatchView.get_match(tournament_id, winner)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_NOT_FOUND]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        nb_matches = match.tournament.matches.count()
        try:
            EndMatchView.set_winner(match, winner)
            EndMatchView.set_loser_ranking(match, nb_matches)
            EndMatchView.update_tournament(match, nb_matches)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.match_to_json(match), status=200)

    @staticmethod
    def get_match(tournament_id: int, winner: int):
        return Match.objects.get(
            Q(
                tournament_id=tournament_id,
                player_1=winner,
                status=Match.IN_PROGRESS
            ) | Q(
                tournament_id=tournament_id,
                player_2=winner,
                status=Match.IN_PROGRESS
            )
        )

    @staticmethod
    def set_winner(match: Match, winner: int):
        if match.player_1.user_id == winner.user_id:
            match.winner = match.player_1
        else:
            match.winner = match.player_2
        match.status = Match.FINISHED
        match.save()

    @staticmethod
    def update_tournament(match: Match, nb_matches: int):
        tournament = match.tournament
        nb_round = int(math.log2(nb_matches + 1))
        round_id = nb_round - int(math.log2(nb_matches - match.match_id))
        is_final = round_id == nb_round

        if is_final:
            EndMatchView.set_winner_ranking(match.winner)
            tournament.status = Tournament.FINISHED
            tournament.save()
            return
        else:
            next_match_id = MatchUtils.get_next_match_id(match.match_id, nb_matches)
            next_match = Match.objects.get(tournament_id=tournament.pk, match_id=next_match_id)
            if match.match_id % 2 == 0:
                next_match.player_1 = match.winner
            else:
                next_match.player_2 = match.winner
            next_match.save()

    @staticmethod
    def set_winner_ranking(winner: Player):
        winner.rank = 1
        winner.save()

    @staticmethod
    def set_loser_ranking(match: Match, nb_matches: int):
        if match.winner == match.player_1:
            loser = match.player_2
        else:
            loser = match.player_1
        if loser is None:
            return

        nb_round = int(math.log2(nb_matches + 1))
        round_id = nb_round - int(math.log2(nb_matches - match.match_id))
        if round_id == 1:
            loser.rank = match.tournament.players.count()
        else:
            loser.rank = int(2 ** math.ceil(math.log2(nb_matches + 1 - match.match_id)))
        loser.save()


@method_decorator(csrf_exempt, name='dispatch')
class AddPointView(View):
    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO: add service authentication when implemented
        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'Tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        player = body.get('player')
        if not isinstance(player, int):
            return JsonResponse(data={'errors': [error.MATCH_PLAYER_NOT_INT]}, status=400)
        try:
            player = Player.objects.get(tournament_id=tournament_id, user_id=player)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_PLAYER_NOT_EXIST]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            match = AddPointView.get_match(tournament_id, player)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.MATCH_NOT_FOUND]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            AddPointView.update_score(match, player)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.match_to_json(match), status=200)

    @staticmethod
    def get_match(tournament_id: int, player: int):
        return Match.objects.get(
            Q(
                tournament_id=tournament_id,
                player_1=player,
                status=Match.IN_PROGRESS
            ) | Q(
                tournament_id=tournament_id,
                player_2=player,
                status=Match.IN_PROGRESS
            )
        )

    @staticmethod
    def update_score(match: Match, player: Player):
        if match.player_1.user_id == player.user_id:
            match.player_1_score += 1
        else:
            match.player_2_score += 1

        match.save()
