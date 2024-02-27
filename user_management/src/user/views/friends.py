import json
from typing import Any, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src import settings
from common.src.internal_requests import InternalAuthRequests
from common.src.jwt_managers import user_authentication
from user import error_messages
from user.models import Friend, User
from user_management.JWTManager import get_user_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'POST', 'DELETE']), name='dispatch')
class FriendsBaseView(View):
    @staticmethod
    def validate_friend_id(friend_id: Any) -> (bool, Optional[str]):
        if friend_id is None:
            return False, '`friend_id` field required'
        if not isinstance(friend_id, int):
            return False, '`friend_id` field must be an integer'
        try:
            User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return False, 'Friend not found'
        return True, None

    @staticmethod
    def validate_friend_id_query(friend_id: Any) -> (bool, Optional[str]):
        if friend_id is None:
            return False, '`friend_id` query parameter required'
        if not friend_id.isdigit():
            return False, '`friend_id` query parameter must be an integer'
        friend_id = int(friend_id)
        try:
            User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return False, 'Friend not found'
        return True, None

    @staticmethod
    def send_friend_request_notification(user_id: int, friend_id: int):
        user = User.objects.get(id=user_id)
        notification_data = {
            'title': f'Friend request from {user.username}',
            'type': 'friend_request',
            'user_list': [friend_id],
            'data': f'{user_id}',
        }
        try:
            response = InternalAuthRequests.post(
                url=settings.USER_NOTIFICATION_ENDPOINT,
                data=json.dumps(notification_data)
            )
        except Exception as e:
            raise Exception(f'Failed to access notification service : {e}')
        if not response.ok:
            raise Exception(f'Failed to send friend request notification : {response.text}')

    @staticmethod
    def send_user_stats_update(user_id: int, friend_id: int, increment: bool):
        data = {
            'increment': increment,
        }
        FriendsBaseView.post_friends_increment(user_id, data)
        FriendsBaseView.post_friends_increment(friend_id, data)

    @staticmethod
    def post_friends_increment(user_id: int, data: dict) -> JsonResponse:
        url = settings.USER_STATS_USER_ENDPOINT + str(user_id) + settings.USER_STATS_FRIENDS_ENDPOINT
        try:
            response = InternalAuthRequests.post(url, data=json.dumps(data))
        except Exception as e:
            raise Exception(f'Failed to access user-stats : {e}')
        if not response.ok:
            raise Exception(f'Failed to update friends in user-stats : {response.text}')


class FriendsView(FriendsBaseView):
    @staticmethod
    def get(request: HttpRequest):
        user_id = get_user_id(request)
        try:
            friends = Friend.objects.filter(user_id=user_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)

        body = {
            'friends': [
                {
                    'id': friend.friend_id,
                    'status': 'accepted' if friend.status == Friend.ACCEPTED else 'pending',
                } for friend in friends
            ]
        }
        return JsonResponse(data=body, status=200)

    @staticmethod
    def delete(request: HttpRequest):
        user_id = get_user_id(request)
        friend_id = request.GET.get('friend_id')

        valid, error = FriendsView.validate_friend_id_query(friend_id)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)

        friend_id = int(friend_id)
        try:
            valid, error = FriendsView.delete_friend(user_id, friend_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'friend deleted'}, status=200)

    @staticmethod
    def delete_friend(user_id: int, friend_id: int) -> (bool, Optional[str]):
        user_friendship = Friend.objects.filter(user_id=user_id, friend_id=friend_id).first()
        related_friendship = Friend.objects.filter(user_id=friend_id, friend_id=user_id).first()
        if user_friendship is None or related_friendship is None:
            return False, 'Friend not found'
        user_friendship.delete()
        related_friendship.delete()
        try:
            FriendsView.send_user_stats_update(user_id, friend_id, False)
            FriendsView.send_delete_friend_notification(user_id, friend_id)
        except Exception as e:
            Friend.objects.create(user_id=user_id, friend_id=friend_id, status=Friend.ACCEPTED)
            Friend.objects.create(user_id=friend_id, friend_id=user_id, status=Friend.ACCEPTED)
            raise Exception(str(e))
        return True, None

    @staticmethod
    def send_delete_friend_notification(user_id: int, friend_id: int):
        response = InternalAuthRequests.post(
            url=settings.DELETE_FRIEND_NOTIFICATION_ENDPOINT,
            data=json.dumps({
                'deleted_relationship': [user_id, friend_id]
            })
        )
        if not response.ok:
            raise Exception(f'Failed to send delete friend notification : {response.text}')


