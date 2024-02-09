import json
from urllib.parse import parse_qs
from typing import Optional

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from common.src.jwt_managers import UserAccessJWTDecoder
from api.models import Notification


# # Get the number of channels in the group
# group_channels = channel_layer.groups.get(f'{instance.owner_id}', {}).items()
# print(f'Nb of channels in group {instance.owner_id}: {len(group_channels)}')
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string.decode())
        success, payload, error = self.authenticate_user(query_params)
        if not success:
            print(error)
            await self.close()
            return
        self.group_name = f'{payload["user_id"]}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_active_notifications()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))

    @staticmethod
    def authenticate_user(query_params: dict) -> tuple[bool, Optional[dict], Optional[str]]:
        if 'Authorization' not in query_params:
            return False, None, 'Missing Authorization header in query params'
        jwt = query_params['Authorization'][0]
        success, payload, error = UserAccessJWTDecoder.authenticate(jwt)
        if not success:
            return False, None, error[0]
        return True, payload, None

    async def send_active_notifications(self):
        notifications = await sync_to_async(Notification.objects.filter)(owner_id=int(self.group_name))
        notifications = await sync_to_async(list)(notifications)
        for notification in notifications:
            notification_data = {
                'id': notification.id,
                'title': notification.title,
                'type': notification.type,
                'data': notification.data
            }
            message_data = {
                'message': json.dumps(notification_data)
            }
            await self.send(text_data=json.dumps(message_data))
