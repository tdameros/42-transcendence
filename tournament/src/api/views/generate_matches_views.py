import json
import math
import random
from typing import Optional

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Match, Player, Tournament
from api.views.match_utils import MatchUtils
from common.src.jwt_managers import user_authentication
from tournament import settings
from tournament.get_user import get_user_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class GenerateMatchesView(View):
    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user_id = get_user_id(request)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = list(tournament.players.all())
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        error_message, status_code = GenerateMatchesView.error_handler(user_id, tournament, players)
        if error_message is not None:
            return JsonResponse({'errors': [error_message]}, status=status_code)

        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            players = GenerateMatchesView.sort_players(request, players, body)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        matches = GenerateMatchesView.generate_matches(players, tournament)

        try:
            tournament.matches.all().delete()
            Match.objects.bulk_create(matches)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.matches_to_json(matches), status=200)

    @staticmethod
    def sort_players(request: HttpRequest, players: list[Player], body: dict) -> list[Player]:
        is_random = body.get('random')
        if isinstance(is_random, bool) and is_random:
            random.shuffle(players)
        else:
            GenerateMatchesView.set_players_elo(players, request.headers['Authorization'])
            players.sort(key=lambda x: x.elo, reverse=True)
        return players

    @staticmethod
    def generate_matches(players: list[Player], tournament: Tournament) -> list[Match]:
        nb_players = len(players)
        seed_order = GenerateMatchesView.get_seed_order(nb_players)
        matches = []

        for i, match in enumerate(seed_order):
            player_1 = players[match[0] - 1] if match[0] - 1 < nb_players else None
            player_2 = players[match[1] - 1] if match[1] - 1 < nb_players else None

            matches.append(
                Match(
                    player_1=player_1,
                    player_2=player_2,
                    tournament=tournament,
                    match_id=i
                )
            )
        nb_matches_first_round = len(matches)
        for i in range(0, nb_matches_first_round - 1):
            matches.append(
                Match(
                    player_1=None,
                    player_2=None,
                    tournament=tournament,
                    match_id=i + nb_matches_first_round
                )
            )
        GenerateMatchesView.manage_no_opponent(matches, nb_matches_first_round)
        return matches

    @staticmethod
    def get_seed_order(nb_players: int) -> list[list[int]]:
        nb_players = int(2 ** math.ceil(math.log2(nb_players)))
        rounds = int(math.log2(nb_players) - 1)
        players = [1, 2]

        for _ in range(rounds):
            players = GenerateMatchesView.next_seeding_layer(players)

        matches = []
        for i in range(0, len(players), 2):
            matches.append([players[i], players[i + 1]])

        return matches

    @staticmethod
    def next_seeding_layer(players):
        out = []
        length = len(players) * 2 + 1

        for player in players:
            out.append(player)
            out.append(length - player)

        return out

    @staticmethod
    def manage_no_opponent(matches: list[Match], nb_matches_first_round: int):
        for i in range(0, nb_matches_first_round):
            if matches[i].player_1 is None or matches[i].player_2 is None:
                matches[i].status = Match.FINISHED
                winner = matches[i].player_1 if matches[i].player_1 is not None else matches[i].player_2
                matches[i].winner = winner

                next_match_id = MatchUtils.get_next_match_id(i, len(matches))
                if i % 2 == 0:
                    matches[next_match_id].player_1 = winner
                else:
                    matches[next_match_id].player_2 = winner

    @staticmethod
    def set_players_elo(players: list[Player], jwt: str):
        for player in players:
            player.elo = GenerateMatchesView.get_elo(player, jwt)
            player.save()

    @staticmethod
    def get_elo(player: Player, jwt: str) -> int:
        headers = {'Authorization': jwt}
        response = requests.get(f'{settings.USER_STATS_USER_ENDPOINT}{player.user_id}', headers=headers)

        if response.status_code == 200:
            body = response.json()
            return body['elo']
        else:
            raise Exception(f'Error while getting elo for player {player.user_id}')

    @staticmethod
    def error_handler(user_id: int, tournament: Tournament, players: list[Player]) -> tuple[Optional[str], int]:
        if tournament.admin_id != user_id:
            return error.NOT_OWNER, 403

        if tournament.status != Tournament.CREATED:
            return error.ALREADY_STARTED, 400

        if len(players) < settings.MIN_PLAYERS:
            return error.NOT_ENOUGH_PLAYERS, 400

        return None, 200
