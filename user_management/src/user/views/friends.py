import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from user_management.JWTManager import get_user_id
from typing import Any, Optional

from user.models import User


@method_decorator(csrf_exempt, name='dispatch')
class FriendsView(View):
    @staticmethod
    def get(request):
        user_id = get_user_id(request)
        try:
            friends = User.objects.get(id=user_id).friends.all()
        except User.DoesNotExist:
            return JsonResponse(data={'errors': ['User not found']}, status=404)
        body = {
            'friends': [
                {
                    'id': friend.id,
                    'username': friend.username,
                } for friend in friends
            ]
        }
        return JsonResponse(data=body, status=200)

    @staticmethod
    def post(request):
        user_id = get_user_id(request)

        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse(data={'errors': 'Invalid JSON format in the request body'}, status=400)
        valid, errors = FriendsView.validate_post_request(json_body)
        if not valid:
            return JsonResponse(data={'errors': errors}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse(data={'errors': ['User not found']}, status=404)
        user.friends.add(json_body['friend_id'])
        try:
            user.save()
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
        return JsonResponse(data={'message': 'Friend added'}, status=200)

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
        return True, None