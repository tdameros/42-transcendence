import json
from typing import Optional

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_messages, settings
from api.GameCreator import GameCreator
from api.JsonResponseException import JsonResponseException
from api.PlayerManager import PlayerManager
from common.src.jwt_managers import service_authentication
from shared_code import settings as shared_settings


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['POST']), name='dispatch')
class CreateGameView(View):
    def post(self, request):
        try:
            game_id, players, request_issuer = CreateGameView._get_args(request)

            if request_issuer == settings.TOURNAMENT:
                api_name = shared_settings.TOURNAMENT
            else:
                api_name = shared_settings.USER_STATS
            port: int = GameCreator.create_game_server(game_id, players, api_name)

            PlayerManager.add_players(players, port)

            return JsonResponse({'port': port},
                                status=201)

        except JsonResponseException as json_response_exception:
            return json_response_exception.to_json_response()

    @staticmethod
    def _get_args(request) -> (int, list[Optional[int]], str):
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            if not isinstance(json_body, dict):
                raise Exception()
        except Exception:
            raise JsonResponseException({'errors': [error_messages.BAD_JSON_FORMAT]},
                                        status=400)

        errors = []

        request_issuer: str = CreateGameView._get_request_issuer(json_body, errors)
        game_id: int = CreateGameView._get_game_id(json_body, errors)
        players: list[Optional[int]] = CreateGameView._get_players(
            json_body, errors, request_issuer
        )

        if len(errors) > 0:
            raise JsonResponseException({'errors': errors}, status=400)

        conflicts: list[str] = []
        for player in players:
            if player is not None:
                if PlayerManager.get_player_game_port(player) is not None:
                    conflicts.append(error_messages.player_is_already_in_a_game(player))
        if len(conflicts) > 0:
            raise JsonResponseException({'errors': conflicts}, status=409)

        return game_id, players, request_issuer

    @staticmethod
    def _get_game_id(json_body, errors) -> int:
        game_id = json_body.get('game_id')
        if game_id is None:
            errors.append(error_messages.GAME_ID_FIELD_MISSING)
            return -1

        if isinstance(game_id, int):
            return game_id

        try:
            return int(game_id)
        except (ValueError, TypeError):
            errors.append(error_messages.GAME_ID_FIELD_IS_NOT_AN_INTEGER)
            return -1

    @staticmethod
    def _get_players(json_body, errors, request_issuer: str) -> list[Optional[int]]:
        players: any = json_body.get('players')
        if players is None:
            errors.append(error_messages.PLAYERS_FIELD_MISSING)
            return []

        if not isinstance(players, list):
            errors.append(error_messages.PLAYERS_FIELD_IS_NOT_A_LIST)
            return []

        if len(players) != 2 and request_issuer == settings.MATCHMAKING:
            errors.append(error_messages.NEED_2_PLAYERS_FOR_MATCHMAKING)

        if (len(players) & (len(players) - 1) != 0) and len(players) != 0:
            errors.append(error_messages.LEN_PLAYERS_IS_NOT_A_POWER_OF_2)

        validated_players: set[int] = set()
        for i in range(0, len(players) - 1, 2):
            CreateGameView._check_player(players, i, errors, validated_players)
            CreateGameView._check_player(players, i + 1, errors, validated_players)
            if players[i] is None and players[i + 1] is None:
                errors.append(error_messages.BOTH_PLAYERS_ARE_NONE)
        if len(players) % 2 == 1:
            CreateGameView._check_player(players, len(players) - 1, errors, validated_players)
        if len(validated_players) <= 1:
            errors.append(error_messages.NEED_AT_LEAST_2_PLAYERS_THAT_ARENT_NONE)

        return players

    @staticmethod
    def _check_player(players: list[any],
                      index: int,
                      errors: list[str],
                      validated_players: set[int]):
        if players[index] is None:
            return

        try:
            if not isinstance(players[index], int):
                players[index] = int(players[index])
        except (ValueError, TypeError):
            errors.append(error_messages.player_is_not_an_optional_int(index))
            return

        if players[index] in validated_players:
            errors.append(error_messages.player_is_found_multiple_times(players[index]))
        else:
            validated_players.add(players[index])

    @staticmethod
    def _get_request_issuer(json_body, errors) -> str:
        request_issuer = json_body.get('request_issuer')
        if request_issuer is None:
            errors.append(error_messages.REQUEST_ISSUER_FIELD_MISSING)
            return ''

        if not isinstance(request_issuer, str):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_A_STRING)
            return ''

        if request_issuer not in (settings.TOURNAMENT, settings.MATCHMAKING):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_VALID)
            return ''

        return request_issuer
