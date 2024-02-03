from typing import Any, Optional
from dateutil import parser

from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import Match, User
from common.src.jwt_managers import user_authentication


class UserGraph:

    @staticmethod
    def get_graph_data(request: HttpRequest, user_id: int, field: str):
        start = parser.isoparse(request.GET.get('start'))
        end = parser.isoparse(request.GET.get('end'))
        num_points = int(request.GET.get('num_points'))

        date_intervals = UserGraph.get_date_intervals(start, end, num_points)
        try:
            data = UserGraph.get_data_from_interval(user_id, date_intervals, field)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        return JsonResponse({'graph': data}, status=200)


    @staticmethod
    def get_date_intervals(start, end, num_points):
        date_intervals = []

        if timezone.is_naive(start):
            start = timezone.make_aware(start)
        if timezone.is_naive(end):
            end = timezone.make_aware(end)
        interval = timezone.timedelta(seconds=(end - start).total_seconds() / (num_points - 1))
        for i in range(num_points):
            date_intervals.append(start + interval * i)
        return date_intervals

    @staticmethod
    def get_data_from_interval(user_id, date_intervals, field):
        data = []
        user = User.objects.get(pk=user_id)
        for date in date_intervals:
            match = Match.objects.filter(user_id=user_id, date__gte=date).order_by('date').first()
            if field == 'elo':
                if match is None:
                    data.append({'date': date.isoformat(), 'value': user.elo})
                else:
                    data.append({'date': date.isoformat(), 'value': match.user_elo})
            elif field == 'win_rate':
                if match is None:
                    data.append({'date': date.isoformat(), 'value': user.win_rate})
                else:
                    data.append({'date': date.isoformat(), 'value': match.user_win_rate})
            elif field == 'matches_played':
                if match is None:
                    data.append({'date': date.isoformat(), 'value': user.matches_played})
                else:
                    data.append({'date': date.isoformat(), 'value': match.user_matches_played})
        return data

    @staticmethod
    def validate_get_request(request: HttpRequest, user_id: int) -> (bool, Optional[list[str]]):
        errors = []
        start = request.GET.get('start')
        end = request.GET.get('end')
        num_points = request.GET.get('num_points')

        valid, error = UserGraph.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        valid, error = UserGraph.validate_date(start)
        if not valid:
            errors.append(error)
        valid, error = UserGraph.validate_date(end)
        if not valid:
            errors.append(error)
        valid, error = UserGraph.validate_num_points(num_points)
        if not valid:
            errors.append(error)
        valid, error = UserGraph.validate_date_order(start, end)
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
    def validate_date(date: Any) -> (bool, Optional[str]):
        if date is None:
            return False, error.DATE_QUERY_REQUIRED
        try:
            if parser.isoparse(date) is None:
                return False, error.DATE_QUERY_INVALID
        except ValueError:
            return False, error.DATE_QUERY_INVALID
        return True, None

    @staticmethod
    def validate_num_points(num_points: Any) -> (bool, Optional[str]):
        if num_points is None:
            return False, error.NUM_POINTS_REQUIRED
        if not num_points.isdigit():
            return False, error.NUM_POINTS_INVALID
        if int(num_points) < 2:
            return False, error.NUM_POINTS_INVALID
        return True, None

    @staticmethod
    def validate_date_order(start: Any, end: Any) -> (bool, Optional[str]):
        valid, _ = UserGraph.validate_date(start)
        if not valid:
            return True, None
        valid, _ = UserGraph.validate_date(end)
        if not valid:
            return True, None
        start = parser.isoparse(start)
        end = parser.isoparse(end)
        if start > end:
            return False, error.DATE_ORDER_INVALID
        return True, None

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserGraphEloView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        valid, errors = UserGraph.validate_get_request(request, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        return UserGraph.get_graph_data(request, user_id, 'elo')

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserGraphWinRateView(View):

        @staticmethod
        def get(request: HttpRequest, user_id: int):
            valid, errors = UserGraph.validate_get_request(request, user_id)
            if not valid:
                return JsonResponse({'errors': errors}, status=400)

            return UserGraph.get_graph_data(request, user_id, 'win_rate')

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserGraphMatchesPlayedView(View):

        @staticmethod
        def get(request: HttpRequest, user_id: int):
            valid, errors = UserGraph.validate_get_request(request, user_id)
            if not valid:
                return JsonResponse({'errors': errors}, status=400)

            return UserGraph.get_graph_data(request, user_id, 'matches_played')

