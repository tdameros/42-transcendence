from typing import Any, Optional

from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import User
from common.src.jwt_managers import user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
class RankingView(View):

    @staticmethod
    def get(request: HttpRequest):
        valid, errors = RankingView.validate_get_request(request)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)
        page = request.GET.get('page', '1')
        page_size = request.GET.get('page_size', '100')

        return RankingView.get_ranking(page, page_size)

    @staticmethod
    def get_ranking(page, page_size):
        users = User.objects.order_by('-elo')
        paginator = Paginator(users, page_size)
        try:
            page = paginator.page(page)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        ranking = [{
            'id': user.id,
            'elo': user.elo,
            'matches_played': user.matches_played,
            'win_rate': user.win_rate,
        } for user in page]
        body = {
            'ranking': ranking,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(body, status=200)

    @staticmethod
    def validate_get_request(request: HttpRequest) -> (bool, Optional[list[str]]):
        errors = []
        page = request.GET.get('page', '1')
        page_size = request.GET.get('page_size', '10')

        valid, error = RankingView.validate_page(page)
        if not valid:
            errors.append(error)
        valid, error = RankingView.validate_page_size(page_size)
        if not valid:
            errors.append(error)
        if errors:
            return False, errors
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
        if int(page_size) > 500:
            return False, error.PAGE_SIZE_INVALID
        return True, None
