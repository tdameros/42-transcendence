import datetime
from typing import Any, Optional

from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import Match, User
from common.src.jwt_managers import user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserProgressView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        valid, errors = UserProgressView.validate_get_request(request, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)
        days = request.GET.get('days', '7')

        return UserProgressView.get_progress_data(user_id, days)

    @staticmethod
    def get_progress_data(user_id: int, days):
        progress = {
            'elo': 0,
            'win_rate': 0,
            'matches_played': 0
        }
        date = timezone.now() - datetime.timedelta(days=int(days))
        try:
            match = Match.objects.filter(user_id=user_id, date__gte=date).order_by('date').first()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        if match is None:
            return JsonResponse({'progress': progress}, status=200)
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        progress['elo'] = user.elo - match.user_elo
        progress['win_rate'] = float(user.win_rate) - float(match.user_win_rate)
        progress['matches_played'] = user.matches_played - match.user_matches_played
        return JsonResponse({'progress': progress}, status=200)

    @staticmethod
    def validate_get_request(request: HttpRequest, user_id: int) -> (bool, Optional[list[str]]):
        errors = []
        days = request.GET.get('days', '7')

        valid, error = UserProgressView.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        valid, error = UserProgressView.validate_days(days)
        if not valid:
            errors.append(error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def validate_user_id(user_id: Any) -> (bool, Optional[str]):
        if user_id is None:
            return False, error.USER_ID_REQUIRED
        if not isinstance(user_id, int):
            return False, error.USER_ID_INVALID
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False, error.USER_NOT_FOUND
        return True, None

    @staticmethod
    def validate_days(days: Any) -> (bool, Optional[str]):
        if not days.isdigit():
            return False, error.DAYS_INVALID
        if int(days) < 0:
            return False, error.DAYS_INVALID
        return True, None
