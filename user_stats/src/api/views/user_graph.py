from typing import Any, Optional

import numpy as np
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
    def get_graph_data_by_value(request: HttpRequest, user_id: int, field: str):
        start = parser.isoparse(request.GET.get('start'))
        end = parser.isoparse(request.GET.get('end'))
        num_points = int(request.GET.get('num_points'))

        if timezone.is_naive(start):
            start = timezone.make_aware(start)
        if timezone.is_naive(end):
            end = timezone.make_aware(end)
        try:
            matches = Match.objects.filter(user_id=user_id, date__gte=start, date__lte=end).order_by('date')
            last_match = Match.objects.filter(user_id=user_id, date__gte=end).order_by('date').first()
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        values = UserGraph.get_database_values(user, matches, last_match, end, field)
        data = UserGraph.downsample_data(values, num_points)
        body = {
            'graph': data,
            'num_points': len(data)
        }
        return JsonResponse(body, status=200)

    @staticmethod
    def get_graph_data_by_date(request: HttpRequest, user_id: int, field: str):
        start = parser.isoparse(request.GET.get('start'))
        end = parser.isoparse(request.GET.get('end'))
        num_points = int(request.GET.get('num_points'))

        if timezone.is_naive(start):
            start = timezone.make_aware(start)
        if timezone.is_naive(end):
            end = timezone.make_aware(end)
        intervals = UserGraph.get_database_intervals(start, end, num_points)
        try:
            data = UserGraph.deltasample_data(user_id, intervals, field)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        body = {
            'graph': data,
            'num_points': len(data)
        }
        return JsonResponse(body, status=200)

    @staticmethod
    def downsample_data(values: Any, num_points: int) -> list:
        data = []
        num_points = min(num_points, len(values))
        segment_length = len(values) // num_points

        for i in range(num_points):
            segment = values[i * segment_length: (i + 1) * segment_length]
            value = np.mean([item['value'] for item in segment])
            date = segment[0]['date'] + (segment[-1]['date'] - segment[0]['date']) / 2
            data.append({
                'value': value,
                'date': date,
            })
        return data

    @staticmethod
    def deltasample_data(user_id: int, intervals: list, field: str) -> list:
        data = []
        user = User.objects.get(pk=user_id)
        max_val = 0
        for date in intervals:
            match = Match.objects.filter(user_id=user_id, date__gte=date).order_by('date').first()
            match_value = getattr(match, f'user_{field}') if match else getattr(user, field)
            value = match_value - max_val
            max_val = max(max_val, match_value)
            data.append({
                'value': value,
                'date': date,
            })
        return data

    @staticmethod
    def get_database_values(user: Any, matches: Any, last_match: Any, end: Any, field: str) -> list:
        match_field = f'user_{field}'
        values = [{
            'value': getattr(match, match_field),
            'date': match.date,
        } for match in matches]
        if last_match:
            values.append({
                'value': getattr(last_match, match_field),
                'date': end,
            })
        else:
            values.append({
                'value': getattr(user, field),
                'date': end,
            })
        return values

    @staticmethod
    def get_database_intervals(start: Any, end: Any, num_points: int) -> list:
        intervals = []

        interval = timezone.timedelta(seconds=(end - start).total_seconds() / (num_points - 1))
        for i in range(num_points):
            intervals.append(start + interval * i)
        return intervals

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

        return UserGraph.get_graph_data_by_value(request, user_id, 'elo')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserGraphWinRateView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        valid, errors = UserGraph.validate_get_request(request, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        return UserGraph.get_graph_data_by_value(request, user_id, 'win_rate')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserGraphMatchesPlayedView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        valid, errors = UserGraph.validate_get_request(request, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        return UserGraph.get_graph_data_by_date(request, user_id, 'matches_played')
