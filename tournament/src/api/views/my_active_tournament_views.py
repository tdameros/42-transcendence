from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from api.models import Tournament
from api.views.tournament_utils import TournamentUtils
from common.src.jwt_managers import user_authentication
from tournament.get_user import get_user_id


@method_decorator(user_authentication(['GET']), name='dispatch')
class MyActiveTournamentView(View):
    @staticmethod
    def get(request: HttpRequest):
        user_id = get_user_id(request)
        active_tournaments = []

        try:
            registered_tournament = Tournament.objects.get(
                status__in=[Tournament.CREATED, Tournament.IN_PROGRESS],
                players__user_id=user_id
            )
            my_tournaments = Tournament.objects.filter(
                status__in=[Tournament.CREATED, Tournament.IN_PROGRESS],
                admin_id=user_id
            )
        except ObjectDoesNotExist:
            registered_tournament = None
            my_tournaments = []
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        my_tournaments = my_tournaments.exclude(
            id=registered_tournament.id) if registered_tournament else my_tournaments
        if registered_tournament:
            active_tournaments.append(registered_tournament)
        if len(my_tournaments) > 0:
            active_tournaments.extend(my_tournaments)

        jwt = request.headers.get('Authorization')
        try:
            tournaments_data = TournamentUtils.tournament_to_json(active_tournaments, jwt)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(
            {
                'nb-active-tournaments': len(tournaments_data),
                'active-tournaments': tournaments_data
            },
            status=200
        )
