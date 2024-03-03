from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.PlayerManager import PlayerManager
from api.views.utils.get_user_id_from_jwt_in_request import \
    get_user_id_from_jwt_in_request
from common.src.jwt_managers import user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class GetMyGamePortView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        user_id = get_user_id_from_jwt_in_request(request)
        return JsonResponse({'port': PlayerManager.get_player_game_port(user_id)},
                            status=200)
