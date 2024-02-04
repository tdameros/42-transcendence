from typing import Any, Optional

from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import Match, User
from common.src.jwt_managers import user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class UserHistoryView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        valid, errors = UserHistoryView.validate_get_request(request, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)
        page = request.GET.get('page', '1')
        page_size = request.GET.get('page_size', '10')

        return UserHistoryView.get_history_data(user_id, page, page_size)

    @staticmethod
    def get_history_data(user_id: int, page, page_size):
        history_objects = Match.objects.filter(user_id=user_id).order_by('-date')
        paginator = Paginator(history_objects, page_size)
        try:
            page_object = paginator.page(page)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        history = [{
            'id': obj.id,
            'opponent_id': obj.opponent.id if obj.opponent else None,
            'date': obj.date.isoformat(),
            'result': obj.result,
            'user_score': obj.user_score,
            'opponent_score': obj.opponent_score,
            'elo_delta': obj.user_elo_delta,
            'expected_result': obj.user_expected_result,
        } for obj in page_object]
        return JsonResponse({'history': history}, status=200)

    @staticmethod
    def validate_get_request(request: HttpRequest, user_id: int) -> (bool, Optional[list[str]]):
        errors = []
        page = request.GET.get('page', '1')
        page_size = request.GET.get('page_size', '10')

        valid, error = UserHistoryView.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        valid, error = UserHistoryView.validate_page(page)
        if not valid:
            errors.append(error)
        valid, error = UserHistoryView.validate_page_size(page_size)
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
    def validate_page(page: Any) -> (bool, Optional[str]):
        if not page.isdigit():
            return False, error.PAGE_INVALID
        if int(page) < 1:
            return False, error.PAGE_INVALID
        return True, None

    @staticmethod
    def validate_page_size(page_size: Any) -> (bool, Optional[str]):
        if not page_size.isdigit():
            return False, error.PAGE_SIZE_INVALID
        if int(page_size) < 1:
            return False, error.PAGE_SIZE_INVALID
        return True, None
