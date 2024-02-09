import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from common.src.jwt_managers import user_authentication
from user_management.JWTManager import get_user_id
from typing import Any, Optional

from user.models import User, Friend


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'POST']), name='dispatch')
class FriendsView(View):
    @staticmethod
    def get(request):
        user_id = get_user_id(request)
        try:
            friends = Friend.objects.filter(user_id=user_id)
        except Friend.DoesNotExist:
            return JsonResponse(data={'errors': ['User not found test']}, status=404)
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
    def post(request):
        user_id = get_user_id(request)

        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        valid, errors = FriendsView.validate_post_request(json_body)
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
        return True, None

    @staticmethod
    def validate_post_request(json_body: Any) -> (bool, Optional[list[str]]):
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