class FriendsRequestView(FriendsBaseView):
    @staticmethod
    def post(request: HttpRequest):
        user_id = get_user_id(request)
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        friend_id = json_body.get('friend_id')
        valid, error = FriendsRequestView.validate_friend_id(friend_id)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)

        if user_id == friend_id:
            return JsonResponse(data={'errors': ['You cannot send a friend request to yourself']}, status=400)
        try:
            valid, error = FriendsRequestView.post_friend_request(user_id, friend_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'friend request sent'}, status=201)

    @staticmethod
    def post_friend_request(user_id: int, friend_id: int) -> (bool, Optional[str]):
        user_friendship = Friend.objects.filter(user_id=user_id, friend_id=friend_id)
        if user_friendship.exists():
            status = 'accepted' if user_friendship.first().status == Friend.ACCEPTED else 'pending'
            return False, f'Friend status: {status}'
        Friend.objects.create(user_id=user_id, friend_id=friend_id)
        FriendsRequestView.send_friend_request_notification(user_id, friend_id)
        return True, None


class FriendsAcceptView(FriendsBaseView):
    @staticmethod
    def post(request: HttpRequest):
        user_id = get_user_id(request)
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        friend_id = json_body.get('friend_id')
        valid, error = FriendsAcceptView.validate_friend_id(friend_id)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)

        try:
            valid, error = FriendsAcceptView.accept_friend_request(user_id, friend_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'friend request accepted'}, status=200)

    @staticmethod
    def accept_friend_request(user_id: int, friend_id: int) -> (bool, Optional[str]):
        related_friendship = Friend.objects.filter(user_id=friend_id, friend_id=user_id).first()
        if related_friendship is None:
            return False, 'Friend request not found'
        if related_friendship.status == Friend.ACCEPTED:
            return False, 'Friend request already accepted'
        related_friendship.status = Friend.ACCEPTED
        related_friendship.save()
        user_friendship = Friend.objects.filter(user_id=user_id, friend_id=friend_id).first()
        if user_friendship is None:
            user_friendship = Friend.objects.create(user_id=user_id, friend_id=friend_id, status=Friend.ACCEPTED)
        else:
            user_friendship.status = Friend.ACCEPTED
            user_friendship.save()
        try:
            FriendsView.send_user_stats_update(user_id, friend_id, True)
            FriendsAcceptView.send_new_friend_notification(user_id, friend_id)
        except Exception as e:
            related_friendship.status = Friend.PENDING
            related_friendship.save()
            user_friendship.delete()
            raise Exception(str(e))
        return True, None

    @staticmethod
    def send_new_friend_notification(user_id: int, friend_id: int):
        response = InternalAuthRequests.post(
            url=settings.ADD_FRIEND_NOTIFICATION_ENDPOINT,
            data=json.dumps({
                'new_relationship': [user_id, friend_id]
            })
        )
        if not response.ok:
            raise Exception(f'Failed to send add friend notification : {response.text}')


class FriendsDeclineView(FriendsBaseView):
    @staticmethod
    def post(request: HttpRequest):
        user_id = get_user_id(request)
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        friend_id = json_body.get('friend_id')
        valid, error = FriendsDeclineView.validate_friend_id(friend_id)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)

        try:
            valid, error = FriendsDeclineView.decline_friend_request(user_id, friend_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'friend request declined'}, status=200)

    @staticmethod
    def decline_friend_request(user_id: int, friend_id: int) -> (bool, Optional[str]):
        related_friendship = Friend.objects.filter(user_id=friend_id, friend_id=user_id).first()
        if related_friendship is None:
            return False, 'Friend request not found'
        if related_friendship.status == Friend.ACCEPTED:
            return False, 'Friend request already accepted'
        related_friendship.delete()
        return True, None


@method_decorator(user_authentication(['GET']), name='dispatch')
class FriendStatusView(View):
    @staticmethod
    def get(request: HttpRequest):
        user_id = get_user_id(request)
        friend_id, error = FriendStatusView.get_friend_id(request)
        if friend_id == -1:
            return JsonResponse(data={'errors': [error]}, status=400)

        try:
            user_friendship = Friend.objects.get(user_id=user_id, friend_id=friend_id)
        except ObjectDoesNotExist:
            try:
                user_friendship = Friend.objects.get(user_id=friend_id, friend_id=user_id)
            except ObjectDoesNotExist:
                return JsonResponse(data={'status': 'not_friend'}, status=200)
        if user_friendship.status == Friend.PENDING:
            return JsonResponse(data={'status': 'pending'}, status=200)
        return JsonResponse(data={'status': 'accepted'}, status=200)

    @staticmethod
    def get_friend_id(request: HttpRequest) -> tuple[int, Optional[str]]:
        friend_id = request.GET.get('friend_id')
        if friend_id is None:
            return -1, error_messages.MISSING_FRIEND_ID
        if not friend_id.isdigit():
            return -1, error_messages.FRIEND_ID_NOT_INT
        friend_id = int(friend_id)
        return friend_id, None
