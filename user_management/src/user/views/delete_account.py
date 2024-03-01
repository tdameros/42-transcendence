import json

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.internal_requests import InternalAuthRequests, InternalRequests
from common.src.jwt_managers import user_authentication
from user.models import User, Friend
from user_management import settings
from user_management.JWTManager import get_user_id
from user_management.utils import generate_random_string


def anonymize_user(user):
    user.username = f'Deleted User {generate_random_string(7)}'
    user.email = f'deleted_user_{generate_random_string(10)}@deleted'
    user.password = generate_random_string(20)
    user.avatar = None
    user.save()


def delete_tournament(user, access_token):
    request = InternalRequests.delete(f'{settings.TOURNAMENT_URL}tournament/', headers={'Authorization': access_token})
    if not request.ok:
        raise Exception(f'Error deleting tournaments : {request.json()}')
    request = InternalAuthRequests.post(
        f'{settings.TOURNAMENT_URL}tournament/player/anonymize/',
        data=json.dumps({'user_id': user.id}),
    )
    if not request.ok:
        raise Exception(f'Error anonymizing players : {request.json()}')


def delete_account(user_id, access_token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse(data={'errors': ['User not found']}, status=404)
    except Exception as e:
        return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
    try:
        delete_tournament(user, access_token)
    except Exception as e:
        return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
    try:
        friends = Friend.objects.filter(user=user.id)
        for friend in friends:
            Friend.objects.filter(user=friend.friend.id, friend=user.id).delete()
    except Exception as e:
        return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
    try:
        anonymize_user(user)
        user.account_deleted = True
        user.save()
    except Exception as e:
        return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
    return JsonResponse(data={'message': 'Account deleted'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['DELETE']), name='dispatch')
class DeleteAccountView(View):
    @staticmethod
    def delete(request: HttpRequest):
        return delete_account(get_user_id(request), request.headers.get('Authorization'))
