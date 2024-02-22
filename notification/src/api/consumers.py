import json
from typing import Optional
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from api.models import Notification
from common.src.internal_requests import InternalRequests
from common.src.jwt_managers import UserAccessJWTDecoder
from notification import settings


# TODO: the customer must send each new jwt
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string.decode())
        success, payload, error = self.authenticate_user(query_params)
        if not success:
            print(error)
            await self.close()
            return
        self.jwt = query_params['Authorization'][0]
        self.group_name = f'{payload["user_id"]}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_active_notifications()
        await self.send_friend_status(self.jwt, payload['user_id'])

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            group_channels = get_channel_layer().groups.get(self.group_name, {}).items()
            if len(group_channels) == 0:
                friend_list = await self.get_friend_list(self.jwt)
                for friend in friend_list:
                    await self.send_user_status(int(self.group_name), friend['id'], 'offline')

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            await self.disconnect(0)
            await self.close()
        access_token = data.get('access_token')
        if access_token is not None and access_token != '':
            success, payload, error = UserAccessJWTDecoder.authenticate(access_token)
            if not success:
                await self.disconnect(0)
                await self.close()
                return
            self.jwt = access_token

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
                'data': notification.data,
                'new_notification': False
            }
            message_data = {
                'message': json.dumps(notification_data)
            }
            await self.send(text_data=json.dumps(message_data))

    async def send_friend_status(self, jwt, user_id):
        friend_list = await self.get_friend_list(jwt)
        if friend_list is None:
            return
        channel_layer = get_channel_layer()
        for friend in friend_list:
            if friend['status'] == 'accepted':
                friend_data = {
                    'type': 'friend_status',
                    'friend_id': friend['id'],
                }
                friend_connected = channel_layer.groups.get(f'{friend['id']}', {}).items()
                if len(friend_connected) > 0:
                    friend_data['status'] = settings.ONLINE_STATUS_STRING
                else:
                    friend_data['status'] = settings.OFFLINE_STATUS_STRING
                message_data = {'message': json.dumps(friend_data)}
                await self.send(text_data=json.dumps(message_data))
                await self.send_user_status(user_id, friend['id'], 'online')

    @staticmethod
    async def get_friend_list(jwt):
        friend_list = await sync_to_async(InternalRequests.get)(
            settings.USER_MANAGEMENT_FRIEND_ENDPOINT,
            headers={
                'Authorization': jwt
            }
        )
        if friend_list.status_code != 200:
            return None
        friend_list = await sync_to_async(friend_list.json)()
        return friend_list['friends']

    @staticmethod
    async def send_user_status(user_id, friend_id, status):
        channel_layer = get_channel_layer()
        friend_data = {
            'type': 'friend_status',
            'friend_id': user_id,
            'status': status
        }
        await channel_layer.group_send(
            f'{friend_id}',
            {
                'type': 'send_notification',
                'message': json.dumps(friend_data)
            }
        )
