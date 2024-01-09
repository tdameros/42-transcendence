from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from api.models import Tournament


@method_decorator(csrf_exempt, name='dispatch')
class ManageTournamentView(View):
    @staticmethod
    def delete(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO replace this line by `user-management` request when jwt will be implemented
        user = {'id': 1}

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)

        tournament_name = tournament.name
        tournament_admin = tournament.admin_id

        if tournament_admin != user['id']:
            return JsonResponse({
                'error': f'you cannot delete `{tournament_name}` because you are not the owner of the tournament'
            }, status=403)

        try:
            tournament.delete()
        except:
            return JsonResponse({'error': f'cannot delete `{tournament_name}`'}, status=500)

        return JsonResponse({'message': f'tournament `{tournament_name}` successfully deleted'}, status=200)
