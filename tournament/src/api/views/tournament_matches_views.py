import json
import math
import random
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.models import Tournament, Player, Match
from tournament.authenticate_request import authenticate_request
from tournament import settings
from api import error_message as error


@method_decorator(csrf_exempt, name='dispatch')
class GenerateMatchesView(View):
    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            body = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = list(tournament.players.all())
            GenerateMatchesView.set_players_elo(players)
            tournament.matches.all().delete()
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        error_message, status_code = GenerateMatchesView.error_handler(user['id'], tournament, players)
        if error_message is not None:
            return JsonResponse({'errors': [error_message]}, status=status_code)

        players = GenerateMatchesView.sort_players(players, body.get('is_random', False))
        matches = GenerateMatchesView.generate_matches(players, tournament)

        try:
            Match.objects.bulk_create(matches)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(GenerateMatchesView.matches_to_json(matches), status=200)

    @staticmethod
    def sort_players(players: list[Player], is_random: any) -> list[Player]:
        if isinstance(is_random, bool) and is_random:
            random.shuffle(players)
        else:
            players.sort(key=lambda x: x.elo, reverse=True)
        return players

    @staticmethod
    def generate_matches(players: list[Player], tournament: Tournament) -> list[Match]:
        nb_players = len(players)
        seed_order = GenerateMatchesView.get_seed_order(nb_players)
        matches = []
        i = 0

        for match in seed_order:
            if match[0] - 1 < nb_players:
                player_1 = players[match[0] - 1]
            else:
                player_1 = None
            if match[1] - 1 < nb_players:
                player_2 = players[match[1] - 1]
            else:
                player_2 = None
            matches.append(
                Match(
                    player_1=player_1,
                    player_2=player_2,
                    tournament=tournament,
                    match_id=i
                )
            )
            i += 1

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
    def set_players_elo(players: list[Player]):
        for player in players:
            player.elo = GenerateMatchesView.get_elo(player)
            player.save()


    @staticmethod
    def get_elo(player: Player) -> int:
        # TODO: Get elo from user stats microservice
        return random.randint(1, 1000)

    @staticmethod
    def error_handler(user_id: int, tournament: Tournament, players: list[Player]) -> tuple[Optional[str], int]:
        if tournament.admin_id != user_id:
            return error.NOT_OWNER, 403

        if tournament.status != Tournament.CREATED:
            return error.ALREADY_STARTED, 400

        if len(players) < settings.MIN_PLAYERS:
            return error.NOT_ENOUGH_PLAYERS, 400

        return None, 200

    @staticmethod
    def matches_to_json(matches: list[Match]) -> dict[str, list[any]]:
        matches_data = [
            {
                'id': match.match_id,
                'player_1': match.player_1.nickname if match.player_1 is not None else None,
                'player_2': match.player_2.nickname if match.player_2 is not None else None
            } for match in matches
        ]
        data = {'matches': matches_data}

        return data
