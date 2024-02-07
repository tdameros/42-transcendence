import json
from typing import Optional

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_messages
from api.GameCreator import GameCreator
from api.JsonResponseException import JsonResponseException


@method_decorator(csrf_exempt, name='dispatch')
class CreateGameView(View):
    def post(self, request):
        try:
            game_id, players, request_issuer = CreateGameView._get_args(request)

            game_server_uri = GameCreator.create_game_server(game_id, players)

            return JsonResponse({'game_server_uri': game_server_uri},
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

        game_id = CreateGameView._get_game_id(json_body, errors)
        players = CreateGameView._get_players(json_body, errors)
        request_issuer = CreateGameView._get_request_issuer(json_body, errors)

        if len(errors) > 0:
            raise JsonResponseException({'errors': errors}, status=400)

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
        except ValueError:
            errors.append(error_messages.GAME_ID_FIELD_IS_NOT_AN_INTEGER)
            return -1

    @staticmethod
    def _get_players(json_body, errors) -> list[Optional[int]]:

        players = json_body.get('players')
        if players is None:
            errors.append(error_messages.PLAYERS_FIELD_MISSING)
            return []

        if not isinstance(players, list):
            errors.append(error_messages.PLAYERS_FIELD_IS_NOT_A_LIST)
            return []

        correct_players: set[int] = set()
        for index, player in enumerate(players):
            if player is None:
                continue
            try:
                if not isinstance(player, int):
                    player = int(player)
                if player in correct_players:
                    errors.append(error_messages.player_is_found_multiple_times(player))
                else:
                    correct_players.add(player)
            except ValueError:
                errors.append(error_messages.player_is_not_an_optional_int(index))

        return players

    @staticmethod
    def _get_request_issuer(json_body, errors) -> str:
        request_issuer = json_body.get('request_issuer')
        if request_issuer is None:
            errors.append(error_messages.REQUEST_ISSUER_FIELD_MISSING)
            return ''

        if not isinstance(request_issuer, str):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_A_STRING)
            return ''

        if (not request_issuer == 'tournament'
                and not request_issuer == 'matchmaking'):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_VALID)
            return ''

        return request_issuer
