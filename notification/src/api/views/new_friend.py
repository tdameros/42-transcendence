import json
from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api import error_message as error
from common.src.jwt_managers import service_authentication
from notification import settings


class NewFriendNotificationView(View):
    @method_decorator(service_authentication(['POST']))
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            body = request.body.decode('utf8')
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        relationship = body.get('new_relationship')
        is_valid, errors = NewFriendNotificationView.validate_friend_request(relationship)

        if not is_valid:
            return JsonResponse(data={'errors': errors}, status=400)

        try:
            self.send_relationship_status(relationship[0], relationship[1])
            self.send_relationship_status(relationship[1], relationship[0])
        except Exception as e:
            return JsonResponse(data={'errors': [str(e)]}, status=500)

        return JsonResponse({'message': 'Notification sent'}, status=200)

    @staticmethod
    def send_relationship_status(user_id: int, friend_id):
        channel_layer = get_channel_layer()
        friend_data = {
            'type': 'friend_status',
            'friend_id': friend_id,
            'status': NewFriendNotificationView.get_friend_status(channel_layer, friend_id)
        }
        async_to_sync(channel_layer.group_send)(
            f'{user_id}',
            {
                'type': 'send_notification',
                'message': json.dumps(friend_data)
            }
        )

    @staticmethod
    def get_friend_status(channel_layer: any, friend_id: int) -> str:
        friend_connected = channel_layer.groups.get(f'{friend_id}', {}).items()
        if len(friend_connected) > 0:
            return settings.ONLINE_STATUS_STRING
        else:
            return settings.OFFLINE_STATUS_STRING

    @staticmethod
    def validate_friend_request(friend_id: any) -> tuple[bool, Optional[str]]:
        if friend_id is None:
            return False, error.RELATIONSHIP_REQUIRED
        if not isinstance(friend_id, list):
            return False, error.INVALID_RELATIONSHIP_FORMAT
        if len(friend_id) != 2:
            return False, error.INVALID_RELATIONSHIP_FORMAT
        if not all(isinstance(i, int) for i in friend_id):
            return False, error.INVALID_RELATIONSHIP_FORMAT
        return True, None
