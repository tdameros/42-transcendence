from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        return JsonResponse({'status': 'ok'}, status=200)
