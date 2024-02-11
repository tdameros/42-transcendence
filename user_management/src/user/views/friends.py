import json
from typing import Any, Optional

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.src.jwt_managers import user_authentication
from common.src.internal_requests import InternalRequests
from common.src import settings
from user.models import Friend, User
from user_management.JWTManager import get_user_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'POST', 'DELETE']), name='dispatch')
class FriendsView(View):
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
    def post(request: HttpRequest):
        user_id = get_user_id(request)
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        valid, errors = FriendsView.validate_friend_request(json_body)
        if not valid:
            return JsonResponse(data={'errors': errors}, status=400)

        try:
            valid, error = FriendsView.process_post_request(json_body, user_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        if not valid:
            return JsonResponse(data={'errors': [error]}, status=400)
        return JsonResponse(data={'message': 'friend request sent'}, status=200)

    @staticmethod
    def delete(request: HttpRequest):
        user_id = get_user_id(request)

        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        valid, errors = FriendsView.validate_friend_request(json_body)
        if not valid:
            return JsonResponse(data={'errors': errors}, status=400)

        try:
            FriendsView.process_delete_request(json_body, user_id)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        return JsonResponse(data={'message': 'friend deleted'}, status=200)

    @staticmethod
    def process_post_request(json_body: Any, user_id: int) -> (bool, Optional[list[str]]):
        friend_id = json_body['friend_id']
        user_friendship = Friend.objects.filter(user_id=user_id, friend_id=friend_id)
        related_friendship = Friend.objects.filter(user_id=friend_id, friend_id=user_id)
        if user_friendship.exists():
            return False, 'Friend request already sent'
        if related_friendship.exists():
            Friend.objects.create(user_id=user_id, friend_id=friend_id, status=Friend.ACCEPTED)
            related_friendship = related_friendship.first()
            related_friendship.status = Friend.ACCEPTED
            related_friendship.save()
        else:
            Friend.objects.create(user_id=user_id, friend_id=friend_id)
            FriendsView.send_friend_request_notification(user_id, friend_id)
        return True, None

    @staticmethod
    def process_delete_request(json_body: Any, user_id: int) -> (bool, Optional[list[str]]):
        friend_id = json_body['friend_id']
        user_friendship = Friend.objects.filter(user_id=user_id, friend_id=friend_id)
        related_friendship = Friend.objects.filter(user_id=friend_id, friend_id=user_id)
        if user_friendship.exists():
            user_friendship = user_friendship.first()
            user_friendship.delete()
        if related_friendship.exists():
            related_friendship = related_friendship.first()
            related_friendship.delete()

    @staticmethod
    def validate_friend_request(json_body: Any) -> (bool, Optional[list[str]]):
        errors = []
        friend_id = json_body.get('friend_id')

        valid, error = FriendsView.validate_friend_id(friend_id)
        if not valid:
            errors.append(error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def validate_friend_id(friend_id: Any) -> (bool, Optional[str]):
        if friend_id is None:
            return False, '`friend_id` field required'
        if not isinstance(friend_id, int):
            return False, '`friend_id` field must be an integer'
        try:
            User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return False, 'User not found'
        return True, None

    @staticmethod
    def send_friend_request_notification(user_id: int, friend_id: int):
        user = User.objects.get(id=user_id)
        notification_data = {
            'title': f'Friend request from {user.username}',
            'type': 'friend_request',
            'user_list': [friend_id],
            'data': user_id,
        }
        response = InternalRequests.post(
            url=settings.USER_NOTIFICATION_ENDPOINT,
            data=json.dumps(notification_data)
            #TODO: Add authentication headers
        )
        if response.status_code != 201:
            raise Exception(f'Failed to send friend request notification : {response.text}')
