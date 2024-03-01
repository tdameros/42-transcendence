from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.JsonResponseException import JsonResponseException
from api.PlayerManager import PlayerManager
from api.views.utils.get_player_list import get_player_list
from common.src.jwt_managers import service_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['POST']), name='dispatch')
class GetPlayersGamePortView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            players: list[int] = get_player_list(request)

            data = {}
            for player in players:
                data[player] = PlayerManager.get_player_game_port(player)

            return JsonResponse(data, status=200)

        except JsonResponseException as json_response_exception:
            return json_response_exception.to_json_response()
