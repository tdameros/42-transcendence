import json
from typing import Any, Optional

from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import FriendsHistory, User
from common.src.jwt_managers import service_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['POST']), name='dispatch')
class UserFriendsView(View):
    @staticmethod
    def post(request: HttpRequest, user_id: int):
        try:
            json_body = json.loads(request.body)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        valid, errors = UserFriendsView.validate_post_request(json_body, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        return UserFriendsView.post_friends(user_id, json_body)

    @staticmethod
    def post_friends(user_id: int, json_body: dict) -> JsonResponse:
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        if json_body['increment']:
            user.friends += 1
        else:
            user.friends -= 1
        if user.friends < 0:
            return JsonResponse({'errors': [error.FRIENDS_NEGATIVE]}, status=400)
        try:
            new_entry = FriendsHistory.objects.create(user_id=user_id, count=user.friends)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        try:
            user.save()
        except Exception as e:
            new_entry.delete()
            return JsonResponse({'errors': [str(e)]}, status=500)
        return JsonResponse({'new_entry': model_to_dict(new_entry)}, status=201)

    @staticmethod
    def validate_post_request(json_body: Any, user_id: int) -> (bool, Optional[list[str]]):
        errors = []
        increment = json_body.get('increment')

        valid, error = UserFriendsView.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        valid, error = UserFriendsView.validate_increment(increment)
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
    def validate_increment(increment: Any) -> (bool, Optional[str]):
        if increment is None:
            return False, error.INCREMENT_REQUIRED
        if not isinstance(increment, bool):
            return False, error.INCREMENT_INVALID
        return True, None
