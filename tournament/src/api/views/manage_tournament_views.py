from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Tournament
from api.views.tournament_views import TournamentView
from tournament.authenticate_request import authenticate_request


@method_decorator(csrf_exempt, name='dispatch')
class ManageTournamentView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        try:
            tournament_players = tournament.players.all()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'nb-players': len(tournament_players),
            'players': [{
                'nickname': player.nickname,
                'user-id': player.user_id
            } for player in tournament_players],
            'is-private': tournament.is_private,
            'status': TournamentView.status_to_string(tournament.status),
            'admin': user['username']
        }

        if tournament.registration_deadline is not None:
            tournament_data['registration-deadline'] = tournament.registration_deadline

        return JsonResponse(tournament_data, status=200)

    @staticmethod
    def delete(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        tournament_name = tournament.name
        tournament_admin = tournament.admin_id

        if tournament_admin != user['id']:
            return JsonResponse({
                'error': f'you cannot delete `{tournament_name}` because you are not the owner of the tournament'
            }, status=403)

        try:
            tournament.delete()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': f'tournament `{tournament_name}` successfully deleted'}, status=200)
