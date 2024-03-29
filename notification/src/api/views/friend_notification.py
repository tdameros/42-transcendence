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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['POST']), name='dispatch')
class FriendNotificationBaseView(View):
    @staticmethod
    def validate_friend_request(relationship: any) -> tuple[bool, Optional[str]]:
        if relationship is None:
            return False, error.RELATIONSHIP_REQUIRED
        if not isinstance(relationship, list):
            return False, error.INVALID_RELATIONSHIP_FORMAT
        if len(relationship) != 2:
            return False, error.INVALID_RELATIONSHIP_FORMAT
        if not all(isinstance(i, int) for i in relationship):
            return False, error.INVALID_RELATIONSHIP_FORMAT
        return True, None


class AddFriendNotificationView(FriendNotificationBaseView):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        relationship = body.get('new_relationship')
        is_valid, errors = self.validate_friend_request(relationship)

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
            'status': AddFriendNotificationView.get_friend_status(channel_layer, friend_id)
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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(service_authentication(['POST']), name='dispatch')
class DeleteFriendNotificationView(FriendNotificationBaseView):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            body = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        relationship = body.get('deleted_relationship')
        is_valid, errors = self.validate_friend_request(relationship)

        if not is_valid:
            return JsonResponse(data={'errors': errors}, status=400)

        try:
            self.send_delete_friend(relationship[0], relationship[1])
            self.send_delete_friend(relationship[1], relationship[0])
        except Exception as e:
            return JsonResponse(data={'errors': [str(e)]}, status=500)

        return JsonResponse({'message': 'Notification sent'}, status=200)

    @staticmethod
    def send_delete_friend(user_id: int, friend_id: int):
        channel_layer = get_channel_layer()
        friend_data = {
            'type': 'friend_status',
            'friend_id': friend_id,
            'status': settings.DELETED_STATUS_STRING
        }
        async_to_sync(channel_layer.group_send)(
            f'{user_id}',
            {
                'type': 'send_notification',
                'message': json.dumps(friend_data)
            }
        )
