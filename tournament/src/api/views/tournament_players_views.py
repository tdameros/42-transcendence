from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.views import View

from api.models import Tournament


class TournamentPlayersView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO uncomment this line when jwt will be implemented
        # user, authenticate_errors = authenticate_request(request)
        # if user is None:
        #     return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)

        players = tournament.players.all()

        players_data = [{
            'nickname': player.nickname,
            'user_id': player.user_id
        } for player in players]

        response_data = {
            'max-players': tournament.max_players,
            'players': players_data
        }

        return JsonResponse(response_data, status=200)
