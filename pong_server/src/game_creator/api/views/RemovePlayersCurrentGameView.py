import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_messages
from api.JsonResponseException import JsonResponseException
from api.PlayerManager import PlayerManager
from common.src.jwt_managers import service_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['DELETE']), name='dispatch')
class RemovePlayersCurrentGameView(View):
    def delete(self, request):
        try:
            players: list[int] = RemovePlayersCurrentGameView._get_players(request)

            PlayerManager.remove_players(players)

            return JsonResponse({}, status=204)

        except JsonResponseException as json_response_exception:
            return json_response_exception.to_json_response()

    @staticmethod
    def _get_players(request) -> list[int]:
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            if not isinstance(json_body, dict):
                raise Exception()
        except Exception:
            raise JsonResponseException({'errors': [error_messages.BAD_JSON_FORMAT]},
                                        status=400)

        players: any = json_body.get('players')
        if players is None:
            raise JsonResponseException(
                {'errors': [error_messages.PLAYERS_FIELD_MISSING]},
                status=400
            )
        if not isinstance(players, list):
            raise JsonResponseException(
                {'errors': [error_messages.PLAYERS_FIELD_IS_NOT_A_LIST]},
                status=400
            )

        errors: list[str] = []
        for index, player in enumerate(players):
            if not isinstance(player, int):
                try:
                    players[index] = int(player)
                except (ValueError, TypeError):
                    errors.append(error_messages.player_is_not_an_int(index))
        if len(errors) != 0:
            raise JsonResponseException(
                {'errors': errors},
                status=400
            )

        return players
