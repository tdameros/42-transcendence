import json
from typing import Any, Optional

from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.error_message as error
from api.models import User
from common.src.jwt_managers import service_authentication, user_authentication


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET']), name='dispatch')
@method_decorator(service_authentication(['POST', 'PATCH', 'DELETE']), name='dispatch')
class UserView(View):

    @staticmethod
    def get(request: HttpRequest, user_id: int):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errors': [error.USER_NOT_FOUND]}, status=404)
        return JsonResponse(model_to_dict(user), status=200)

    @staticmethod
    def post(request: HttpRequest, user_id: int):
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        valid, errors = UserView.validate_update_request(json_body, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        if User.objects.filter(pk=user_id).exists():
            return JsonResponse({'errors': [error.USER_EXISTING]}, status=400)
        user = User()
        UserView.update_user(json_body, user)
        user.id = user_id
        try:
            user.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        return JsonResponse(model_to_dict(user), status=201)

    @staticmethod
    def patch(request: HttpRequest, user_id: int):
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        valid, errors = UserView.validate_update_request(json_body, user_id)
        if not valid:
            return JsonResponse({'errors': errors}, status=400)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errors': [error.USER_NOT_FOUND]}, status=404)
        UserView.update_user(json_body, user)
        user.save()
        return JsonResponse(model_to_dict(user), status=200)

    @staticmethod
    def delete(request: HttpRequest, user_id: int):
        valid, error_msg = UserView.validate_user_id(user_id)
        if not valid:
            return JsonResponse({'errors': [error_msg]}, status=400)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errors': [error.USER_NOT_FOUND]}, status=404)
        try:
            user.delete()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        return JsonResponse({}, status=200)

    @staticmethod
    def validate_update_request(json_body: Any, user_id: int) -> (bool, Optional[list[str]]):
        errors = []
        elo = json_body.get('elo')
        matches_played = json_body.get('matches_played')
        matches_won = json_body.get('matches_won')
        matches_lost = json_body.get('matches_lost')
        win_rate = json_body.get('win_rate')
        friends = json_body.get('friends')

        valid, error = UserView.validate_user_id(user_id)
        if not valid:
            errors.append(error)
        valid, error = UserView.validate_elo(elo)
        if elo is not None and not valid:
            errors.append(error)
        valid, error = UserView.validate_matches_played(matches_played)
        if matches_played is not None and not valid:
            errors.append(error)
        valid, error = UserView.validate_matches_won(matches_won)
        if matches_won is not None and not valid:
            errors.append(error)
        valid, error = UserView.validate_matches_lost(matches_lost)
        if matches_lost is not None and not valid:
            errors.append(error)
        valid, error = UserView.validate_win_rate(win_rate)
        if win_rate is not None and not valid:
            errors.append(error)
        valid, error = UserView.validate_friends(friends)
        if friends is not None and not valid:
            errors.append(error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def update_user(json_body: Any, user: User) -> None:
        if json_body.get('elo') is not None:
            user.elo = json_body['elo']
        if json_body.get('matches_played') is not None:
            user.matches_played = json_body['matches_played']
        if json_body.get('matches_won') is not None:
            user.matches_won = json_body['matches_won']
        if json_body.get('matches_lost') is not None:
            user.matches_lost = json_body['matches_lost']
        if json_body.get('win_rate') is not None:
            user.win_rate = json_body['win_rate']
        if json_body.get('friends') is not None:
            user.friends = json_body['friends']

    @staticmethod
    def validate_user_id(user_id: Any) -> (bool, Optional[str]):
        if user_id is None:
            return False, error.USER_ID_REQUIRED
        if not isinstance(user_id, int):
            return False, error.USER_ID_INVALID
        return True, None

    @staticmethod
    def validate_elo(elo: Any) -> (bool, Optional[str]):
        if elo is None:
            return False, error.ELO_REQUIRED
        if not isinstance(elo, int):
            return False, error.ELO_INVALID
        if elo < 0:
            return False, error.ELO_INVALID
        return True, None

    @staticmethod
    def validate_matches_played(matches_played: Any) -> (bool, Optional[str]):
        if matches_played is None:
            return False, error.MATCHES_PLAYED_REQUIRED
        if not isinstance(matches_played, int):
            return False, error.MATCHES_PLAYED_INVALID
        if matches_played < 0:
            return False, error.MATCHES_PLAYED_INVALID
        return True, None

    @staticmethod
    def validate_matches_won(matches_won: Any) -> (bool, Optional[str]):
        if matches_won is None:
            return False, error.MATCHES_WON_REQUIRED
        if not isinstance(matches_won, int):
            return False, error.MATCHES_WON_INVALID
        if matches_won < 0:
            return False, error.MATCHES_WON_INVALID
        return True, None

    @staticmethod
    def validate_matches_lost(matches_lost: Any) -> (bool, Optional[str]):
        if matches_lost is None:
            return False, error.MATCHES_LOST_REQUIRED
        if not isinstance(matches_lost, int):
            return False, error.MATCHES_LOST_INVALID
        if matches_lost < 0:
            return False, error.MATCHES_LOST_INVALID
        return True, None

    @staticmethod
    def validate_win_rate(win_rate: Any) -> (bool, Optional[str]):
        if win_rate is None:
            return False, error.WIN_RATE_REQUIRED
        if not isinstance(win_rate, float):
            return False, error.WIN_RATE_INVALID
        if win_rate < 0 or win_rate > 1:
            return False, error.WIN_RATE_INVALID
        return True, None

    @staticmethod
    def validate_friends(friends: Any) -> (bool, Optional[str]):
        if friends is None:
            return False, error.FRIENDS_REQUIRED
        if not isinstance(friends, int):
            return False, error.FRIENDS_INVALID
        if friends < 0:
            return False, error.FRIENDS_INVALID
        return True, None
