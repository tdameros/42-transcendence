from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Tournament
from api.views.match_utils import MatchUtils
from common.src.jwt_managers import user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class MatchesView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            matches = list(tournament.matches.all())
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse(MatchUtils.matches_to_json(matches), status=200)
