import datetime

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Tournament
from common.src.jwt_managers import service_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['DELETE']), name='dispatch')
class DeleteInactiveTournamentView(View):
    @staticmethod
    def delete(request: HttpRequest) -> JsonResponse:
        limit_datetime = datetime.datetime.now() - datetime.timedelta(hours=1)
        try:
            in_progress_tournaments = Tournament.objects.filter(
                status=Tournament.IN_PROGRESS,
                start_datetime__lt=limit_datetime
            )
            in_progress_tournaments.delete()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        return JsonResponse({'message': 'Tournament deleted'}, status=200)


