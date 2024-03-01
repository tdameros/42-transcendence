from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.JsonResponseException import JsonResponseException
from api.PlayerManager import PlayerManager
from api.views.utils.get_player_list import get_player_list
from common.src.jwt_managers import service_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['DELETE']), name='dispatch')
class RemovePlayersCurrentGameView(View):
    def delete(self, request):
        try:
            players: list[int] = get_player_list(request)

            PlayerManager.remove_players(players)

            return JsonResponse({}, status=204)

        except JsonResponseException as json_response_exception:
            return json_response_exception.to_json_response()
